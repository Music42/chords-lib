from music21 import *
import sys, os

dict = {
    'commonNotes': 'cdefgab',
    'graus': 'I II III IV V VI VII VIII'.split(' ')
}

def buildChord(mainNote, symbol = '', duration = 'whole'):
    n1 = note.Note('C4')

    if symbol == 'm':
        n2 = note.Note('E-4')
        n3 = note.Note('G4')
        n4 = note.Note('B-4')
    elif symbol == 'm(b5)':
        n2 = note.Note('E-4')
        n3 = note.Note('G-4')
        n4 = note.Note('B-4')
    elif symbol == '7':
        n2 = note.Note('E4')
        n3 = note.Note('G4')
        n4 = note.Note('B-4')
    else:
        n2 = note.Note('E4')
        n3 = note.Note('G4')
        n4 = note.Note('B4')

    n5 = note.Note('C5')
    c = chord.Chord([n1, n2, n3, n4, n5])

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

    data = {
        's': s,
        'p': p,
    }

    return data

def show(sheet):
    sheet['s'].append(sheet['p'])
    sheet['s'].show()
