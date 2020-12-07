from flask import Flask

from app.views.tables_view import bp as tables_view
from app.views.teams_view import bp as teams_view


def create_app():
    app = Flask(__name__)

    app.register_blueprint(tables_view)
    app.register_blueprint(teams_view)

    return app
