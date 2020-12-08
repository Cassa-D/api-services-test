import csv

from application.models.team_model import Team

FILENAME = 'data/teams.csv'


def list_all_teams():
    def transform_id(team):
        team["id"] = int(team.get("id"))
        return team

    with open(FILENAME, 'r') as f:
        r = csv.DictReader(f)
        return {'data': list(map(transform_id, [team for team in r])), 'status': 200}


def create_new_team(team):
    # Começando tratação de erros:
    if (not team.get('name')
        or not team.get('player1')
            or not team.get('player2')):
        return {'data': "Hey mano, tem que mandar os bagulho certinho meu!", 'status': 400}

    new_team = Team(**team)
    new_team.get_next_id(FILENAME)

    with open(FILENAME, 'a') as f:
        FIELDNAMES = ["id", "name", "player1", "player2"]
        w = csv.DictWriter(f, FIELDNAMES)

        w.writerow(new_team.__dict__)

    return {'data': new_team.__dict__, 'status': 201}
