from environs import Env
import csv

from application.models.table_model import Table
from application.models.team_model import Team
from application.services.teams_sevices import list_all_teams

env = Env()
env.read_env()

FILENAME = 'data/tables.csv'
FIELDNAMES = ["id", "name", "award", "table_score",
              "description", "teams_id", "teams_score", "team_win"]


def list_all_tables():
    with open(FILENAME, 'r') as f:
        r = csv.DictReader(f)
        return {'data': Table.transform_in_json(r), 'status': 200}


def create_new_table(table: dict):
    new_table = Table(**table)
    new_table.get_next_id(FILENAME)

    with open(FILENAME, 'a') as f:
        w = csv.DictWriter(f, FIELDNAMES)

        w.writerow(new_table.transform_in_csv())

    return {'data': new_table.transform_in_dict(), 'status': 201}


def add_team_to_table(table_id: int, team_id: int):
    if type(team_id) != int:
        return {'data': "Id do time deve ser um inteiro!", 'status': 400}

    chosen_table = Table.existing_table(table_id)
    chosen_team = Team.existing_team(team_id)

    # Começando tratação de erros:
    if not chosen_table:
        return {'data': f"Não encontrado tabela com id {table_id}!", 'status': 404}
    if not chosen_team:
        return {'data': f"Não encontrado time com id {team_id}!", 'status': 404}

    try:
        next(team for team in chosen_table.get_teams()
             if team[0] == chosen_team.id)
        return {'data': f"Time com id {team_id} já está na tabela com id {table_id}!", 'status': 400}
    except:
        f"""Não tem nenhum time com id {table_id}! Então pode ser adicionado na tabela!"""

    max_teams = int(env("MAXTEAMS"))

    if len(chosen_table.get_teams()) >= max_teams:
        return {'data': f"Hey, só pode ter {max_teams} times para cada tabela!", 'status': 400}

    chosen_table.add_team(chosen_team.id)

    csv_table = chosen_table.transform_in_csv()

    all_tables = []
    with open(FILENAME, 'r') as f:
        r = csv.DictReader(f)

        all_tables = [table
                      if table.get("id") != csv_table.get("id")
                      else csv_table
                      for table in r]

    rewrite(all_tables)

    return {'data': chosen_table.transform_in_dict()['teams'], 'status': 202}


def update_score_team(table_id: int, team_id: int, new_score: int):
    chosen_table = Table.existing_table(table_id)

    # Começando tratação de erros:
    if type(new_score) != int:
        return {'data': "Score deve ser um inteiro!", 'status': 400}

    if not chosen_table:
        return {'data': f"Não encontrado tabela com id {table_id}!", 'status': 404}

    all_teams = chosen_table.get_teams()

    for index, team in enumerate(all_teams):
        if team[0] == team_id:
            modified_team = chosen_table.give_points(index, new_score)

            csv_table = chosen_table.transform_in_csv()

            with open(FILENAME, 'r') as f:
                r = csv.DictReader(f)

                all_tables = [table
                              if table.get("id") != csv_table.get("id")
                              else csv_table
                              for table in r]

            rewrite(all_tables)

            return {'data': modified_team, 'status': 200}

    return {'data': f"Não encontrado time com id {team_id}!", 'status': 404}


def team_have_win(table_id, team_id):
    chosen_table = Table.existing_table(table_id)

    # Começando tratação de erros:
    if not chosen_table:
        return {'data': f"Não encontrado tabela com id {table_id}!", 'status': 404}

    try:
        next(team for team in chosen_table.get_teams() if team[0] == team_id)
    except:
        return {'data': f"Time de id {team_id} não encontrado!", 'status': 404}

    if chosen_table._team_win >= 0:
        return {'data': f"Tabela com id {table_id} já possui um time vencedor!", 'status': 400}

    chosen_table.team_win(team_id)

    csv_table = chosen_table.transform_in_csv()
    with open(FILENAME, 'r') as f:
        r = csv.DictReader(f)

        all_tables = [table
                      if table.get("id") != csv_table.get("id")
                      else csv_table
                      for table in r]

        rewrite(all_tables)

        return {'data': chosen_table.transform_in_dict(), 'status': 200}


def rewrite(all_tables):
    with open(FILENAME, 'w') as f:
        w = csv.DictWriter(f, FIELDNAMES)

        w.writeheader()
        w.writerows(all_tables)
