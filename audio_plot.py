import pyaudio
import numpy as np
import matplotlib.pyplot as plt

# Initialize PyAudio
p = pyaudio.PyAudio()

# Set the plot parameters
plt.ion()
fig, ax = plt.subplots()
x = np.arange(0, 2 * 1024, 2)
line, = ax.plot(x, np.random.rand(1024), '-', lw=2)

# Ask the user to select an input device
print("Available input devices:")
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    if dev['maxInputChannels'] > 0:
        print(str(i) + ': ' + dev['name'])
device_index = int(input("Enter the index of the input device you want to use: "))

# Set the audio stream parameters
CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = int(p.get_device_info_by_index(device_index)['defaultSampleRate'])

# Open the audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=device_index)

# Initialize variables for pitch detection and plotting
pitch_values = []
frequencies = []
prev_frequency = 0

# Start the audio stream and the plot
stream.start_stream()
while stream.is_active():
    # Read audio data from the stream
    data = stream.read(CHUNK, exception_on_overflow=False)

    # Convert the audio data to a numpy array
    audio_array = np.frombuffer(data, dtype=np.float32)

    # Compute the power spectrum of the audio data
    power_spectrum = np.abs(np.fft.rfft(audio_array)) ** 2

    # Find the index of the frequency with the maximum power
    max_index = np.argmax(power_spectrum)

    # Convert the index to a frequency
    frequency = max_index * RATE / CHUNK

    # If the frequency is too low or too high, discard it and use the previous frequency instead
    if frequency < 100 or frequency > 1000:
        frequency = prev_frequency
    else:
        prev_frequency = frequency

    # Compute the pitch of the frequency in Hz
    pitch_hz = 69 + 12 * np.log2(frequency / 440)

    # Compute the pitch in musical notation (e.g. A4)
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note_number = int(round(pitch_hz))
    octave = note_number // 12 - 1
    note_name = note_names[note_number % 12]
    note = note_name + str(octave)

    # Add the pitch to the list of pitch values
    pitch_values.append(pitch_hz)
    frequencies.append(frequency)

    # Plot the pitch values in real time
    line.set_ydata(pitch_values[-1024:])
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()

    # Play back the audio input
    stream.write(data)

# Stop the audio stream and terminate PyAudio
stream.stop_stream()
stream.close()
p.terminate()
