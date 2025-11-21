from flask import Flask
from pathlib import Path
import os

# Create the Flask app
app = Flask(__name__)

# Default inverted index file if no env variable is set
INDEX_DIR = Path(__file__).parent / "inverted_index"
app.config["INDEX_PATH"] = os.getenv(
    "INDEX_PATH",
    INDEX_DIR / "inverted_index_1.txt"
)

def load_index():
    # TODO: fill in real index loading later
    pass

# Load all index data once when the server starts
load_index()

# REGISTER THE API BLUEPRINT (THIS WAS MISSING)
from .api import api
app.register_blueprint(api)
