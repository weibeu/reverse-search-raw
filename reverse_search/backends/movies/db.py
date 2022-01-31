from ...db import conn

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

    cur.close()
    return movie_details


def get_subtitle_meta(title_id, index_, span=3):
    lower_limit = index_ - span
    upper_limit = index_ + span
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        """
        SELECT start_, end_, dialogue
        FROM title_subtitles
        WHERE titleId=%s AND index_>=%s AND index_<=%s;
        """,
        (title_id, lower_limit, upper_limit, )
    )
    results = cur.fetchall()

    cur.close()
    return results
