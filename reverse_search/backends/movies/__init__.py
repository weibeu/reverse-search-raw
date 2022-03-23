from ...elasticsearch import client
from ...db import conn
from ...utils import cache_posters

import pysrt
import elasticsearch.helpers


def index_movie_subtitle(title_id, path):
    subs = pysrt.open(path)
    cur = conn.cursor()

    cur.execute(
        """SELECT title_basics.tconst FROM title_basics WHERE tconst=%s""",
        (title_id, )
    )
    if cur.fetchone() is None:
        print("No data registered for specified title ID.")
        return

    cur.execute(
        """SELECT title_subtitles.titleid FROM title_subtitles WHERE titleId=%s""",
        (title_id, )
    )
    if cur.fetchone() is not None:
        print("Subtitle is already registered for specified title ID.")
        cur.close()
        return

    elasticsearch_objects = list()
    for sub in subs:
        cur.execute(
            """INSERT INTO title_subtitles (titleId, index_, start_, end_, dialogue) VALUES (%s, %s, %s, %s, %s)""",
            (title_id, sub.index, str(sub.start), str(sub.end), sub.text_without_tags)
        )
        elasticsearch_objects.append(dict(
            _index="title_subtitles",
            titleId=title_id, index_=sub.index, dialogue=sub.text_without_tags.replace("\n", " ")
        ))
    conn.commit()
    cur.close()
    elasticsearch.helpers.bulk(client, elasticsearch_objects)

    poster_path = cache_posters(title_id)
    print(f"Title poster successfully written to '{poster_path}'.")
