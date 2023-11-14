import sys

sys.path.insert(1, '.')

import random
import os
import spacy
import gensim.downloader as api

from codeNames.base_elements.word import Word, Clue
from codeNames.base_elements.card import Card
from typing import List
from termcolor import colored
# from gensim.models.keyedvectors import KeyedVectors
from itertools import combinations

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
LIST_WORDS = open(f'{PROJECT_PATH}{os.path.sep}resources{os.path.sep}english-nouns.txt').read().splitlines()
GOOG_VECTOR = api.load("glove-twitter-25")
nlp = spacy.load("en_core_web_sm")


class Team:
    def __init__(self, name: str):
        self.name = name
        self.players: List['Player'] = []
        self.is_first: bool = False
        self.color: str = 'red'
        self.cards_found: int = 0

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

    def wins(self):
        if self.is_first and self.cards_found == 9:
            return True
        elif self.is_first == False and self.cards_found == 8:
            return True
        else:
            return False


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
        self.clue: Clue = None

    def __str__(self):
        # return f"{self.id}, {self.team}, {self.player}"
        return f"C'est au tour de {self.player.name} ({colored(self.player.role, self.team.color)}) !"

    def __repr__(self):
        return f"Turn({self.id}, {self.team}, {self.player})"

    def action_turn(self, list_cards: List[Card]) -> bool:
        if self.player.role == 'spy':
            clue = self.give_clue(list_cards, ai=True)
            self.clue = clue
            print(f"L'indice {clue.form} a été donné pour trouver {clue.nb_cards} carte(s).")
            return True
        else:
            return False if self.guess(list_cards) == 'END' or self.team.wins() else True

    def give_clue(self, list_cards: List[Card], ai: bool = False) -> Clue:
        if ai:
            list_card_team = [c.word.lower() for c in list_cards if c.color == self.team.color]
            clue_given, pairs_card = ai_give_clue(list_card_team)
            cards_chosen = [check_card(c, list_cards) for c in pairs_card]
            nb_cards = 2
        else:
            clue_given = input("Donnez un indice : ")
            print("Vous avez saisi :", clue_given)

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

        return Clue(clue_given, cards_chosen, nb_cards)

    def guess(self, list_cards: List[Card]) -> str:
        prev_turn = self.game.turns[-2]
        nb_guess = int(prev_turn.clue.nb_cards) + 1
        print(f"Tour de l'agent ; vous avez {nb_guess} essais.")
        print(f"Vous pouvez passer votre tour en pressant les touches CTRL + C")

        cards_chosen_agent = []
        for i in range(0, int(nb_guess)):
            try:

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
                            self.team.cards_found += 1
                            continue
                        else:
                            print(f"Carte {card_found} était une carte rouge ; au tour de l'équipe adversaire")
                            other_team = next(
                                team for team in [self.game.team1, self.game.team2] if team.color != self.team.color)
                            other_team.cards_found += 1
                            return 'PASS'
                    case 'blue':
                        if self.team.color == 'blue':
                            print(f'Carte {card_found} était une carte bleue ; continuez')
                            self.team.cards_found += 1
                            continue
                        else:
                            print(f"Carte {card_found} était une carte bleue ; au tour de l'équipe adversaire")
                            other_team = next(
                                team for team in [self.game.team1, self.game.team2] if team.color != self.team.color)
                            other_team.cards_found += 1
                            return 'PASS'
                # cards_chosen_agent.append(card_found)
                return 'DONE'
            except KeyboardInterrupt:
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


def similarity_score(pairs):
    try:
        return GOOG_VECTOR.similarity(pairs[0], pairs[1])
    except KeyError as e:
        return 0.0


def same_lemma(word, list_card_words):
    doc_word = nlp(word)
    list_doc_card = [nlp(mot) for mot in list_card_words]
    return True if any(doc_card[0].lemma_ == doc_word[0].lemma_
                       for doc_card in list_doc_card) else False


def valid_word(list_word_similar, list_original_words):
    for word in list_word_similar:
        if not same_lemma(word[0], list_original_words):
            return word


def choose_word(list_words):
    scores = list(map(similarity_score, list_pairs := list(combinations(list_words, 2))))
    highest_pair = list_pairs[scores.index(max(scores))]
    word_most_similar = GOOG_VECTOR.most_similar(positive=[*highest_pair])
    chosen_word = valid_word(word_most_similar, list_words)
    print(f'{highest_pair} => {chosen_word}')
    return chosen_word, highest_pair


def ai_give_clue(list_w):
    return choose_word(list_w)


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
