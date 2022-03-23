from reverse_search import config

import csv
import os
import sys
import requests

from flask import url_for


maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)


def csv_from_tsv(filename, output_filename):
    with open(filename) as tf:
        reader = csv.DictReader(tf, delimiter="\t")
        with open(output_filename, "w", newline=str()) as cf:
            writer = csv.DictWriter(cf, fieldnames=reader.fieldnames)
            writer.writeheader()
            for row in reader:
                for k, v in row.items():
                    if v == r"\N":
                        row[k] = None
                writer.writerow(row)


def cache_posters(title_id):
    headers = {"Authorization": f"Bearer {config.TMDB_ACCESS_TOKEN}"}
    params = {"external_source": "imdb_id"}
    response = requests.get(
        f"https://api.themoviedb.org/3/find/{title_id}",
        params=params, headers=headers,
    )
    if not response.ok:
        return
    data = response.json()
    title_data = data["movie_results"] or data["tv_results"]
    if not title_data:
        return
    poster_path = title_data[0]["backdrop_path"] or title_data[0]["poster_path"]
    if not poster_path:
        return

    poster_url = f"https://image.tmdb.org/t/p/original/{poster_path}"
    response = requests.get(poster_url)
    if not response.ok:
        return

    poster_path = os.path.join(config.POSTERS_BASE_PATH, f"{title_id}.png")
    with open(poster_path, "wb") as pf:
        pf.write(response.content)

    return poster_path


def get_cached_poster_url(title_id):
    return url_for("static", filename=f"posters/{title_id}.png", _external=True)
