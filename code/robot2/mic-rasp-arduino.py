import numpy as np
import serial
import time
import sounddevice as sd

# ---------------- Serial setup ----------------
arduino = serial.Serial(
    '/dev/ttyACM0',
    9600,
    timeout=1
)
arduino.setDTR(False)  # Prevent Arduino auto-reset
time.sleep(2)  # allow Arduino to initialize

# ---------------- Audio setup ----------------
def find_input_device(keyword="USB"):
    devices = sd.query_devices()
    for i, dev in enumerate(devices):
        if dev['max_input_channels'] > 0 and keyword.lower() in dev['name'].lower():
            print(f"Using audio device {i}: {dev['name']}")
            return i
    raise RuntimeError("No suitable input device found")

DEVICE = find_input_device()

CHANNELS = 1
SAMPLERATE = 48000
SEND_INTERVAL = 0.5  # seconds between serial sends

# ---------------- Globals ----------------
last_chunk = None

# ---------------- Utilities ----------------
def rms_to_percent(data):
    rms = np.sqrt(np.mean(np.square(data)))
    percent = min(int(rms * 1000), 100)  # scale RMS to 0–100
    return percent

# ---------------- Audio callback ----------------
def audio_callback(indata, frames, time_info, status):
    global last_chunk
    last_chunk = indata[:, 0].copy()  # copy the first channel

# ---------------- Main loop ----------------
with sd.InputStream(device=DEVICE, channels=CHANNELS,
                    samplerate=SAMPLERATE,
                    callback=audio_callback):
    print("Sending detected volume to Arduino (Ctrl+C to stop)...")
    try:
        last_send_time = 0
        while True:
            now = time.time()
            if last_chunk is not None and now - last_send_time >= SEND_INTERVAL:
                volume_percent = rms_to_percent(last_chunk)
                try:
                    arduino.write(f"{volume_percent}\n".encode())
                    print(f"{time.strftime('%H:%M:%S')} - Volume sent: {volume_percent}%")
                except serial.SerialException:
                    print("Error: Arduino disconnected")
                    break
                last_chunk = None
                last_send_time = now
            time.sleep(0.05)  # small sleep to reduce CPU usage
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        arduino.close()
        print("Serial port closed.")
