from Shikaku import *
from ShikakuVisualizer import *
from Puzzles import *
from pokorie import *
from tkinter import *

v = ShikakuVisualizer(900, True)
s = pokorie(p7, 60, None)
res = s.solution()
print(res)