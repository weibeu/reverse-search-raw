from reverse_search.elasticsearch.index import bulk_index_to_elasticsearch
from reverse_search.db.migrate import make_migrations


COMMANDS = {
    "migrate": make_migrations,
    "index": bulk_index_to_elasticsearch,
}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    command = parser.add_argument(dest="command", choices=COMMANDS.keys())

    argument, _ = parser.parse_known_args()
    try:
        COMMANDS[argument.command]()
    except KeyError:
        raise NotImplementedError
