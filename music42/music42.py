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
    elif symbol == 'm(b5)' or symbol == 'm(b5)7':
        l.append(note.Note('E-4'))
        l.append(note.Note('G-4'))
        if symbol == 'm(b5)7':
            l.append(note.Note('B-4'))
    elif symbol == '7':
        l.append(note.Note('E4'))
        l.append(note.Note('G4'))
        l.append(note.Note('B-4'))
    elif symbol == '7M' or symbol == '':
        l.append(note.Note('E4'))
        l.append(note.Note('G4'))
        if symbol == '7M':
            l.append(note.Note('B4'))

    l.append(note.Note('C5'))
    c = chord.Chord(l)

    a = buildInterval('C', mainNote)
    if a is not None:
        c.transpose(a, inPlace=True)

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

def calc7(add7):
    l = {
        'm': '',
        'M': '',
    }
    if add7 is not None:
        l['m'] = '7'
        l['M'] = '7M'
    return l

def buildPitchesForScale(sc):
    global dict
    pitches = {}
    i = 0
    for r in dict['graus']:
        pitches[r] = sc.pitches[i].name
        i += 1
    return pitches

def getHarmonyForMajorScale(n, add7 = None):
    l = calc7(add7)
    sc = scale.MajorScale(n)
    data = {}
    data['I'] = buildChord(sc.pitches[0].name, l['M'])
    data['II'] = buildChord(sc.pitches[1].name, 'm'+l['m'])
    data['III'] = buildChord(sc.pitches[2].name, 'm'+l['m'])
    data['IV'] = buildChord(sc.pitches[3].name, l['M'])
    data['V'] = buildChord(sc.pitches[4].name, l['m'])
    data['VI'] = buildChord(sc.pitches[5].name, 'm'+l['m'])
    data['VII'] = buildChord(sc.pitches[6].name, 'm(b5)'+l['m'])
    data['VIII'] = buildChord(sc.pitches[7].name, l['m'])
    data['pitches'] = buildPitchesForScale(sc)
    return data

def getHarmonyForMinorScale(n, add7 = None):
    l = calc7(add7)
    sc = scale.MinorScale(n)
    data = {}
    data['I'] = buildChord(sc.pitches[0].name, 'm'+l['m'])
    data['II'] = buildChord(sc.pitches[1].name, 'm(b5)'+l['m'])
    data['III'] = buildChord(sc.pitches[2].name, l['M'])
    data['IV'] = buildChord(sc.pitches[3].name, 'm'+l['m'])
    data['V'] = buildChord(sc.pitches[4].name, 'm'+l['m'])
    data['VI'] = buildChord(sc.pitches[5].name, l['M'])
    data['VII'] = buildChord(sc.pitches[6].name, l['m'])
    data['VIII'] = buildChord(sc.pitches[7].name, l['M'])
    data['pitches'] = buildPitchesForScale(sc)
    return data

def buildSheet(timeSignature = '4/4', title = 'Music42 Sheet', composer='@Music42', popularTitle='', metronomeMark = 90):
    s= stream.Stream()
    p= stream.Part()
    s.insert(0, metadata.Metadata(
        title=title,
        popularTitle=popularTitle,
        composer = composer,
    ))
    ts0 = meter.TimeSignature(timeSignature)
    p.append(ts0)

    mm = tempo.MetronomeMark(metronomeMark)
    p.append(mm)

    data = {
        's': s,
        'p': p,
        'title': title,
        'composer': composer,
    }
    return data

def write(sheet, format, extension):
    return sheet['s'].write(format, fp="output/%s/%s-%s.%s" % (format, sheet['composer'], sheet['title'], extension))


def show(sheet):
    sheet['s'].append(sheet['p'])
    sheet['s'].makeNotation()
    write(sheet, 'musicxml', 'mxl')
    write(sheet, 'vexflow', 'html')
    write(sheet, 'capella', 'capx')
    write(sheet, 'text', 'txt')
    write(sheet, 'textline', 'txt')
    
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
