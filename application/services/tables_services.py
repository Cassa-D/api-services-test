import csv

from application.models.table_model import Table
from application.models.team_model import Team
from application.services.teams_sevices import list_all_teams

FILENAME = 'data/tables.csv'
FIELDNAMES = ["id", "name", "award", "table_score",
              "description", "teams_id", "teams_score"]


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
    chosen_table = Table.existing_table(table_id)
    chosen_team = Team.existing_team(team_id)

    if not chosen_table:
        return {'data': f"Não encontrado tabela com id {table_id}!", 'status': 404}
    if not chosen_team:
        return {'data': f"Não encontrado time com id {team_id}", 'status': 404}

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


def rewrite(all_tables):
    with open(FILENAME, 'w') as f:
        w = csv.DictWriter(f, FIELDNAMES)

        w.writeheader()
        w.writerows(all_tables)
