"""Initialization code for the index server API."""
from pathlib import Path

from flask import Blueprint, current_app

# Create a Blueprint for the API
api = Blueprint("api", __name__, url_prefix="/api/v1")


def load_index():
    """Load inverted index segment, stopwords, and pagerank into memory."""
    app = current_app

    # ----------------------
    # Load stopwords
    # ----------------------
    stopwords_path = Path(app.root_path) / "stopwords.txt"
    with open(stopwords_path, encoding="utf-8") as f:
        stopwords = set(w.strip() for w in f)
    app.config["STOPWORDS"] = stopwords

    # ----------------------
    # Load PageRank
    # ----------------------
    pagerank_path = Path(app.root_path) / "pagerank.out"
    pagerank = {}
    with open(pagerank_path, encoding="utf-8") as f:
        for line in f:
            docid, score = line.strip().split(",")
            pagerank[int(docid)] = float(score)
    app.config["PAGERANK"] = pagerank

    # ----------------------
    # Load inverted index segment
    # ----------------------
    inverted = {}

    with open(Path(app.config["INDEX_PATH"]), encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            idf = float(parts[1])

            postings = []
            nums = parts[2:]

            # postings come in triples: docid, termfreq, norm
            for i in range(0, len(nums), 3):
                postings.append((int(nums[i]),
                                 float(nums[i+1]),
                                 float(nums[i+2])))

            inverted[parts[0]] = (idf, postings)

    app.config["INVERTED_INDEX"] = inverted


# Import routes so they register with the blueprint
from . import main  # noqa: E402 pylint: disable=wrong-import-position
