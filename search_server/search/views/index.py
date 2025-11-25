"""Serve uploaded files view."""
import flask

import search

@search.app.route("/", methods=["GET"])
def show_index():
    """
    The graphical user interface (GUI) allows users to input a query and a weight,
    then view a ranked list of relevant docs.
    """

    return flask.render_template("index.html")
