"""
Uses Google Speech Cloud API to extract text from Audio
"""
import speech_recognition as sr

CONFIG_KEY_LANG = "lang"
CONFIG_KEY_API_KEY = "api_key"

class GoogleSTT(object):
    """
    Uses Google Speech Cloud API to extract text from Audio
    """
    def __init__(self, config):
        self.language = config.get(CONFIG_KEY_LANG, "es-ES")
        self.key = config.get(CONFIG_KEY_API_KEY, None)


    def process_file(self, audiofile):
        """
        processes audio file and returns the text
        """
        """
        Uses Google Cloud Speech API
        """
        recognizer = sr.Recognizer()
        with sr.AudioFile(audiofile) as source:
            audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language=self.language, key=self.key)
            return text
        except sr.UnknownValueError:
            print "Sphinx could not understand audio"
        except sr.RequestError as error:
            print "Sphinx error; {0}".format(error)
        return None
