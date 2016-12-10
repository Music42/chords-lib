#! /usr/bin/env python3
import music42
from music21 import *

sheet = music42.buildSheet('4/4','Progression VI – IV – I – V')

for n in music42.dict['commonNotes']:
    data = music42.getHarmonyForMajorScale(n)
    i = 0
    for g in 'VI IV I V'.split(" "):
        cho = data[g]
        i += 1
        m = stream.Measure()
        if i == 1:
            m.leftBarline = 'light-heavy'

        m.append(cho)
        sheet['p'].append(m)

music42.show(sheet)
