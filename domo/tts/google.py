"""
Text to speech with Google API
"""
import sys
from gtts import gTTS
from playsound import playsound

reload(sys)
sys.setdefaultencoding("utf-8")

TMP_AUDIO_FILE = "/tmp/txt.mp3"

class GoogleTTS(object):
    """
    Text to speech with Google API
    """
    def __init__(self, config):
        self.lang = config["lang"]

    def say(self, txt):
        """
        Text to speech with Google API
        """
        if txt != "" or txt is not None:
            tts = gTTS(text=txt, lang=self.lang)
            tts.save(TMP_AUDIO_FILE)
            playsound(TMP_AUDIO_FILE)
