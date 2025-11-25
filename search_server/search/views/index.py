"""Serve uploaded files view."""
import flask

import search


@search.app.route("/", methods=["GET"])
def show_index():
    """Users input a query and weight and view ranked list of relevant docs."""
    return flask.render_template("index.html")
