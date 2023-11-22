import tkinter as tk
from codeNames.game import *


def display_ui(game, window):
    frame = tk.Frame(window)
    frame.pack(expand=True)

    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill=tk.BOTH)

    left_column = tk.Frame(main_frame, bg="white", width=150)
    left_column.pack(side=tk.LEFT, fill=tk.Y)

    text_frame = tk.Frame(main_frame)
    text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    text_widget = tk.Text(text_frame,
                          wrap=tk.WORD)
    text_widget.pack(pady=20, expand=True,
                     fill=tk.BOTH)

    right_column = tk.Frame(main_frame, bg="white", width=150)
    right_column.pack(side=tk.LEFT, fill=tk.Y)

    game.display_tinkter(game.turns[-1], text_widget)

    window.mainloop()
