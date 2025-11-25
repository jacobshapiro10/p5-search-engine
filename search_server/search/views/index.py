"""`Search server main page view."""
import heapq
import sqlite3
import threading

import flask
import requests
from search import app


@app.route("/")
def index():
    """View the main search page."""
    query = flask.request.args.get("q", "")
    weight = flask.request.args.get("w", "0.5")

    try:
        weight = float(weight)
    except ValueError:
        weight = 0.5

    documents = []

    if not query:
        # No query provided; show empty search page
        return flask.render_template(
            'index.html',
            query='',
            weight=weight,
            documents=[])
    responses = []
    threads = []

    def fetch(url):
        """Fetch from one index server."""
        try:
            res = requests.get(
                url,
                params={"q": query, "w": weight},
                timeout=2,
            )
            response_data = res.json()
            if isinstance(response_data, dict) and 'hits' in response_data:
                responses.append(response_data['hits'])
            else:
                responses.append(response_data)
        except requests.exceptions.RequestException:
            responses.append([])

    for url in app.config["SEARCH_INDEX_SEGMENT_API_URLS"]:
        t = threading.Thread(target=fetch, args=(url,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Merge all per-server sorted hit lists using heapq.merge
    merged = heapq.merge(
        *responses,
        key=lambda x: (-x.get("score", 0), x.get("docid", 0))
    )

    # Take top 10 without sorting the entire list
    all_hits = []
    for hit in merged:
        all_hits.append(hit)
        if len(all_hits) == 10:
            break

    # Look up document info for each hit
    db = sqlite3.connect(app.config['DATABASE_FILENAME'])
    db.row_factory = sqlite3.Row
    for hit in all_hits:
        docid = hit.get('docid')
        cur = db.execute(
            "SELECT title, url, summary FROM Documents WHERE docid = ?",
            (docid,)
        )
        row = cur.fetchone()
        if row:
            documents.append({
                'title': row['title'],
                'url': row['url'],
                'summary': row['summary'],
                'score': hit.get('score', 0)
            })
    db.close()

    return flask.render_template(
        "index.html",
        query=query,
        weight=weight,
        documents=documents,
    )
