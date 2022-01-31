from . import client
# from ..db import conn

import os
# import shutil


def bulk_index_to_elasticsearch():
    # shutil.rmtree("exports", ignore_errors=True)
    # os.makedirs("exports", exist_ok=True)
    title_akas_filepath = os.path.abspath("datasets/exports/title.akas.csv")
    name_basics_filepath = os.path.abspath("datasets/exports/name.basics.csv")

    # cur = conn.cursor()
    # cur.execute(
    #     "COPY (SELECT titleId, title FROM title_akas) TO '{}' WITH CSV HEADER".format(title_akas_filepath)
    # )
    # cur.execute(
    #     "COPY (SELECT nconst, primaryName FROM name_basics) TO '{}' WITH CSV HEADER".format(name_basics_filepath)
    # )

    client.bulk_index_from_csv(title_akas_filepath, index="title_akas")
    client.bulk_index_from_csv(name_basics_filepath, index="name_basics")
