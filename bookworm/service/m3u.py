import signal
import subprocess


class M3UPlayer:
    def __init__(self):
        self.process = None

    def play(self, m3u_path):
        """Starts playing the M3U playlist."""
        self.stop()  # Stop any existing playback before starting a new one
        self.process = subprocess.Popen(
            ["cvlc", "--no-video", "--quiet", m3u_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def stop(self):
        """Stops the currently playing playlist."""
        if self.process:
            self.process.send_signal(signal.SIGTERM)
            self.process.wait()
            self.process = None
