# -*- coding: utf-8 -*-
"""
Application entrypoint
"""
import sys
import os
import getopt
import domo.global_vars
import domo.audio_inputs
import domo.config as configuration
from domo.stt.pocket_sphinx import PocketSphinxSTT
from domo.stt.google import GoogleSTT
from domo.tts.pico2wave import Pico2WaveTTS
from domo.tts.google import GoogleTTS
from domo.domo_commands.repeat import RepeatCommand
from domo.domo_commands.learn import LearnCommand

def usage():
    """
    Show help
    """
    print("""
    parameters:
    -c (--config) yaml configuration file
    """)

def defaults():
    """
    Set default values for arguments
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    domo.global_vars.configfile = os.path.join(dir_path, "config.yaml")


def get_args(argv):
    """
    Application entrypoint
    """
    try:
        opts, args = getopt.getopt(argv, "hc:", ["help", "config="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, value in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-c", "--config"):
            domo.global_vars.configfile = value
    print("Config File", domo.global_vars.configfile)

def handle_keyword(text):
    print("*****************")
    print("keyword Detected:", text)
    print("*****************")
    tts = Pico2WaveTTS(domo.global_vars.config["text_to_speech"]["pico2wave"])
    #tts = GoogleTTS(global_vars.config["text_to_speech"]["google"])

    commands_stt = PocketSphinxSTT(domo.global_vars.config["speech_to_text"]["commands"])
    google_stt = GoogleSTT(domo.global_vars.config["speech_to_text"]["google"])
    # tts.say("¿sí?")
    # learn_cmd = LearnCommand(
    #     global_vars.config["speech_to_text"]["learning"],
    #     tts,
    #     commands_stt,
    #     google_stt
    # )
    # learn_cmd.run()
    repeat_cmd = RepeatCommand(tts, commands_stt)
    repeat_cmd.run()


def main():
    defaults()
    get_args(sys.argv[1:])

    # Init configuration
    domo.global_vars.config = configuration.Config()

    #print global_vars.config
    keyword_stt = PocketSphinxSTT(domo.global_vars.config["speech_to_text"]["keyword"])
    stream = domo.audio_inputs.get_mic_stream()
    keyword_stt.process_stream(stream,handle_keyword)
