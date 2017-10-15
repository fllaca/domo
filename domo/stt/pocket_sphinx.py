"""
Uses PocketSphinx to extract text from Audio
"""
from pocketsphinx.pocketsphinx import Decoder

class PocketSphinxSTT(object):
    """
    Uses PocketSphinx to extract text from Audio
    """
    config = None
    def __init__(self, config):
        self.config = Decoder.default_config()
        for key in config:
            self.config.set_string("-" + key, config[key])


    def process_file(self, audiofile):
        """
        processes audio file and returns the text
        """
        with open(audiofile, 'rb') as audiofile:
            decoder = Decoder(self.config)
            decoder.start_utt()

            while True:
                buf = audiofile.read(1024)
                if buf:
                    decoder.process_raw(buf, False, False)
                else:
                    break
            decoder.end_utt()

            hyp = decoder.hyp()
            print "Hyp:", hyp

            if hyp != None:
                print "Hyp Score", (hyp.prob, hyp.best_score)
                average_score = 0
                seg_count = 0
                for seg in decoder.seg():
                    if seg.word != "<sil>":
                        seg_count += 1
                        average_score += seg.ascore
                        print (seg.word, seg.ascore, seg.lscore)

                print "hyp:", hyp.hypstr
                print average_score/seg_count
                return hyp.hypstr
        return None

    def process_stream(self, stream, callback):
        """
        Processes continuosly an audio stream and
        trigger the callback when text is detected
        """
        decoder = Decoder(self.config)
        decoder.start_utt()
        while True:
            buf = stream.read(1024)
            decoder.process_raw(buf, False, False)
            if decoder.hyp() is not None and decoder.hyp().hypstr is not None:
                decoder.end_utt()
                callback(decoder.hyp().hypstr)
                decoder.start_utt()
