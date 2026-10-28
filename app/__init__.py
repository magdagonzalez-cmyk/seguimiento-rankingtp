from flask import Flask

from .config import Config
from .databases import setup_database
from .routes import bp


def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    app.config.from_object(Config)

    app.register_blueprint(bp)

    with app.app_context():
        setup_database(app)

    return app
