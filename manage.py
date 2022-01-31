from reverse_search.elasticsearch.index import bulk_index_to_elasticsearch
from reverse_search.db.migrate import make_migrations
from reverse_search.backends.movies import index_movie_subtitle


COMMANDS = {
    "migrate": make_migrations,
    "index-exports": bulk_index_to_elasticsearch,
    "index-movie-subs": index_movie_subtitle,
}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    command = parser.add_argument(dest="command", choices=COMMANDS.keys())
    movie_id = parser.add_argument("-mi", "--movie-id", dest="movie_id")
    subtitle_path = parser.add_argument("-sp", "--subs-path", dest="subtitle_path")

    argument, _ = parser.parse_known_args()
    try:
        if argument.command == "index-movie-subs":
            COMMANDS[argument.command](argument.movie_id, argument.subtitle_path)
        else:
            COMMANDS[argument.command]()
    except KeyError:
        raise NotImplementedError
