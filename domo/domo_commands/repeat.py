# -*- coding: utf-8 -*-
"""
Simple command that just repeats what the user says
"""
from domo.dialogs import DialogManager

class RepeatCommand(object):

    def __init__(self, tts, stt):
        self.stt = stt
        self.tts = tts
        
        self.dialogs = DialogManager(stt=self.stt, tts=self.tts)
    
    def run(self):
        text = self.dialogs.prompt("Simón dice")
        self.dialogs.say(text)
