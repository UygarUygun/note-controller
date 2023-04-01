import pyaudio
import numpy as np

# Define parameters for recording
CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Create PyAudio object
p = pyaudio.PyAudio()

# Open the stream
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)


# Get default input device info
default_device_info = p.get_default_input_device_info()
default_device_name = default_device_info['index']

# Display default input device name
print(f"Default input device: {default_device_name}")


while True:
    # Read audio data from stream
    data = stream.read(CHUNK)

    # Convert audio data to numpy array
    samples = np.frombuffer(data, dtype=np.int16)

    # Calculate the pitch using autocorrelation
    corr = np.correlate(samples, samples, mode='full')
    corr = corr[len(corr)//2:]
    pitch = RATE / np.argmax(corr)

    # Print pitch to screen
    print("Pitch: %.2f Hz" % pitch)

# Stop the stream and terminate PyAudio
stream.stop_stream()
stream.close()
p.terminate()