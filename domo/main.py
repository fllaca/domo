# -*- coding: utf-8 -*-
"""
Application entrypoint
"""
import sys
import os
import getopt
import global_vars
import audio_inputs
import config as configuration
from stt.pocket_sphinx import PocketSphinxSTT
from stt.google import GoogleSTT
from tts.pico2wave import Pico2WaveTTS
from tts.google import GoogleTTS
import domo_commands

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
    global_vars.configfile = os.path.join(dir_path, "config.yaml")


def main(argv):
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
            global_vars.configfile = value
    print("Config File", global_vars.configfile)

def handle_keyword(text):
    print("*****************")
    print("keyword Detected!")
    print("*****************")
    tts = Pico2WaveTTS(global_vars.config["text_to_speech"]["pico2wave"])
    #tts = GoogleTTS(global_vars.config["text_to_speech"]["google"])

    commands_stt = PocketSphinxSTT(global_vars.config["speech_to_text"]["commands"])
    google_stt = GoogleSTT(global_vars.config["speech_to_text"]["google"])
    # tts.say("¿sí?")
    # learn_cmd = domo_commands.learn.LearnCommand(
    #     global_vars.config["speech_to_text"]["learning"],
    #     tts,
    #     commands_stt,
    #     google_stt
    # )
    # learn_cmd.run()
    repeat_cmd = domo_commands.repeat.RepeatCommand(tts, commands_stt)
    repeat_cmd.run()


if __name__ == "__main__":
    defaults()
    main(sys.argv[1:])

    # Init configuration
    global_vars.config = configuration.Config()

    #print global_vars.config
    keyword_stt = PocketSphinxSTT(global_vars.config["speech_to_text"]["keyword"])
    stream = audio_inputs.get_mic_stream()
    keyword_stt.process_stream(stream,handle_keyword)
