from flask import Blueprint, request, jsonify

from app.services.teams_sevices import create_new_team, list_all_teams

bp = Blueprint("teams_view", __name__)


@bp.route('/teams', methods=["GET"])
def list_teams():
    all_teams = list_all_teams()

    return jsonify(all_teams), 200


@bp.route('/teams', methods=["POST"])
def create_team():
    new_team = request.get_json()

    team_created = create_new_team(new_team)

    return team_created, 201
