from ...utils import get_cached_poster_url, cache_posters
from ...db import conn

import logging
import collections
import psycopg2.extras


def get_movie_details(title_id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        """
        SELECT titleType, originalTitle, isAdult, startYear, endYear,
            runtimeMinutes, genres, averageRating, numVotes, directors, writers
        FROM title_basics
        JOIN ratings on title_basics.tConst = ratings.tConst
        JOIN title_crew tc on ratings.tConst = tc.tConst
        WHERE title_basics.tConst=%s
        """,
        (title_id, )
    )
    movie_details = cur.fetchone()
    movie_details['directors'] = movie_details['directors'] or str()
    movie_details['writers'] = movie_details['writers'] or str()
    cur.execute(
        """
        SELECT primaryName, birthYear, deathYear, primaryProfession
        FROM name_basics
        WHERE nConst IN %s
        """,
        (tuple(movie_details['directors'].split(",")), )
    )
    movie_details['directors'] = cur.fetchall()
    cur.execute(
        """
        SELECT primaryName, birthYear, deathYear, primaryProfession
        FROM name_basics
        WHERE nConst IN %s
        """,
        (tuple(movie_details['writers'].split(",")), )
    )
    movie_details['writers'] = cur.fetchall()
    cur.execute(
        """
        SELECT title, region, language
        FROM title_akas
        WHERE titleId=%s
        """,
        (title_id, )
    )
    movie_details['titleAKAS'] = cur.fetchall()
    cur.execute(
        """
        SELECT primaryName, birthyear, primaryProfession, category, characters, knownForTitles
        FROM principals JOIN name_basics ON principals.nconst=name_basics.nconst
        WHERE tconst=%s
        ORDER BY ordering
        """,
        (title_id, )
    )
    movie_details['cast'] = cur.fetchall()
    cur.execute(
        """
        SELECT title_basics.tconst, originalTitle
        FROM title_basics JOIN ratings ON title_basics.tconst=ratings.tconst
        WHERE title_basics.tconst IN %s
        ORDER BY averagerating DESC
        """,
        (tuple(tid for c in movie_details["cast"] for tid in c["knownfortitles"].split(",")), )
    )
    id_title_map = collections.OrderedDict(((r["tconst"], r["originaltitle"]) for r in cur.fetchall()))
    for cast in movie_details["cast"]:
        try:
            characters = eval(cast["characters"])
            cast["characters"] = characters[0]
        except (SyntaxError, IndexError, TypeError):
            cast["characters"] = None
        cast["knownfortitles"] = [tn for tid, tn in id_title_map.items() if tid in cast["knownfortitles"].split(",")]

    cur.close()

    try:
        cache_posters(title_id)
    except Exception as exc:
        logging.exception(exc)

    movie_details["poster"] = get_cached_poster_url(title_id)
    return movie_details


def get_subtitle_meta(title_id, index_, span=3):
    lower_limit = index_ - span
    upper_limit = index_ + span
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        """
        SELECT index_, start_, end_, dialogue
        FROM title_subtitles
        WHERE titleId=%s AND index_>=%s AND index_<=%s;
        """,
        (title_id, lower_limit, upper_limit, )
    )
    results = cur.fetchall()

    cur.close()

    for r in results:
        r["is_key_phrase"] = r["index_"] == index_
        r.pop("index_")

    return [r for r in results if not ("(" in r["dialogue"] and ")" in r["dialogue"])]
