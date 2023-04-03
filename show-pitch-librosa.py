import librosa
import librosa.display
import numpy as np
import pyaudio
import matplotlib as plt

# Set the frame size and sampling rate for the audio input
frame_size = 2048
sample_rate = 44100

# Set the pitch detection parameters
fmin = librosa.note_to_hz('C2')  # Minimum frequency to detect
fmax = librosa.note_to_hz('C7')  # Maximum frequency to detect

# Initialize the PyAudio object
p = pyaudio.PyAudio()

# Open the audio input stream
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sample_rate, input=True, frames_per_buffer=frame_size)

# Initialize the pitch detector
pitch = librosa.yin(frame_size, fmin=fmin, fmax=fmax)

# Create a figure for plotting the pitch
fig, ax = plt.subplots()

# Continuously read audio data from the stream and detect the pitch in real-time
while True:
    # Read a frame of audio data from the stream
    data = stream.read(frame_size, exception_on_overflow=False)
    
    # Convert the audio data to a numpy array
    y = np.frombuffer(data, dtype=np.float32)
    
    # Detect the pitch of the audio frame
    pitch_hz = pitch(y)
    
    # Print the detected pitch in Hz
    print(f"Detected pitch: {pitch_hz:.2f} Hz")
    
    # Clear the plot and plot the current pitch
    ax.clear()
    librosa.display.pitch(pitch_hz, ax=ax, y_axis='hz', fmin=fmin, fmax=fmax)
    
    # Show the plot
    plt.show(block=False)
    plt.pause(0.001)
