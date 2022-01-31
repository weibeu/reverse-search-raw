from flask_cors import CORS
from flask import Flask

from . import api


blueprints = [api.bp, ]


def create_app(config=None):
    app = Flask(__name__)
    CORS(app)

    if config is not None:
        app.config.from_object(config)

    for bp in blueprints:
        app.register_blueprint(bp)

    return app
