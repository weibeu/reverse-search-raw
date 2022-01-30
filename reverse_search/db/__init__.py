from .. import config

import psycopg2


def get_database_connection():
    db_config = config.POSTGRESQL
    return psycopg2.connect(
        f"dbname={db_config['db']} "
        f"host={db_config['host']} "
        f"port={db_config['port']} "
        f"user={db_config['username']} "
        f"password={db_config['password']}"
    )


conn = get_database_connection()
