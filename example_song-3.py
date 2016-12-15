#! /usr/bin/env python3
from music42 import music42
from music21 import *
import time

sheet = music42.buildSheet('4/4','Campo harmônico Maior e Menor', time.strftime("%d/%m/%Y"))

for n in 'EFGABCD':
    for data in [music42.getHarmonyForMajorScale(n, True), music42.getHarmonyForMinorScale(n, True)]:
        music42.appendChords(sheet, data, '|I - II - III - IV - V - VI - VII|')

music42.show(sheet)
