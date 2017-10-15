# -*- coding: utf-8 -*-
import time
import os
import audio_inputs
from dialogs import DialogManager

class LearnCommand(object):

    def __init__(self, config, tts, training_stt, corrector_stt):
        self.training_stt = training_stt
        self.corrector_stt = corrector_stt
        self.tts = tts
        self.audio_folder = config["audio_folder"]
        self.transcription_file = config["transcription_file"]
        self.fileids_file = config["fileids_file"]
        self.learning = config["enabled"] if "enabled" in config else False
        self.dialogs = DialogManager(stt=self.corrector_stt, tts=self.tts)
    
    def run(self):
        audio_id=time.strftime("%Y%m%d-%H%M%S")
        filename="audio-" + audio_id
        filename_ext= self.audio_folder + "/" + filename + ".wav"
        audio_inputs.listen(filename_ext)

        text = self.training_stt.process_file(filename_ext)
        correction = text

        self.tts.say(text)

        if self.dialogs.ask_confirmation():
            self.tts.say("genial")
        else:
            self.tts.say("jopetas")
            correction = self.corrector_stt.process_file(filename_ext)
            self.tts.say(u"correción")
            self.tts.say(correction)

        if self.learning:
            self.save_transcription(filename, correction)
        else:
            os.remove(filename_ext)

    def save_transcription(self, filename, text):
        """
        Saves the transcription in a .transcription file
        Args:
            filename: the name of the audio file (without extension)
            text: the transcripted text
        """
        print "Saving transcription"
        with open(self.transcription_file, 'a') as file:
            file.writelines('\n<s>' + text + '</s> (' + filename +')')
        with open(self.fileids_file, 'a') as file:
            file.writelines("\n" + filename)
