import librosa
import numpy as np
import pyaudio
import statistics as st
import math, struct, mouse
import keyboard as ky
from PySide6.QtCore import Signal, Qt, QObject, Slot


class noteReadWorker(QObject):
    
    # A volume treshold for notes to be registered as keystrokes
    # On my system the input background noise is around 0.37 and this causes
    # faulty detection of notes while no notes are being played
    # A treshold is neccessary to overcome this problem
    volTreshold = 0.48

    # the value of mouse position change for every note detected
    mouseMovementValue = 50

    # the amount of time between each mouse pos update
    mouseDurationValue = 0.05

    # This value direclty effects the frame size
    # Lower values grant lower latency but may cause faulty detection
    # This also directly effects how many key strokes are registered for valid notes
    # ^^^^^^ this part is subject to change
    frameSizeMultiplier = 3 

    # All notes from a to g#, this is for readers reference and not used in the program
    notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

    # A minor pentatonic scale notes
    scaleNotes = ['A2', 'C3', 'D3', 'E3', 'G3', 'A3', 'C4', 'D4', 'E4', 'G4', 'A4', 'C5']
    keyControlNotes = scaleNotes[:6]
    mouseXControlNotes = scaleNotes[6:8]
    mouseYControlNotes = scaleNotes[8:10]
    mouseClickControlNotes = scaleNotes[10:12]
    prevNote = ""

    # The flag indicates whether the shift key is being held or not
    shiftHoldFlag = False

    # Only 6 keys are mapped to the firs 5 notes of A minor pentatonic scale
    noteKeyDict = {
        keyControlNotes[0]: "w",
        keyControlNotes[1]: "s",
        keyControlNotes[2]: "a",
        keyControlNotes[3]: "d",
        keyControlNotes[4]: "space",
        keyControlNotes[5]: "shift"
    }

    noteMouse_X_PosDict = {
        mouseXControlNotes[0]: -mouseMovementValue,
        mouseXControlNotes[1]: mouseMovementValue,
    }

    noteMouse_Y_PosDict = {
        mouseYControlNotes[0]: mouseMovementValue,
        mouseYControlNotes[1]: -mouseMovementValue    
    }

    noteMouseClickDict = {
        mouseClickControlNotes[0]: 'left',
        mouseClickControlNotes[1]: 'right'
    }
    
    #stream = pyaudio.Stream()
    updateNote = Signal(str)
    shiftHoldFlag
    
    threadClosedBool = False
    
    def noteToKey(self, note):
        
        keystroke = str(self.noteKeyDict[note])
        if (keystroke != 'shift'):
            ky.send(str(self.noteKeyDict[note]))
        else:
            ky.send(str(self.noteKeyDict[note]), do_press=self.shiftHoldFlag, do_release=not(self.shiftHoldFlag))
            self.shiftHoldFlag = not(self.shiftHoldFlag)
        
    def noteToMouse(self, note):
        return (self.noteMouse_X_PosDict[note])

    # An rms function to determine the input audio volume
    def rms(self, data ):
        count = len(data)/2
        format = "%dh"%(count)
        shorts = struct.unpack( format, data )
        sum_squares = 0.0
        for sample in shorts:
            n = sample * (1.0/32768)
            sum_squares += n*n
        return math.sqrt( sum_squares / count )
    
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Define the frame size and sampling rate for the audio input
        self.frame_size = int(2048 * self.frameSizeMultiplier)
        self.sample_rate = 48000

        # Initialize the PyAudio object
        p = pyaudio.PyAudio()

        # Open the audio input stream
        self.stream = p.open(format=pyaudio.paFloat32, channels=1, rate=self.sample_rate, input=True, frames_per_buffer=self.frame_size, input_device_index=3)
    
    
    def run(self):
        self.runRead()
        
    @Slot()
    def closeEvent(self):
        self.threadClosedBool = True
        self.thread().wait()
        
        
    def runRead(self):
        # Continuously read audio data from the stream and detect the pitch in real-time
        while not self.threadClosedBool:
            # Read a frame of audio data from the stream
            data = self.stream.read(self.frame_size, exception_on_overflow=False)
            
            # Convert the audio data to a numpy array
            y = np.frombuffer(data, dtype=np.float32)
            
            # Compute the pitch using the YIN algorithm
            pitch = librosa.yin(y=y, sr=self.sample_rate, fmin=20, fmax=2000, frame_length=self.frame_size, hop_length=self.frame_size // 4)
            
            # Get the index of the maximum value in the pitch vector
            #max_idx = np.argmax(pitch)
            
            # volume is calculated for the frame
            #print(data)
            vol = self.rms(data)
            #decibel = 20 * math.log10(vol)
            
            # median of notes in the frame (depends on the frame size)
            # taking the mean would not work because plucking the strings
            # always produce a very short out of pitch noise
            # we want the pitch of the sustained note
            median = np.median(pitch)
            
            
            # Get the frequency in Hz of the maximum pitch value
            #freq_hz = librosa.note_to_hz(librosa.hz_to_note(librosa.midi_to_hz(max_idx)))
            freq_hz = median

            
            # Get the note name from the MIDI number
            note_name = librosa.hz_to_note(median)
            
            # Print the detected note name and frequency
            #print(f"Detected note: {note_name}, frequency: {freq_hz:.2f} Hz, Volume: {vol}")
            
            # print the note name and volume
            # register the related keystroke if the note is mapped and over the treshold
            if(note_name in self.noteKeyDict and vol > self.volTreshold):
                print(self.noteKeyDict[note_name] + ' Volume: ' + str(vol))
                self.noteToKey(note_name)
                prevNote = note_name
                self.updateNote.emit(self.noteKeyDict[note_name] + ' Key pressed')
                #return (self.noteKeyDict[note_name] + ' Volume: ' + "{:.3f}".format((vol)))
        
            
            if (note_name in self.noteMouse_X_PosDict and vol > self.volTreshold - 0.1):        
                print(str(self.noteMouse_X_PosDict[note_name]) + ' X, Volume: ' + str(vol))
                mouse.move(self.noteMouse_X_PosDict[note_name], 0, absolute=False, duration=self.mouseDurationValue)
                self.updateNote.emit(str(self.noteMouse_X_PosDict[note_name]) + ' Pixels Horizontal')
                #return (str(self.noteMouse_X_PosDict[note_name]) + ' X, Volume: ' + "{:.3f}".format((vol)))
                        
            if (note_name in self.noteMouse_Y_PosDict and vol > self.volTreshold - 0.1):        
                print(str(self.noteMouse_Y_PosDict[note_name]) + ' Y, Volume: ' + str(vol))
                mouse.move(0, self.noteMouse_Y_PosDict[note_name], absolute=False, duration=self.mouseDurationValue)
                self.updateNote.emit(str(self.noteMouse_Y_PosDict[note_name]) + ' Pixels Vertical')
                #return (str(self.noteMouse_Y_PosDict[note_name]) + ' Y, Volume: ' + "{:.3f}".format((vol)))
            
            if (note_name in self.noteMouseClickDict and vol > self.volTreshold - 0.1):        
                print(str(self.noteMouseClickDict[note_name]) + ' Click, Volume: ' + str(vol))
                mouse.click(self.noteMouseClickDict[note_name])
                self.updateNote.emit(str(self.noteMouseClickDict[note_name]) + ' Clicked')
                #return(str(self.noteMouseClickDict[note_name]) + ' Click, Volume: ' + "{:.3f}".format((vol)))
            
            
            #print(pitch)
            #print(data)
        print('thread closing')
    


