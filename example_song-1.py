#! /usr/bin/env python3
from music42 import music42
from music21 import *
import random

sheet = music42.buildSheet('4/4','Deus Está Aqui')
colors= ['#212F3C', '#AF601A', '#4A235A', '#9A7D0A']
i = 1
tons = 'DEFGABC'
for n in tons:
    data = music42.getHarmonyForMajorScale(n)
    music42.appendChords(sheet, data, '|I V - VI - IV V - I pIV - IV V - III VI - II V - I V ..|')
    music42.custom['color'] = random.choice(colors);
    if i < len(tons):
        m = music42.builMeasure()
        nk = key.Key('C')
        m.insert(0, nk)
        pd = music42.buildPrepareForChord(data['pitches']['II'])
        pd['II'].color = '#16A085'
        pd['V'].color = '#7DCEA0'
        m.append(pd['II'])
        m.append(pd['V'])
        sheet['p'].append(m)

    i +=1

music42.show(sheet)
