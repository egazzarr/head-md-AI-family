import os
import subprocess
from pydub import AudioSegment
import tempfile
import sys
import termios
import tty

recordings_folder = "/home/pc/Desktop/family/robot1/recordings"

key_map = {
    "0": "humming_default.WAV",
    "1": "ah.WAV",
    "2": "aah.WAV",
    "3": "aaah_rupture.WAV",
    "4": "OH.WAV",
    "5": "oooh_manners.WAV",
    "6": "ooooooh_surprise.WAV",
    "7": "hhmm_affirmation.WAV",
    "8": "olalaaaa.WAV",
    "9": "ssshh.WAV",
    "q": "gnam.WAV",
    "w": "bouche.WAV",
    "e": "slurp.WAV",
    "p": "mumble1.WAV",
    "l": "mumble2.WAV"
}

alsa_device = "hw:2,0"
current_process = None


def play_sound(file_path):
    global current_process

    # Stop previous sound
    if current_process and current_process.poll() is None:
        current_process.terminate()

    sound = AudioSegment.from_file(file_path)
    sound = sound.fade_in(200).fade_out(200)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        temp_file_path = tmp.name
        sound.export(temp_file_path, format="wav")

    env = os.environ.copy()
    env["AUDIODEV"] = alsa_device

    current_process = subprocess.Popen(
        ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", temp_file_path],
        env=env
    )


def getch():
    """Read single key without Enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch


print("Press keys 0-9, q, w, e, p, l to play sounds. Ctrl+C to exit.")

try:
    while True:
        key = getch()

        # Detect Ctrl+C directly
        if key == "\x03":
            raise KeyboardInterrupt

        if key in key_map:
            file_path = os.path.join(recordings_folder, key_map[key])

            if os.path.exists(file_path):
                print(f"Playing: {key_map[key]}")
                play_sound(file_path)
            else:
                print(f"Missing file: {file_path}")

except KeyboardInterrupt:
    print("\nStopping program...")

    if current_process and current_process.poll() is None:
        current_process.terminate()

    print("Exited cleanly.")
