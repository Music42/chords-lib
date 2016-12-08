import music42
from music21 import *

s = stream.Stream()
p = stream.Part()
m = stream.Measure()

s.insert(0, metadata.Metadata())
s.metadata.title = 'Chords Lib'
s.metadata.composer = '@Music42'

p.insert(0, metadata.Metadata())
p.metadata.title = 'List'

ts0 = meter.TimeSignature('4/4')
p.append(ts0)

for mainNote in ['C', 'C#', 'D-', 'D', 'D#', 'E-', 'E', 'F', 'F#', 'G-', 'G', 'G#', 'A-', 'A', 'A#', 'B-', 'B']:
    for tp in ['', 'm', 'm(b5)', '7']:
        p.append(music42.buildChord(mainNote, tp))

s.append(p)
s.show()
