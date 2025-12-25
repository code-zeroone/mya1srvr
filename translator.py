from deep_translator import GoogleTranslator

class Translator:
    def __init__(self, cfg):
        self.enabled = cfg["translate"]

    def translate(self, text, src, target):
        try:
            return GoogleTranslator(source=src, target=target).translate(text)
        except:
            return text
