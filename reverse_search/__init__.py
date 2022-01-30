import dotenv

dotenv.load_dotenv(dotenv_path=dotenv.find_dotenv())


from ._config import config
from ._app import create_app


app = create_app(config)
