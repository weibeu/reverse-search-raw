import os


class BaseConfig(object):

    POSTGRESQL = {
        "url": "postgresql+psycopg2",
        "db": "weibeu-reverse-search",
        "host": "localhost",
        "port": 5432,
        "username": "weibeu",
        "password": None,
        "pool": {
            "pool_size": 40,
            "max_overflow": 50,
            "pool_timeout": 60,
        }
    }
    ELASTICSEARCH = {
        "hosts": ["127.0.0.1:9200", ],
    }
    TMDB_ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")
    STATIC_URL_PATH = ""
    STATIC_DIR_PATH = "reverse_search/_app/static"
    POSTERS_BASE_PATH = STATIC_DIR_PATH + "/posters"


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


ENV_CONFIG_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}


def init_config(env=None):
    env = env or os.getenv("REVERSE_SEARCH_ENV", "development")
    return ENV_CONFIG_MAP[env]()


config = init_config()
