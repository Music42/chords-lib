#! /usr/bin/env python3
from music42 import music42
from music21 import *

sheet = music42.buildSheet('4/4','Chords Lib')

for mainNote in music42.dict['chromaticNotes']:
    for tp in ['', 'm', 'm(b5)', '7']:
        sheet['p'].append(music42.buildChord(mainNote, tp))

music42.show(sheet)
