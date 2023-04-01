import pyaudio
import numpy as np
import math
import sounddevice as sd
import time

# Set up PyAudio
p = pyaudio.PyAudio()

# Set the chunk size and sampling rate
chunk_size = 1024
sampling_rate = 44100

# Let the user select the input device
print("Available input devices:")
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print((i,dev['name']))
device_index = int(input("Select input device: "))

# Open the audio stream
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=sampling_rate,
                input=True,
                frames_per_buffer=chunk_size,
                input_device_index=device_index)

# Define the pitch detection function using the Auto-correlation method
def detect_pitch_auto_corr(signal):
    """
    Detects the pitch of an audio signal using the Auto-correlation method.
    """
    # Calculate the Auto-correlation of the signal
    auto_corr = np.correlate(signal, signal, mode='full')
    auto_corr = auto_corr[len(auto_corr)//2:]

    # Find the index of the maximum Auto-correlation value
    max_idx = np.argmax(auto_corr)

    # Calculate the fundamental frequency (pitch) in Hz
    fundamental_freq = sampling_rate / max_idx

    # Calculate the note name from the fundamental frequency
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    if fundamental_freq > 0:
        note_index = int(round(12 * math.log2(fundamental_freq / 440.0))) % 12
    elif fundamental_freq == 0:
        note_index = 0
    else:
        note_index = int(round(12 * math.log2(fundamental_freq / 440.0))) % 12
    note_name = notes[note_index]

    return note_name

# Main loop
while True:
    # Read audio data from the stream
    data = stream.read(chunk_size)
    # Convert the data to a numpy array
    data = np.frombuffer(data, dtype=np.float32)
    # Play the audio data
    sd.play(data, sampling_rate)
    # Calculate the pitch of the audio data
    note = detect_pitch_auto_corr(data)
    # Display the pitch on the screen
    print(f"Note: {note}", end='\r', flush=True)
    # Wait for 0.0125 seconds before displaying the next pitch
    time.sleep(0.0125)
