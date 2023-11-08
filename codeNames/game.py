import sys

sys.path.insert(1, '.')

import random
import os

from codeNames.base_elements.word import Word
from codeNames.base_elements.card import Card
from typing import List
from termcolor import colored

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
LIST_WORDS = open(f'{PROJECT_PATH}{os.path.sep}resources{os.path.sep}words.txt').read().splitlines()


class Team:
    def __init__(self, name: str, players: List['Player'] = [], is_first: bool = False):
        self.name = name
        self.players: List['Player'] = []
        self.is_first = is_first

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"

    def assign_roles(self) -> None:
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

    def set_role(self, given_role: str) -> None:
        self.role = given_role


class Game:
    def __init__(self, id: str, team1: Team, team2: Team):
        self.id = id
        self.team1 = team1
        self.team2 = team2
        self.words = self.create_pool_words()
        self.cards = self.create_cards()

    def setup(self) -> None:
        print(f'=== Game {self.id} ===')
        self.check_requirements()
        random.choice([self.team1, self.team2]).is_first = True
        print(f'Team {self.team1.name} -- {self.team1.is_first} -- {self.team1.players}')
        print(f'Team {self.team2.name} -- {self.team2.is_first} -- {self.team2.players}')
        print(self.cards)
        print()
        self.display()

    def check_requirements(self) -> None:
        assert all(len(team.players) >= 2 for team in [self.team1, self.team2])
        if not any(player.role == 'spy' for team in [self.team1, self.team2] for player in team.players):
            for team in [self.team1, self.team2]:
                team.assign_roles()
        assert any(player.role == 'spy' for team in [self.team1, self.team2] for player in team.players)

    @staticmethod
    def create_pool_words() -> List[Word]:
        return list(map(lambda w: w.upper(), random.sample(LIST_WORDS, 25)))

    def create_cards(self):
        list_cards = []

        occurrences = {'red': 8, 'blue': 9, 'yellow': 7, 'black': 1}

        mapping_color = []
        for value, count in occurrences.items():
            mapping_color.extend([value] * count)
        random.shuffle(mapping_color)

        for w, c in zip(self.words, mapping_color):
            list_cards.append(Card(word=w, color=c))
        return list_cards

    def display(self):
        max_length = max(len(card.word) for card in self.cards)

        for i, card in enumerate(self.cards, start=1):
            formatted_name = f"{card.word:{max_length}}"
            if i % 5 == 0:
                print(f"| {colored(formatted_name, card.color)} |")
                if i < len(self.cards):
                    print("+-" + "-" * (6 * max_length) + "-+")
            else:
                print(f"| {colored(formatted_name, card.color)} ", end=" ")


team_1 = Team('team_1')
team_A = Team('team_A')
p1 = Player('p1', team_1)
p2 = Player('p2', team_1)
pA = Player('pA', team_A)
pB = Player('pB', team_A)

game_test = Game('test', team_1, team_A)
game_test.setup()
