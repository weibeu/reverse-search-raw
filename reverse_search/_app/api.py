from flask import Blueprint, request, abort, jsonify

import functools

from ..elasticsearch import client


def ensure_search_query(view):

    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if not request.args.get("query"):
            abort(400)
        return view(request.args["query"], *args, **kwargs)

    return wrapper


bp = Blueprint("api", __name__, url_prefix="/api", )


@bp.route("/search-subtitles")
@ensure_search_query
def search_subtitles(query):
    hits = client.get_hits("title_subtitles", dialogue=query)
    return jsonify(hits)


@bp.route("/search-movies")
@ensure_search_query
def search_movies(query):
    hits = client.get_hits("title_akas", title=query)
    return jsonify(hits)


@bp.route("/search-names")
@ensure_search_query
def search_names(query):
    hits = client.get_hits("name_basics", primaryname=query)
    return jsonify(hits)
