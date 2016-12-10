#! /usr/bin/env python3
from music42 import music42
from music21 import *

sheet = music42.buildSheet('4/4','Deus Está Aqui')


#for n in 'DEFG':
for n in 'D':
    sheet['p'].append(key.Key(n))
    data = music42.getHarmonyForMajorScale(n)
    sheet = music42.appendChords(sheet, data, 'I V - VI - IV V - I pIV - IV V - III VI - II V - I V')

music42.show(sheet)
