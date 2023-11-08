import typing


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
