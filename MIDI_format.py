import os
import music21

from music21 import converter, harmony #armony might be used for chord symbols

#the goal is to strip all the info from a midi file using music21
#we prep the data every tree in the random forest, the first thing in
#the list being the thing we need to predict

#writes all midi events into lists of
#chords/notes,rhythm,velocity

def read_midi(dir_name):
    note_events = []
    chord_events = []
    for root, dirs, files in os.walk(dir_name, topdown=False):
        for file in files:
            print("Reading File:",file)
            midi_stream = converter.parse(os.path.join(root,file))
            # print("midi_stream is type:",type(midi_stream))
            # print("showing text:")
            # midi_stream.show('text')

            # print("each element now:")
            for element in midi_stream.flat.notesAndRests:
                # print("element:",element)
                if isinstance(element,music21.note.Note):
                    name = element.nameWithOctave
                    duration = element.duration.type
                    velocity = velocity_to_dynamic(element.volume.velocity)

                    note_events.append([name,duration,velocity])
                    chord_events.append([None,duration,None])
                    
                elif isinstance(element,music21.chord.Chord):
                    #collapse into string of pitch name
                    name = element.pitchedCommonName

                    #chord symbols are pretty cringe, they cant get octaves and crash often, maybe find an alternative

                    # symbol = harmony.chordSymbolFromChord(element)
                    # print("encoded symbol:",symbol)
                    # name = str(symbol)

                    #pitches (normal order string[its classification anyway])
                    pitches = element.normalOrderString
                    #collapse duration into float
                    duration = element.duration.type
                    #encoded velocity
                    velocity = velocity_to_dynamic(element.volume.velocity)

                    #append to chord list
                    chord_events.append([name,pitches,duration,velocity])
                    #append a rest of equal length to note list
                    note_events.append([None,None,duration,None])
                    
                else: #element is a rest
                    #encoded duration
                    duration = element.duration.type

                    #append to both lists

                    note_events.append([None,None,duration,None])
                    chord_events.append([None,None,duration,None])

    return [note_events,chord_events]

def analysis(events):
    #a little data analysis here; how many kinds of chords does it encode??

    labels = []
    for event in events:
        labels.append(event[0])

    no_repeats = set(labels)

    # print("printing list with no repeats:")
    # for element in no_repeats:
    #     print(element)
    
    print("the set is ",len(no_repeats)," long")
    print("the og list is ",len(events)," long")

#takes the events and splits into x and y training/testing 
def to_training(events,percent):

    #partition the data into the specified percent
    #e.g. a 100 length list at 70% has 70 elements
    #easy peasy?
    split_events = events[:(round(len(events)*percent))]
    # print("training split is:",len(split_events))

    # y_training = [note[0] for note in split_events]
    # x_training = [note[1:] for note in split_events]
    y_training = []
    x_training = []

    for event in split_events:
        y_training.append(event[0])
        x_training.append(event[1:])

    # print("printing x training:",len(x_training),"long")
    # for val in x_training:
    #     print(val)

    # print("printing y training:",len(y_training),"long")
    # for val in y_training:
    #     print(val)

    return x_training,y_training

def to_testing(events,percent):
    split_events = events[(round(len(events)*(1-percent))):]
    # print("testing split is:",len(split_events))

    # y_testing = [note[0] for note in split_events]
    # x_testing = [note[1:] for note in split_events]
    y_testing = []
    x_testing = []

    for event in split_events:
        y_testing.append(event[0])
        x_testing.append(event[1:])

    # print("printing x testing:",len(x_testing),"long")
    # for val in x_testing:
    #     print(val)
    
    # print("printing y testing:",len(y_testing),"long")
    # for val in y_testing:
    #     print(val)

    return x_testing,y_testing


def velocity_to_dynamic(velocity):
    if velocity <= 23:
        return 'ppp'
    elif velocity <= 36:
        return 'pp'
    elif velocity <= 49:
        return 'p'
    elif velocity <= 62:
        return 'mp'
    elif velocity <= 75:
        return 'mf'
    elif velocity <= 88:
        return 'f'
    elif velocity <= 101:
        return 'ff'
    else:
        return 'fff'

def midi_to_datasets(dir_name,trainP,testP):
    notes, chords = read_midi(dir_name)
    
    # analysis(notes)
    # analysis(chords)

    x_note_training, y_note_training = to_training(notes,trainP)
    x_note_testing, y_note_testing = to_testing(notes,0.3)

    x_chord_training, y_chord_training = to_training(chords,testP)
    x_chord_testing, y_chord_testing = to_testing(chords,testP)

    #return statement is monstrous
    #[note training and testing (x&y),chord training and testing(x&y)]
    # return [x_note_training, y_note_training,x_note_testing, y_note_testing],[x_chord_training, y_chord_training,x_chord_testing, y,chord_testing]

    #just chords for now; above return statement is for both notes and chords
    return [x_chord_training,y_chord_training,x_chord_testing,y_chord_testing]

# def main():

#     midi_to_datasets()

# main()