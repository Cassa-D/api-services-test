import csv

from app.models.team_model import Team

FILENAME = 'data/teams.csv'


def list_all_teams():
    def transform_id(team):
        team["id"] = int(team.get("id"))
        return team

    with open(FILENAME, 'r') as f:
        r = csv.DictReader(f)
        return list(map(transform_id, [team for team in r]))


def create_new_team(team):
    new_team = Team(**team)
    new_team.get_next_id(FILENAME)

    with open(FILENAME, 'a') as f:
        FIELDNAMES = ["id", "name", "player1", "player2"]
        w = csv.DictWriter(f, FIELDNAMES)

        w.writerow(new_team.__dict__)

    return new_team.__dict__
