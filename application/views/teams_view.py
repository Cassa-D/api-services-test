from flask import Blueprint, request, jsonify

from application.services.teams_sevices import create_new_team, list_all_teams

bp = Blueprint("teams_view", __name__)


@bp.route('/teams', methods=["GET"])
def list_teams():
    response = list_all_teams()

    return jsonify(response.get('data')), response.get('status')


@bp.route('/teams', methods=["POST"])
def create_team():
    new_team = request.get_json()

    response = create_new_team(new_team)

    return response.get('data'), response.get('status')
