import pyaudio
import numpy as np
import math
import matplotlib.pyplot as plt

# initialize PyAudio
p = pyaudio.PyAudio()

# open stream using default input device
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024,
                input_device_index=3)

# create a new plot to show the pitch and signal over time
fig, (ax_pitch, ax_signal) = plt.subplots(2, figsize=(8, 6))
x = np.arange(0, 2 * 1024, 2)
line_pitch, = ax_pitch.plot([], [], lw=2)
line_signal, = ax_signal.plot([], [], lw=2)
ax_pitch.set_ylim(0, 1500)
ax_pitch.set_xlim(0, 1024)
ax_pitch.set_title('Pitch over time')
ax_pitch.set_xlabel('Time')
ax_pitch.set_ylabel('Pitch (Hz)')
ax_signal.set_ylim(-1, 1)
ax_signal.set_xlim(0, 2 * 1024)
ax_signal.set_title('Signal over time')
ax_signal.set_xlabel('Time')
ax_signal.set_ylabel('Amplitude')

fundamental_freq = 0.0

# callback function to read audio data and update plot
def update_plot(frame):
    global fundamental_freq

    # read audio data
    data = stream.read(1024, exception_on_overflow=False)
    # convert data to numpy array
    data = np.frombuffer(data, dtype=np.float32)

    # calculate pitch
    autocorr = np.correlate(data, data, mode='full')
    autocorr = autocorr[len(autocorr)//2:]
    # find the first peak in the autocorrelation
    start = 0
    while autocorr[start] > autocorr[start + 1]:
        start += 1
    peak = start
    while peak < len(autocorr) and autocorr[peak] > autocorr[peak - 1]:
        peak += 1
    if peak == len(autocorr):
        peak = 0
    fundamental_period = peak + start
    fundamental_freq = 44100.0 / fundamental_period
    # handle case where fundamental_freq is zero or negative
    if fundamental_freq <= 0:
        note_index = 0
    else:
        note_index = int(round(12 * math.log2(fundamental_freq / 440.0))) % 12

    # update plot
    line_pitch.set_data(x[:len(data)//2], autocorr[:len(data)//2])
    line_signal.set_data(x, data)
    ax_pitch.set_title(f'Pitch over time: {note_names[note_index]} ({fundamental_freq:.2f} Hz)')
    fig.canvas.draw()
    fig.canvas.flush_events()

    return (line_pitch,)

note_names = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

# start animation
while True:
    ani = update_plot(None)
    plt.pause(0.001)
