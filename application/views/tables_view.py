from flask import Blueprint, request, jsonify

from application.services.tables_services import list_all_tables, create_new_table, add_team_to_table, update_score_team, team_have_win

bp = Blueprint("tables_view", __name__)


@bp.route('/tables', methods=["GET"])
def list_tables():
    response = list_all_tables()
    return jsonify(response.get("data")), response.get("status")


@bp.route('/tables', methods=["POST"])
def create_table():
    new_table = request.get_json()

    if (
        not new_table.get('name')
        or not new_table.get('award')
        or (
            not new_table.get('table_score')
            or type(new_table.get('table_score')) != int)
        or not new_table.get('description')
    ):
        return "Hey tem que mandar as coisas certas manolo!", 400

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

    response = update_score_team(table_id, team_id, new_score)

    return jsonify(response.get("data")), response.get("status")


@bp.route('/table/<int:table_id>/<int:team_id>', methods=["GET"])
def team_win(table_id, team_id):
    response = team_have_win(table_id, team_id)

    return response.get("data"), response.get("status")
