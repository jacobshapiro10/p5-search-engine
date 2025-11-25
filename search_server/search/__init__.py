"""initialize search server package."""
from flask import Flask

app = Flask(__name__)

import search.views