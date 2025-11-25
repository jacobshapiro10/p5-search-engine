"""Configuration for the search server."""
import pathlib

SEARCH_INDEX_SEGMENT_API_URLS = [
    "http://localhost:9000/api/v1/hits/",
    "http://localhost:9001/api/v1/hits/",
    "http://localhost:9002/api/v1/hits/",
]

APPLICATION_ROOT = '/'

# Database file is var/search.sqlite3
DATABASE_FILENAME = pathlib.Path("var/search.sqlite3")
