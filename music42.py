from music21 import *

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
