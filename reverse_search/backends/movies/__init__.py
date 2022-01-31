from ...elasticsearch import client
from ...db import conn

import pysrt
import elasticsearch.helpers


def index_movie_subtitle(title_id, path):
    subs = pysrt.open(path)
    cur = conn.cursor()
    elasticsearch_objects = list()
    for sub in subs:
        cur.execute(
            """INSERT INTO title_subtitles (titleId, index_, start_, end_, dialogue) VALUES (%s, %s, %s, %s, %s)""",
            (title_id, sub.index, str(sub.start), str(sub.end), sub.text_without_tags)
        )
        elasticsearch_objects.append(dict(
            _index="title_subtitles",
            titleId=title_id, index_=sub.index, dialogue=sub.text_without_tags
        ))
    conn.commit()
    cur.close()
    elasticsearch.helpers.bulk(client, elasticsearch_objects)
