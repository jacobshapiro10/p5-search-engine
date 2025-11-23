from flask import Blueprint, current_app
from pathlib import Path
# Create a Blueprint for the API
api = Blueprint("api", __name__, url_prefix="/api/v1")

def load_index():
    """Load inverted index segment, stopwords, and pagerank into memory."""
    app = current_app

    # ----------------------
    # Load stopwords
    # ----------------------
    stopwords_path = Path(app.root_path) / "stopwords.txt"
    with open(stopwords_path) as f:
        stopwords = set(w.strip() for w in f)
    app.config["STOPWORDS"] = stopwords

    # ----------------------
    # Load PageRank
    # ----------------------
    pagerank_path = Path(app.root_path) / "pagerank.out"
    pagerank = {}
    with open(pagerank_path) as f:
        for line in f:
            docid, score = line.strip().split(",")
            pagerank[int(docid)] = float(score)
    app.config["PAGERANK"] = pagerank

    # ----------------------
    # Load inverted index segment
    # ----------------------
    inverted = {}
    index_path = Path(app.config["INDEX_PATH"])

    with open(index_path) as f:
        for line in f:
            parts = line.split()
            term = parts[0]
            idf = float(parts[1])

            postings = []
            nums = parts[2:]

            # postings come in triples: docid, termfreq, norm
            for i in range(0, len(nums), 3):
                docid = int(nums[i])
                tf = float(nums[i+1])
                norm = float(nums[i+2])
                postings.append((docid, tf, norm))

            inverted[term] = (idf, postings)

    app.config["INVERTED_INDEX"] = inverted


# Import routes so they register with the blueprint
from . import main  # noqa: F401

