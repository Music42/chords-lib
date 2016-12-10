import music42
from music21 import *

s = stream.Stream()
p = stream.Part()


s.insert(0, metadata.Metadata(
    title='Progression VI – IV – I – V',
    popularTitle='',
    composer='@Music42',
))

ts0 = meter.TimeSignature('4/4')
p.append(ts0)


#VI – IV – I – V
for n in 'cdefgab':
    data = music42.getHarmonyForMajorScale(n)
    i = 0
    for g in ['VI', 'IV', 'I', 'V']:
        cho = data[g]
        i += 1
        m = stream.Measure()
        if i == 1:
            m.leftBarline = 'light-heavy'

        m.append(cho)
        p.append(m)

s.append(p)
s.show()
