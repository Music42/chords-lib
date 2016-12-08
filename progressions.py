import music42
from music21 import *

s = stream.Stream()
p = stream.Part()
m = stream.Measure()

s.insert(0, metadata.Metadata(
    title='Progression VI – IV – I – V',
    popularTitle='',
    composer='@Music42',
))

ts0 = meter.TimeSignature('4/4')
p.append(ts0)

#VI – IV – I – V
for n in 'cdefgab':
    sc = scale.MajorScale(n)
    p.append(music42.buildChord(sc.pitches[5].name, 'm'))
    p.append(music42.buildChord(sc.pitches[4].name))
    p.append(music42.buildChord(sc.pitches[0].name))
    p.append(music42.buildChord(sc.pitches[4].name))

s.append(p)
s.show()
