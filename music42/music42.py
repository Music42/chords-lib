from music21 import *
import sys, os, copy, re
from collections import *

custom = {
    'color': '#000000'
}

dict = {
    'commonNotes': 'cdefgab',
    'chromaticNotes': 'C C# D- D D# E- E F F# G- G G# A- A A# B- B'.split(' '),
    'graus': 'I II III IV V VI VII VIII'.split(' ')
}

def debug(s):
    print(s)

def buildChord(mainNote, symbol = '', duration = 'whole'):
    global custom
    l = deque([note.Note('C4')])
    if symbol == 'm' or symbol == 'm7':
        l.append(note.Note('E-4'))
        l.append(note.Note('G4'))
        if symbol == 'm7':
            l.append(note.Note('B-4'))
    elif symbol == 'm(b5)':
        l.append(note.Note('E-4'))
        l.append(note.Note('G-4'))
        l.append(note.Note('B-4'))
    elif symbol == '7':
        l.append(note.Note('E4'))
        l.append(note.Note('G4'))
        l.append(note.Note('B-4'))
    elif symbol == '7M' or symbol == '':
        l.append(note.Note('E4'))
        l.append(note.Note('G4'))
        l.append(note.Note('B4'))

    l.append(note.Note('C5'))
    c = chord.Chord(l)

    a = buildInterval('C', mainNote)
    if a is not None:
        c.transpose(a, True)

    c.addLyric(mainNote.replace('-', 'b')+symbol)
    c.duration.type = duration

    c.color = custom['color']

    return c

def buildInterval(fromNote, toNote):
    dc = note.Note(fromNote)
    pc = note.Note(toNote)
    return interval.Interval(dc, pc)

def saveToXml(t, s):
    GEX = musicxml.m21ToXml.GeneralObjectExporter(s)
    out = GEX.parse()
    outStr = out.decode('utf-8')
    file_ = open(t, 'w')
    file_.write(outStr.strip())
    file_.close()
    return True

def getHarmonyForMajorScale(n, add7 = None):
    global dict

    sm = ''
    SM = ''
    if add7 is not None:
        sm = '7'
        SM = '7M'

    sc = scale.MajorScale(n)
    data = {}
    data['I'] = buildChord(sc.pitches[0].name, SM)
    data['II'] = buildChord(sc.pitches[1].name, 'm'+sm)
    data['III'] = buildChord(sc.pitches[2].name, 'm'+sm)
    data['IV'] = buildChord(sc.pitches[3].name, sm)
    data['V'] = buildChord(sc.pitches[4].name, sm)
    data['VI'] = buildChord(sc.pitches[5].name, 'm'+sm)
    data['VII'] = buildChord(sc.pitches[6].name, 'b5')
    data['VIII'] = buildChord(sc.pitches[7].name, sm)
    pitches = {}
    i = 0
    for r in dict['graus']:
        pitches[r] = sc.pitches[i].name
        i += 1

    data['pitches'] = pitches

    return data

def buildSheet(timeSignature = '4/4', title = 'Music42 Sheet', composer='@Music42', popularTitle=''):
    s= stream.Stream()
    p= stream.Part()
    s.insert(0, metadata.Metadata(
        title=title,
        popularTitle=popularTitle,
        composer = composer,
    ))
    ts0 = meter.TimeSignature(timeSignature)
    p.append(ts0)

    mm = tempo.MetronomeMark('slow')
    p.append(mm)

    data = {
        's': s,
        'p': p,
    }
    return data

def show(sheet):
    sheet['s'].append(sheet['p'])
    sheet['s'].makeNotation()
    sheet['s'].show()

def builMeasure():
    return stream.Measure()

def buildPrepareForChord(note, dn = 1):
    duration = getDurationByNumber((dn*2))
    data = getHarmonyForMajorScale(note)
    return {
        'II': buildChord(data['pitches']['II'], 'm7', duration),
        'V': buildChord(data['pitches']['V'], '7', duration),
    }

def copyChord(data, grau, duration):
    c = copy.deepcopy(data[grau])
    c.duration.type = duration
    return c

def getDurationByNumber(dn):
    durations = {
        '1' : 'whole',
        '2' : 'half',
        '4' : 'quarter'
    }
    return durations[str(dn).strip('.0')]

def addKeySignature(sheet, n):
    try:
        k = key.Key(n)
        sheet['p'][-1].insert(0, k)
    except AttributeError:
        sheet['p'].append(key.KeySignature(key.pitchToSharps(n)))
    return sheet

def appendChords(sheet, data, grau = ''):
    global custom
    o = 0
    li = grau.strip().split('-')
    for t in li:
        o += 1
        m = builMeasure()

        # Key Signature
        if o == 1:
            nk = key.Key(data['pitches']['I'])
            nk.color = custom['color']
            m.insert(0, nk)

        raw = t.strip()
        block= ''.join(c for c in raw if c not in '.|').strip().split(' ')
        if raw.startswith('|'):
            m.leftBarline = bar.Repeat(direction='start')

        if raw.endswith('|'):
            times = raw.count('.')
            if times < 1:
                times = 1
            m.rightBarline = bar.Repeat(direction='end', times=times)

        dn = len(block)

        duration = getDurationByNumber(dn)
        for g in block:
            if g[0] == 'p':
                grau = g.strip('p')
                note = data['pitches'][grau]
                pd = buildPrepareForChord(note, dn)
                m.append(pd['II'])
                m.append(pd['V'])
            else:
                c = copy.deepcopy(data[g])
                c.duration.type = duration
                m.append(c)
        #new line
        #if o == len(li):
            #m.append("\n")
        sheet['p'].append(m)

    return sheet

def circleOfFifths(n = 'C', c = 7):
    i = 1
    edgeList = []
    while i <= c:
        edgeList.append('P5')
        i += 1

    net5ths = scale.intervalNetwork.IntervalNetwork()
    net5ths.fillBiDirectedEdges(edgeList)
    l = deque([])
    for p in net5ths.realizePitch(pitch.Pitch(n)):
        l.append(p.name)
    return l
