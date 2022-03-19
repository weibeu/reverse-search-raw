from flask import Blueprint, request, abort, jsonify

import functools
import collections

from ..elasticsearch import client
from ..backends.movies.db import get_movie_details, get_subtitle_meta


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
    hits.sort(key=lambda h: h['_score'], reverse=True)

    data = dict()

    try:
        hit = hits[0]
    except IndexError:
        return jsonify(data)
    else:
        source = hit['_source']
        title_id = source['titleId']
        index_ = source['index_']

    data["movie_details"] = get_movie_details(title_id)
    data["subtitle_meta"] = get_subtitle_meta(title_id, index_)

    return jsonify(data)


@bp.route("/search-movies")
@ensure_search_query
def search_movies(query):
    hits = client.get_hits("title_akas", title=query)
    hits.sort(key=lambda h: h['_score'], reverse=True)
    data = list(collections.OrderedDict(**{
        h['_source']['titleid']: get_movie_details(h['_source']['titleid'])
        for h in hits
    }).values())
    return jsonify(data)


@bp.route("/search-names")
@ensure_search_query
def search_names(query):
    hits = client.get_hits("name_basics", primaryname=query)
    return jsonify(hits)
