import sys
sys.path.insert(1, '.')
from codeNames.base_elements.word import Word


class Card:
    def __init__(self, word: Word, color: str, revealed: bool = False):
        self.word = word
        self.color = color
        self.revealed = revealed

    def __str__(self):
        return f"{self.word}, {self.color}"

    def __repr__(self):
        return f"Card({self.word}, {self.color})"
