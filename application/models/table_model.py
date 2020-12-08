from typing import List, Tuple
import csv

from application.models.team_model import Team


class Table:
    def __init__(self, name: str, award: str, table_score: int, description: str, **_):
        self._name = name
        self._award = award
        self._table_score = table_score
        self._description = description
        self._teams: List[Tuple[int, int]] = []
        self._team_win: bool | int = False

    def add_team(self, new_team_id: int):
        self._teams.append((new_team_id, 0))

    def get_teams(self):
        return self._teams

    def give_points(self, team_id: int, points: int):
        if not self._team_win:
            self._teams[team_id] = self._teams[team_id][0], points
            return self._teams[team_id]
        return self._teams[team_id]

    def get_next_id(self, filename: str):
        with open(filename, 'r') as f:
            r = csv.DictReader(f)
            table_list = [table for table in r]

            next_id = 1
            if len(table_list) > 0:
                next_id = int(table_list[-1].get("id", "0")) + 1

            self.id = next_id

    def team_win(team_id):
        self._team_win = team_id

    def transform_in_dict(self):
        return {
            'id': self.id,
            'name': self._name,
            'award': self._award,
            'table_score': self._table_score,
            'description': self._description,
            'teams': [
                {'id': team, 'score': score}
                for team, score in self._teams
            ],
            'team_win': self._team_win
        }

    def transform_in_csv(self):
        return {
            'id': str(self.id),
            'name': self._name,
            'award': self._award,
            'table_score': str(self._table_score),
            'description': self._description,
            'teams_id': '-'.join([str(team) for team, _ in self._teams]),
            'teams_score': '-'.join([str(score) for _, score in self._teams]),
            'team_win': self._team_win
        }

    @classmethod
    def existing_table(cls, table_id: int):
        with open("data/tables.csv", 'r') as f:
            r = csv.DictReader(f)

            for table in r:
                if int(table.get("id")) == table_id:
                    break

        if int(table.get("id")) == table_id:
            created_table = cls(**table)
            created_table.id = table_id

            created_table._team_win = teable.get("team_win")

            teams_id = [int(team_id)
                        for team_id in table.get("teams_id").split("-")
                        if team_id != ""]
            teams_score = [int(score)
                           for score in table.get("teams_score").split("-")
                           if score != ""]

            for index, (team_id, team_score) in enumerate(zip(teams_id, teams_score)):
                created_table.add_team(team_id)
                created_table.give_points(index, team_score)

            return created_table
        else:
            return None

    @staticmethod
    def transform_in_json(reader):
        return [{
            'id': int(table.get("id")),
            'name': table.get("name"),
            'award': table.get("award"),
            'table_score': int(table.get("table_score")),
            'description': table.get("description"),
            'teams': [
                {'id': int(team_id),
                 'score': int(team_score)}
                for team_id, team_score in zip(table.get("teams_id").split("-"), table.get("teams_score").split("-"))
                if team_id != ""
            ],
            'team_win': table.get("team_win")
        } for table in reader]
