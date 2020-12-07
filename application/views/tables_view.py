from flask import Blueprint, request, jsonify

from application.services.tables_services import list_all_tables, create_new_table, add_team_to_table, update_score_team

bp = Blueprint("tables_view", __name__)


@bp.route('/tables', methods=["GET"])
def list_tables():
    response = list_all_tables()
    return jsonify(response.get("data")), response.get("status")


@bp.route('/tables', methods=["POST"])
def create_table():
    new_table = request.get_json()

    response = create_new_table(new_table)

    return response.get("data"), response.get("status")


@bp.route('/table/<int:table_id>', methods=["POST"])
def add_team(table_id):
    team_id = request.get_json().get("id")

    response = add_team_to_table(table_id, team_id)

    return jsonify(response.get("data")), response.get("status")


@bp.route('/table/<int:table_id>/<int:team_id>', methods=["PUT"])
def update_score(table_id, team_id):
    new_score = request.get_json().get("score")

    if type(new_score) != int:
        return 400

    response = update_score_team(table_id, team_id, new_score)

    return jsonify(response.get("data")), response.get("status")
