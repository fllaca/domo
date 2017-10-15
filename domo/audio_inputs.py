"""
Tools to get audio inputs
"""
import pyaudio
import speech_recognition as sr

def get_mic_stream():
    """
    Gets a audio stream from mic
    """
    p = pyaudio.PyAudio()
    return p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True
        )

def listen(audio_filename):
    """
    Get audio from mic and stores it in a wav file
    """
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=16000) as source:
        print("Say something!")
        audio = r.listen(source)
    # write audio to a WAV file
    with open(audio_filename, "wb") as f:
        f.write(audio.get_wav_data())

def list_devices():
    """
    List in console audio input devices
    """
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print(
                "Input Device id ",
                i,
                " - ",
                p.get_device_info_by_host_api_device_index(0, i).get('name')
            )
