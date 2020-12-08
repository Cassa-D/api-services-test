from flask import Flask
from flask_cors import CORS

from application.views.tables_view import bp as tables_view
from application.views.teams_view import bp as teams_view


def create_app():
    app = Flask(__name__)

    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    app.register_blueprint(tables_view)
    app.register_blueprint(teams_view)

    return app
