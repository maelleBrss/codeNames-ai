import sys
sys.path.insert(1, '.')
from codeNames.base_elements.card import Card

from typing import List


class Word:
    def __init__(self, form: str):
        self.form = form

    def __str__(self):
        return f"{self.form}"

    def __repr__(self):
        return f"Word({self.form})"

    def update_word(self, new_form: str):
        assert not all(char.isdigit() for char in new_form)
        self.form = new_form


class Clue(Word):
    def __init__(self, form: str, nb_cards: int, chosen_cards: List[Card] = None):
        Word.__init__(self, form)
        self.chosen_cards = chosen_cards
        self.nb_cards = nb_cards

