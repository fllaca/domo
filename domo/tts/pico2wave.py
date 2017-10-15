"""
Text to speech with commandline pico2wave tool
"""
import os
import subprocess
import tempfile

class Pico2WaveTTS(object):
    """
    Text to speech with commandline pico2wave tool
    """
    def __init__(self, config):
        self.lang = config["lang"]

    def play_file(self, path):
        cmd = ['aplay', path]
        subprocess.call(cmd)

    def say(self, phrase):
        if phrase is None:
            return
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            fname = f.name

        cmd = ['pico2wave', '-w', fname, '-l', self.lang, phrase.lower()]
                                            # Ensure lowercase because consecutive uppercases
                                            # sometimes cause it to spell out the letters.
        subprocess.call(cmd)

        self.play_file(fname)
        os.remove(fname)
