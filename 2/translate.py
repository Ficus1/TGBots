import googletrans
from googletrans import Translator
translator = Translator()


def translate_text(text, language):
    result = translator.translate(text, dest=language)
    return result.text


languages_list = googletrans.LANGUAGES