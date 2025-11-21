from flask import Blueprint

# Create a Blueprint for the API
api = Blueprint("api", __name__, url_prefix="/api/v1")

# Import routes so they register with the blueprint
from . import main  # noqa: F401
