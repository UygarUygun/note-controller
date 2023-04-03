import librosa
import numpy as np
import pyaudio
import statistics as st

# Define the frame size and sampling rate for the audio input
frame_size = 2048 * 4
sample_rate = 48000

# Initialize the PyAudio object
p = pyaudio.PyAudio()

# Open the audio input stream
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sample_rate, input=True, frames_per_buffer=frame_size, input_device_index=3)

# Continuously read audio data from the stream and detect the pitch in real-time
while True:
    # Read a frame of audio data from the stream
    data = stream.read(frame_size, exception_on_overflow=False)
    
    # Convert the audio data to a numpy array
    y = np.frombuffer(data, dtype=np.float32)
    
    # Compute the pitch using the YIN algorithm
    pitch = librosa.yin(y=y, sr=sample_rate, fmin=20, fmax=2000, frame_length=frame_size, hop_length=frame_size // 4)
    
    print(pitch)
    
    # Get the index of the maximum value in the pitch vector
    max_idx = np.argmax(pitch)
    
    median = np.median(pitch)
    #mode = st.mode(pitch)
    
    #print(max_idx)
    
    # Get the frequency in Hz of the maximum pitch value
    #freq_hz = librosa.note_to_hz(librosa.hz_to_note(librosa.midi_to_hz(max_idx)))
    freq_hz = median

    
    # Get the note name from the MIDI number
    note_name = librosa.hz_to_note(median)
    
    # Print the detected note name and frequency
    print(f"Detected note: {note_name}, frequency: {freq_hz:.2f} Hz")
