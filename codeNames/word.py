import typing


class Word:
    def __init__(self, form: str):
        self.form = form

    def show_details(self):
        print(f'form: {self.form}')

    def update_word(self, new_form: str):
        assert not all(char.isdigit() for char in new_form)
        self.form = new_form


word1 = Word('lapin')
word2 = Word('poule')

word1.show_details()
word2.show_details()

word1.update_word('123')
word1.show_details()
