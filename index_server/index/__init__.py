"""Index server package initializer."""
import os
from pathlib import Path

from flask import Flask, current_app
from index.api import load_index

from .api import api

# Create the Flask app
app = Flask(__name__)

# Default inverted index file if no env variable is set
INDEX_DIR = Path(__file__).parent / "inverted_index"
app.config["INDEX_PATH"] = os.getenv(
    "INDEX_PATH",
    INDEX_DIR / "inverted_index_1.txt"
)

# Load all index data once when the server starts
with app.app_context():
    load_index()

# REGISTER THE API BLUEPRINT (THIS WAS MISSING)
app.register_blueprint(api)
