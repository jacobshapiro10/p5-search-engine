from flask import Flask, current_app
from pathlib import Path
import os
import index.api

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
    index.api.load_index()

# REGISTER THE API BLUEPRINT (THIS WAS MISSING)
from .api import api
app.register_blueprint(api)




