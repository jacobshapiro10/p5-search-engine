
import threading
import requests
import flask
import sqlite3
from search import app


@app.route("/")
def index():
    """Main search page."""
    query = flask.request.args.get("q", "")
    weight = flask.request.args.get("w", "0.5")

    try:
        weight = float(weight)
    except ValueError:
        weight = 0.5

    documents = []

    if query:
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
                pass

        for url in app.config["SEARCH_INDEX_SEGMENT_API_URLS"]:
            t = threading.Thread(target=fetch, args=(url,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Aggregate all hits from all index servers
        all_hits = []
        for response in responses:
            if isinstance(response, list):
                all_hits.extend(response)
        
        # Sort by score (descending) and take top 10
        all_hits.sort(key=lambda x: x.get('score', 0), reverse=True)
        top_hits = all_hits[:10]

        # Look up document info for each hit
        db = sqlite3.connect(app.config['DATABASE_FILENAME'])
        db.row_factory = sqlite3.Row
        for hit in top_hits:
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
