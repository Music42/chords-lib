#! /usr/bin/env python3
from music42 import music42
from music21 import *

sheet = music42.buildSheet('4/4','Deus Está Aqui')

i = 1
tons = 'DEFGABC'
for n in tons:
    data = music42.getHarmonyForMajorScale(n)
    sheet = music42.appendChords(sheet, data, '|I V - VI - IV V - I pIV - IV V - III VI - II V - I V ..|')

    if i < len(tons):
        m = music42.builMeasure()
        pd = music42.buildPrepareForChord(data['pitches']['II'])
        pd['II'].color = '#235409'
        pd['V'].color = '#235409'
        m.append(pd['II'])
        m.append(pd['V'])
        sheet['p'].append(m)

    i +=1


music42.show(sheet)
