import librosa
import numpy as np
import pyaudio

# Define the frame size and sampling rate for the audio input
frame_size = 1024
sample_rate = 22050

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
    pitch, mag = librosa.piptrack(y=y, sr=sample_rate, fmin=80, fmax=500)
    pitch = pitch[:, -1]  # Take the last frame

    # Get the index of the maximum value in the pitch vector
    max_idx = np.argmax(pitch)

    # Get the frequency in Hz of the maximum pitch value
    freq_hz = librosa.midi_to_hz(pitch[max_idx])/100

    # Print the detected pitch in Hz
    print(f"Detected pitch: {freq_hz:.2f} kHz")
