#! /usr/bin/env python3
from music42 import music42
from music21 import *
import time

sheet = music42.buildSheet('4/4','Progressão I - VI - II - V', time.strftime("%d/%m/%Y"))

for n in music42.circleOfFifths('C', 6):
    data = music42.getHarmonyForMajorScale(n.strip('#'), True)
    sheet = music42.appendChords(sheet, data, '|I - VI - II - V|')


music42.show(sheet)
