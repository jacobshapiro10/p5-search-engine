"""API endpoints for the index server."""
import math
import re

from flask import current_app, jsonify, request

from . import api


# GET /api/v1/
@api.route("/")
def api_root():
    """Find API root endpoint."""
    return jsonify({
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    })


# GET /api/v1/hits/?q=hello+world&w=0.5
@api.route("/hits/")
def api_hits():
    """Find API endpoint for search hits."""
    words_to_keep = []
    translation_to_numbers = []

    stopwords = current_app.config["STOPWORDS"]

    query = request.args.get("q")
    if query is None:
        return jsonify({"error": "missing query parameter q"}), 400

    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    query = query.casefold()
    query = query.split()
    for word in query:
        if word not in stopwords and word != "":
            words_to_keep.append(word)

    tf_query = {}
    for term in words_to_keep:
        tf_query[term] = tf_query.get(term, 0) + 1

    inverted = current_app.config["INVERTED_INDEX"]

    # Translate query to vector space
    translate_vector(tf_query, inverted, translation_to_numbers)

    doc_sets = []

    # Find candidate documents containing all query terms
    for term in words_to_keep:
        if term not in inverted:
            return jsonify({"hits": []})
        _, postings = inverted[term]
        docs = {docid for (docid, _, _) in postings}
        doc_sets.append(docs)

    candidate_docs = set.intersection(*doc_sets)

    pagerank = current_app.config["PAGERANK"]
    query_terms = list(tf_query.keys())

    return compute_score(candidate_docs, query_terms,
                         translation_to_numbers, inverted, pagerank)


def translate_vector(tf_query, inverted, translation_to_numbers):
    """Translate query to vector space and normalize."""
    for key, value in tf_query.items():
        if key in inverted:
            idf_of_term = inverted[key][0]
        else:
            continue
        translation_to_numbers.append(idf_of_term * value)

    # Normalize query vector
    query_vector_before_root = 0
    for num in translation_to_numbers:
        query_vector_before_root += num * num

    final_query_vector = math.sqrt(query_vector_before_root)
    for i, val in enumerate(translation_to_numbers):
        translation_to_numbers[i] = val / final_query_vector


def compute_score(candidate_docs, query_terms,
                  translation_to_numbers, inverted, pagerank):
    """Compute scores for candidate documents and return results."""
    results = []
    # Compute scores for each candidate document
    for docid in candidate_docs:

        doc_vector = []

        # Build document vector
        build_document_vector(docid, query_terms,
                              inverted, doc_vector)

        normalized_doc = doc_vector   # already normalized!

        cos_sim = sum(
            q_i * d_i
            for q_i, d_i in zip(translation_to_numbers, normalized_doc)
        )

        w = float(request.args.get("w", "0.5"))
        pr = pagerank.get(docid, 0.0)

        final_score = w * pr + (1 - w) * cos_sim

        # Save result
        results.append({
            "docid": docid,
            "score": final_score
        })

    # Sort by score (descending)
    results.sort(key=lambda x: x["score"], reverse=True)

    return jsonify({"hits": results})


def build_document_vector(docid, query_terms, inverted, doc_vector):
    """Build document vector for a given document ID."""
    for term in query_terms:
        idf, postings = inverted[term]

        tf = 0.0
        norm = None

        for d, tf_doc, norm_doc in postings:
            if d == docid:
                tf = tf_doc
                norm = norm_doc
                break

        if norm is None:
            doc_vector.append(0.0)
        else:
            doc_vector.append((tf * idf) / norm)
