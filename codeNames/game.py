import random

from typing import List, Type, Optional


class Team:
    def __init__(self, name: str, players: List['Player'] = [], is_first: bool = False):
        self.name = name
        self.players: List['Player'] = []
        self.is_first = is_first

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"

    def assign_roles(self):
        if not any(player.role == 'spy' for player in self.players):
            random_spy = random.choice(self.players)
            random_spy.set_role('spy')

            for p in [x for x in self.players if x != random_spy]:
                p.set_role('agent')


class Player:
    def __init__(self, name: str, team: Team = None, role: str = None):
        self.name = name
        self.team = team
        self.role = role
        team.players.append(self)

    def __str__(self):
        return f"{self.name}, {self.team}, {self.role}"

    def __repr__(self):
        return f"Player({self.name}, {self.team}, {self.role})"

    def set_role(self, given_role: str):
        self.role = given_role


class Game:
    def __init__(self, id: str, team1: Team, team2: Team):
        self.id = id
        self.team1 = team1
        self.team2 = team2

    def show_details(self):
        print(f'=== Game {self.id} ===')
        self.check_requirements()
        random.choice([self.team1, self.team2]).is_first = True
        print(f'Team {self.team1.name} -- {self.team1.is_first} -- {self.team1.players}')
        print(f'Team {self.team2.name} -- {self.team2.is_first} -- {self.team2.players}')

    def check_requirements(self):
        assert all(len(team.players) >= 2 for team in [self.team1, self.team2])
        if not any(player.role == 'spy' for team in [self.team1, self.team2] for player in team.players):
            for team in [self.team1, self.team2]:
                team.assign_roles()
        assert any(player.role == 'spy' for team in [self.team1, self.team2] for player in team.players)


team_1 = Team('team_1')
team_A = Team('team_A')
p1 = Player('p1', team_1)
p2 = Player('p2', team_1)
pA = Player('pA', team_A)
pB = Player('pB', team_A)

game_test = Game('test', team_1, team_A)
game_test.show_details()
