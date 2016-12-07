# See http://web.mit.edu/music21/
# http://www.jaytomlin.com/music/settheory/help.html

import collections
from music21 import *

d = {}

def buildChord(forte, a):
    c = chord.fromForteClass(forte)
    if a is not None:
        c.transpose(a, True)

    if c.isMajorTriad():
        c.addLyric(c.pitchedCommonName+'M')
    elif c.isMinorTriad():
        c.addLyric(c.pitchedCommonName+'m')
    else:
        c.addLyric(c.pitchedCommonName+'?')

    return c;


for forte in ['3-5', '3-11', '7-35', '8-28']:
    for i in range(12):
        c = buildChord(forte, i)
        d[c.pitchedCommonName] = c

dict = collections.OrderedDict(sorted(d.items(), key=lambda t: t[0]))

display = stream.Stream()

for key, value in dict.items():
    for x in value.derivation.chain():
        display.append(x);

    display.append(value);


display.show()
