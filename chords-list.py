import collections
from music21 import *

d = {}

def buildChord(forte, a):
    c = chord.fromForteClass(forte)
    if a is not None:
        c.transpose(a, True)

    if c.isMajorTriad():
        mode = "M"
    elif c.isMinorTriad():
        mode = "m"
    else:
        mode = ""

    legend = c.pitchedCommonName.replace('--', 'b ').replace('-', ' ')+' '+mode
    #c.fullName
    c.addLyric(legend)
    c.duration.type = 'whole'

    return c;

def buildInterval(fromNote, toNote):
    dc = note.Note(fromNote)
    pc = note.Note(toNote)
    return interval.Interval(dc, pc)

for mainNote in ['c', 'c#','d', 'd#', 'e-', 'e', 'f', 'f#', 'g', 'g#', 'a-', 'a', 'a#', 'b-', 'b', 'c-']:
    sc = scale.ChromaticScale(mainNote+'3')
    for direction in ['ascending', 'descending']:
        for p in sc.getPitches(mainNote+'3', mainNote+'4', direction=direction):
            i = buildInterval(mainNote+'3', p)
            #'8-28'
            for forte in ['3-5', '3-11', '7-35']:
                c = buildChord(forte, i)
                d[c.fullName] = c

dict = collections.OrderedDict(sorted(d.items(), key=lambda t: t[0]))

s = stream.Stream()
p = stream.Part()
m = stream.Measure()

s.insert(0, metadata.Metadata())
s.metadata.title = 'Chords Lib'
s.metadata.composer = 'music42'

p.insert(0, metadata.Metadata())
p.metadata.title = 'List'

ts0 = meter.TimeSignature('4/4')
p.append(ts0)

for key, value in dict.items():
    p.append(value);
    for x in value.derivation.chain():
        p.append(x);

s.append(p)
s.show()
