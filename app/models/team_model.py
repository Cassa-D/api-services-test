import csv


class Team:
    def __init__(self, name: str, player1: str, player2: str, **_):
        self.name = name
        self.player1 = player1
        self.player2 = player2

    def get_next_id(self, filename: str):
        with open(filename, 'r') as f:
            r = csv.DictReader(f)
            team_list = [team for team in r]

            next_id = 1
            if len(team_list) > 0:
                next_id = int(team_list[-1].get("id", "0")) + 1

            self.id = next_id

    @classmethod
    def existing_team(cls, team_id: int):
        with open("data/teams.csv", 'r') as f:
            r = csv.DictReader(f)

            for team in r:
                if int(team.get("id")) == team_id:
                    break

        created_team = cls(**team)

        created_team.id = int(team.get("id"))
        return created_team
