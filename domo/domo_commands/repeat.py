# -*- coding: utf-8 -*-
import time
import os
import audio_inputs
from dialogs import DialogManager

class RepeatCommand(object):

    def __init__(self, tts, stt):
        self.stt = stt
        self.tts = tts
        
        self.dialogs = DialogManager(stt=self.stt, tts=self.tts)
    
    def run(self):
        text = self.dialogs.prompt("Simón dice")
        self.dialogs.say(text)
