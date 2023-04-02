import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
import time

# Parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024*4
PLOT_INTERVAL = 50 # milliseconds
GAIN = 1.0

# PyAudio object
p = pyaudio.PyAudio()

# Stream object
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=3)

# Figure object and subplots
fig, (ax1, ax2) = plt.subplots(2)

# Frequency axis
freqs = np.fft.rfftfreq(CHUNK, 1/RATE)

# Line objects
line_fft, = ax1.plot(freqs, np.zeros(CHUNK//2+1))
line_signal, = ax2.plot(np.arange(0, CHUNK)/RATE*1000, np.zeros(CHUNK))

# Axis settings
ax1.set_xlim(20, RATE/2)
ax1.set_ylim(0, 0.05)
ax2.set_xlim(0, (CHUNK/RATE)*1000)
ax2.set_ylim(-20000, 20000)

# Plot titles
ax1.set_title('FFT')
ax2.set_title('Signal')

# Set up the gain slider
def on_gain_change(val):
    global GAIN
    GAIN = val
    print(f'Gain changed to {val}')

gain_slider_ax = fig.add_axes([0.15, 0.1, 0.7, 0.05])
gain_slider = plt.Slider(gain_slider_ax, 'Gain', 0, 10, valinit=GAIN)
gain_slider.on_changed(on_gain_change)

# Display figure
plt.tight_layout()
plt.ion()
plt.show()

# Variable to keep track of the last time the plot was updated
last_plot_time = 0

# Infinite loop
while True:
    # Read data from stream
    data = stream.read(CHUNK, exception_on_overflow=False)
    
    # Convert data to integers
    data_int = struct.unpack(str(CHUNK) + 'h', data)
    
    # Apply gain control
    data_int = np.array(data_int) * GAIN
    
    # Perform FFT and normalize
    fft = np.fft.rfft(data_int)
    fft_norm = np.abs(fft) / (CHUNK // 2)
    
    # Update line objects
    line_fft.set_ydata(fft_norm)
    line_signal.set_ydata(data_int)
    
    # Redraw figures
    plt.pause(0.001)
    
    # Update plot every PLOT_INTERVAL milliseconds
    current_time = time.time_ns()
    if current_time - last_plot_time > PLOT_INTERVAL:
        last_plot_time = current_time
        plt.draw()
