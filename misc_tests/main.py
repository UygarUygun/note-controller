import wave
import matplotlib.pyplot as plt
import numpy as np

debug = True
fileName = "drums.wav"

obj = wave.open(fileName, "rb")


if debug:
    print("Number of Channels " + str(obj.getnchannels()))
    print("Sample Width " + str(obj.getsampwidth()))
    print("Framerate " + str(obj.getframerate()))
    print("Number of Frames " + str(obj.getnframes()))
    print("Parameters " + str(obj.getparams()))
    



sample_freq = obj.getframerate()
n_samples = obj.getnframes()

#reads all the frames
signal_wave = obj.readframes(-1)

obj.close()

time_audio = n_samples / sample_freq

print("Time of Audio " + str(np.ceil(time_audio)))

signal_array = np.frombuffer(signal_wave, dtype=np.int16)

print("Size of Frames " + str(len(signal_array)))

times = np.linspace(0, np.ceil(time_audio), num=n_samples)

plt.figure(figsize=(15, 5))
plt.plot(times, signal_array)
plt.title("Audio Signal of" + fileName)
plt.ylabel("Signal Wave")
plt.xlabel("Time (s)")
plt.xlim(0, time_audio)
plt.show()