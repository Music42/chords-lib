from music21 import *
import sys, os, copy, re
from collections import *

dict = {
    'commonNotes': 'cdefgab',
    'chromaticNotes': 'C C# D- D D# E- E F F# G- G G# A- A A# B- B'.split(' '),
    'graus': 'I II III IV V VI VII VIII'.split(' ')
}

def debug(s):
    print(s)

def buildChord(mainNote, symbol = '', duration = 'whole'):
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
    else:
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

def getHarmonyForMajorScale(n):
    global dict
    sc = scale.MajorScale(n)
    data = {}
    data['I'] = buildChord(sc.pitches[0].name)
    data['II'] = buildChord(sc.pitches[1].name, 'm')
    data['III'] = buildChord(sc.pitches[2].name, 'm')
    data['IV'] = buildChord(sc.pitches[3].name)
    data['V'] = buildChord(sc.pitches[4].name)
    data['VI'] = buildChord(sc.pitches[5].name, 'm')
    data['VII'] = buildChord(sc.pitches[6].name, 'b5')
    data['VIII'] = buildChord(sc.pitches[7].name)
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

    for t in grau.strip().split('-'):
        m = builMeasure()
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
        sheet['p'].append(m)

    return sheet
