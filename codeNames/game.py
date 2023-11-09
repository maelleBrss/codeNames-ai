import sys

sys.path.insert(1, '.')

import random
import os

from codeNames.base_elements.word import Word, Hint
from codeNames.base_elements.card import Card
from typing import List
from termcolor import colored

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
LIST_WORDS = open(f'{PROJECT_PATH}{os.path.sep}resources{os.path.sep}words.txt').read().splitlines()


class Team:
    def __init__(self, name: str):
        self.name = name
        self.players: List['Player'] = []
        self.is_first: bool = False
        self.color: str = 'red'

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


class Turn:
    def __init__(self, id: str, team: Team, player: Player, game: 'Game'):
        self.id = id
        self.team = team
        self.player = player
        self.game = game
        self.game.turns.append(self)
        self.hint: Hint = None

    def __str__(self):
        # return f"{self.id}, {self.team}, {self.player}"
        return f"C'est au tour de {self.player.name} ({colored(self.player.role, self.team.color)}) !"

    def __repr__(self):
        return f"Turn({self.id}, {self.team}, {self.player})"

    def action_turn(self, list_cards: List[Card]) -> bool:
        if self.player.role == 'spy':
            hint = self.give_hint(list_cards)
            self.hint = hint
            print(f"L'indice {hint.form} a été donné pour trouver {hint.nb_cards} carte(s).")
            return True
        else:
            return False if self.guess(list_cards) == 'END' else True

    def give_hint(self, list_cards: List[Card]) -> Hint:
        hint_given = input("Donnez un indice : ")
        print("Vous avez saisi :", hint_given)

        nb_cards = input("Donnez le nombre de cartes à faire deviner : ")
        print("Vous avez saisi :", nb_cards)
        cards_chosen = []

        for i in range(0, int(nb_cards)):
            card_input = input("Carte à faire deviner : ")
            card_found = check_card(card_input, list_cards)
            while not card_found:
                card_input = input("Veuillez choisir une carte existante. Carte à faire deviner : ")
                card_found = check_card(card_input, list_cards)
            cards_chosen.append(card_found)

        return Hint(hint_given, cards_chosen, nb_cards)

    def guess(self, list_cards: List[Card]) -> str:
        prev_turn = self.game.turns[-2]
        nb_guess = int(prev_turn.hint.nb_cards) + 1
        print(f"Tour de l'agent ; vous avez {nb_guess} essais.")

        cards_chosen_agent = []
        for i in range(0, int(nb_guess)):
            card_input = input("Carte à deviner : ")
            card_found = check_card(card_input, list_cards)
            while not card_found:
                card_input = input("Veuillez choisir une carte existante. Carte à deviner : ")
                card_found = check_card(card_input, list_cards)
            self.game.reveal_card(card_found)

            match card_found.color:
                case 'black':
                    print(f'FIN DE LA PARTIE')
                    return 'END'
                case 'yellow':
                    print(f'Carte jaune ; tour fini')
                    return 'PASS'
                case 'red':
                    if self.team.color == 'red':
                        print(f'Carte {card_found} était une carte rouge ; continuez')
                        continue
                    else:
                        print(f"Carte {card_found} était une carte rouge ; au tour de l'équipe adversaire")
                        return 'PASS'
                case 'blue':
                    if self.team.color == 'blue':
                        print(f'Carte {card_found} était une carte bleue ; continuez')
                        continue
                    else:
                        print(f"Carte {card_found} était une carte bleue ; au tour de l'équipe adversaire")
                        return 'PASS'
            # cards_chosen_agent.append(card_found)
            return 'DONE'


class Game:
    def __init__(self, id: str, team1: Team, team2: Team):
        self.id = id
        self.team1 = team1
        self.team2 = team2
        self.words: List[Word] = self.create_pool_words()
        self.cards: List[Card] = self.create_cards()
        self.turns: List[Turn] = []

    def setup(self) -> None:
        print(f'=== Game {self.id} ===')
        self.check_requirements()
        first_team = random.choice([self.team1, self.team2])
        first_team.is_first = True
        first_team.color = 'blue'
        print(f'Team {self.team1.name} -- {self.team1.is_first} -- {self.team1.color} -- {self.team1.players}')
        print(f'Team {self.team2.name} -- {self.team2.is_first} -- {self.team2.color} -- {self.team2.players}')
        print()
        print()
        self.run_game()

    def check_requirements(self) -> None:
        assert all(len(team.players) >= 2 for team in [self.team1, self.team2])
        if not any(player.role == 'spy' for team in [self.team1, self.team2] for player in team.players):
            for team in [self.team1, self.team2]:
                team.assign_roles()
        assert any(player.role == 'spy' for team in [self.team1, self.team2] for player in team.players)

    @staticmethod
    def create_pool_words() -> List[Word]:
        return list(map(lambda w: w.upper(), random.sample(LIST_WORDS, 25)))

    def create_cards(self) -> List[Card]:
        list_cards = []
        occurrences = {'red': 8, 'blue': 9, 'yellow': 7, 'black': 1}
        mapping_color = []

        for value, count in occurrences.items():
            mapping_color.extend([value] * count)
        random.shuffle(mapping_color)

        for w, c in zip(self.words, mapping_color):
            list_cards.append(Card(word=w, color=c))
        return list_cards

    def display(self, current_turn: Turn) -> None:
        max_length = max(len(card.word) for card in self.cards)

        for i, card in enumerate(self.cards, start=1):
            formatted_name = f"{card.word:{max_length}}"
            if i % 5 == 0:
                if current_turn.player.role == 'spy':
                    print(f"| {colored(formatted_name, card.color)} |")
                else:
                    print(f"| {colored(formatted_name, card.color) if card.revealed else formatted_name} |")
                if i < len(self.cards):
                    print("+-" + "-" * (6 * max_length) + "-+")
            else:
                if current_turn.player.role == 'spy':
                    print(f"| {colored(formatted_name, card.color)} ", end=" ")
                else:
                    print(f"| {colored(formatted_name, card.color) if card.revealed else formatted_name} ", end=" ")

    def reveal_card(self, input_card: Card) -> None:
        for card in self.cards:
            if card == input_card:
                card.revealed = True

    def run_game(self) -> None:
        continue_game = True
        i_turn = 1
        curr_role = 'spy'
        curr_team = next(team for team in [self.team1, self.team2] if team.is_first)

        # while i_turn <= 7:
        while continue_game:
            find_player = next(player for player in curr_team.players if player.role == curr_role)
            curr_turn = Turn(i_turn, curr_team, find_player, self)
            print(curr_turn)

            self.display(curr_turn)
            continue_game = curr_turn.action_turn(self.cards)

            curr_team = self.team1 if (curr_team == self.team2 and curr_role == 'agent') else (
                self.team2 if (curr_team == self.team1 and curr_role == 'agent') else (
                    self.team1 if (curr_team == self.team1 and curr_role == 'spy') else self.team2))

            curr_role = 'agent' if curr_role == 'spy' else 'spy'
            i_turn += 1
            print("=======")


def check_card(given_word: str, list_cards_in_game: List[Card]):
    return next((card for card in list_cards_in_game if card.word == given_word.upper()), None)


team_1 = Team('team_1')
team_A = Team('team_A')
p1 = Player('p1', team_1)
p2 = Player('p2', team_1)
pA = Player('pA', team_A)
pB = Player('pB', team_A)

game_test = Game('test', team_1, team_A)
game_test.setup()
