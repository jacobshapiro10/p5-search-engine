from flask import jsonify, request, current_app
from . import api

# GET /api/v1/
@api.route("/", methods=["GET"])
def api_root():
    return jsonify({
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    })


# GET /api/v1/hits/?q=hello+world&w=0.5
@api.route("/hits/")
def api_hits():
    q = request.args.get("q")
    if q is None:
        return jsonify({"error": "missing query parameter q"}), 400

    w = request.args.get("w", default="0.5")
    