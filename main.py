import tkinter as tk
from codeNames.game import *

team_1 = Team('team_1')
team_A = Team('team_A')
p1 = Player('p1', team_1)
p2 = Player('p2', team_1)
pA = Player('pA', team_A)
pB = Player('pB', team_A)

game_test = Game('test', team_1, team_A)
game_test.setup()

