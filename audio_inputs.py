import pyaudio

# Create PyAudio object
p = pyaudio.PyAudio()

# Get the number of audio devices
num_devices = p.get_device_count()

print("Available audio devices:")

# Iterate over audio devices
for i in range(num_devices):
    device_info = p.get_device_info_by_index(i)
    device_name = device_info['name']
    device_input_channels = device_info['maxInputChannels']

    # Only print devices with input channels
    if device_input_channels > 0:
        print(f"  Device {i}: {device_name}")
        print(f"    Input channels: {device_input_channels}")


# Get default input device info
default_device_info = p.get_default_input_device_info()
default_device_name = default_device_info['index']

# Display default input device name
print(f"Default input device: {default_device_name}")

# Terminate PyAudio
p.terminate()
