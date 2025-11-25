"""initialize search server package."""
import urllib.parse

import flask

app = flask.Flask(__name__)  # pylint: disable=invalid-name

app.config.from_object('search.config')


@app.template_filter('urldecode')
def urldecode_filter(s):
    """Decode percent-encoded URLs (for spec requirement)."""
    return urllib.parse.unquote(s)


import search.views  # noqa: E402  pylint: disable=wrong-import-position
