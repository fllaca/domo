# -*- coding: utf-8 -*-
import audio_inputs
"""
Human dialog functions
"""

class DialogManager(object):
    def __init__(self, stt=None, tts=None):
        if stt is None or tts is None:
            raise ValueError("stt and tts are mandatory arguments")
        self.stt = stt
        self.tts = tts

    def ask_confirmation(self):
        confirm = self.prompt("¿es correcto?")
        print "Confirmation: ", confirm
        return confirm != None and confirm.strip() == "correcto"

    def prompt(self, question):
        self.tts.say(question)
        audio_inputs.listen("question.wav")
        return self.stt.process_file("question.wav")

    def say(self, text):
        self.tts.say(text)
