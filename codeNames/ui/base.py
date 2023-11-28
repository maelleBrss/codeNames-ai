import tkinter as tk
# from codeNames.game import *
import tkinter as tk
import tkinter.ttk as ttk

#
# def display_ui(game, window):
#     frame = tk.Frame(window)
#     frame.pack(expand=True)
#
#     main_frame = tk.Frame(window)
#     main_frame.pack(expand=True, fill=tk.BOTH)
#
#     left_column = tk.Frame(main_frame, bg="white", width=150)
#     left_column.pack(side=tk.LEFT, fill=tk.Y)
#
#     text_frame = tk.Frame(main_frame)
#     text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#
#     text_widget = tk.Text(text_frame,
#                           wrap=tk.WORD)
#     text_widget.pack(pady=20, expand=True,
#                      fill=tk.BOTH)
#
#     right_column = tk.Frame(main_frame, bg="white", width=150)
#     right_column.pack(side=tk.LEFT, fill=tk.Y)
#
#     entry_widget = tk.Entry(main_frame)
#     validate_button = tk.Button(main_frame, text="Valider", command=lambda: game.on_validate(entry_widget, text_widget))
#
#     game.display_tinkter(game.turns[-1], text_widget, entry_widget)
#
#     window.mainloop()


class GameUI:
    def __init__(self, window, game):
        self.window = window
        self.game = game

        self.frame = tk.Frame(self.window)
        self.frame.pack(expand=True)

        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        self.left_column = tk.Frame(self.main_frame, bg="white", width=150)
        self.left_column.pack(side=tk.LEFT, fill=tk.Y)

        self.text_frame = tk.Frame(self.main_frame)
        self.text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.text_widget = tk.Text(self.text_frame, wrap=tk.WORD)
        self.text_widget.pack(pady=20, expand=True, fill=tk.BOTH)

        self.right_column = tk.Frame(self.main_frame, bg="white", width=150)
        self.right_column.pack(side=tk.LEFT, fill=tk.Y)

        self.tk_entry_widget = tk.Entry(self.main_frame)
        self.tk_combobox = ttk.Combobox(self.main_frame, values=[str(i) for i in range(1, 8)])
        self.tk_validate_button = tk.Button(self.main_frame, text="Valider", command=self.on_validate)

        # if game.turns[-1].player.role == 'spy':
        #     self.entry_widget = tk.Entry(self.main_frame)
        #     self.validate_button = tk.Button(self.main_frame, text="Valider", command=self.on_validate)

        self.window.after(1000, self.poll_background)

    def on_validate(self):
        self.game.on_validate(self.game.turns[-1])

    def poll_background(self):
        self.window.after(1000, self.poll_background)

    def run_ui(self):
        self.game.display_tinkter(self.game.turns[-1], self.text_widget)
        self.window.mainloop()

