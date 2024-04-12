import re

import nltk
import pymorphy2
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

from text_tagging_model.processing.normalizers.base_normalizer import BaseNormalizer
from text_tagging_model.processing.utils import languages


class NounsKeeper(BaseNormalizer):
    def __init__(self, language: str, keep_latn: bool = False) -> None:
        if language not in languages:
            raise ValueError(f"Wrong language!\nAvailable languages: {languages.keys()}")

        self.morph = pymorphy2.MorphAnalyzer(lang=languages[language])
        self.keep_latn = keep_latn

    def normalize(self, text: str) -> str:
        nouns = []
        for word in text.split():
            p = self.morph.parse(str(word))[0]
            if p.tag.POS == "NOUN":
                nouns.append(p.normal_form)

            if self.keep_latn and "LATN" in p.tag:
                nouns.append(p.normal_form)

        return " ".join(nouns)


class BilingualTextNormalizer(BaseNormalizer):
    def __init__(self):
        nltk.download("averaged_perceptron_tagger")
        nltk.download("wordnet")
        self.morph = pymorphy2.MorphAnalyzer()
        self.lemmatizer = WordNetLemmatizer()

    @staticmethod
    def get_wordnet_pos(tag):
        tag_dict = {"N": wordnet.NOUN}
        return tag_dict.get(tag[0].upper(), wordnet.NOUN)

    def is_noun(self, word, lang="en"):
        if lang == "ru":
            parsed_word = self.morph.parse(word)[0]
            return "NOUN" in parsed_word.tag
        else:
            pos = nltk.pos_tag([word])[0][1]
            return pos.startswith("N")

    def lemmatize_word(self, word, lang="en"):
        if lang == "ru":
            return self.morph.parse(word)[0].normal_form
        else:
            pos = self.get_wordnet_pos(nltk.pos_tag([word])[0][1])
            return self.lemmatizer.lemmatize(word, pos)

    def normalize(self, key_phrases):
        normalized_phrases = []
        for phrase in key_phrases:
            words = re.findall(r'\w+', phrase.lower())
            words_en = [word for word in words if re.match(r"[a-z]+", word, re.IGNORECASE)]
            words_ru = [word for word in words if re.match(r"[а-яё]+", word, re.IGNORECASE)]

            all_en_nouns = all(self.is_noun(word, "en") for word in words_en) if words_en else True
            all_ru_nouns = all(self.is_noun(word, "ru") for word in words_ru) if words_ru else True

            if all_en_nouns and all_ru_nouns:
                lemmatized_words = [
                    self.lemmatize_word(word, "en") if word in words_en else self.lemmatize_word(
                        word, "ru")
                    for word in words
                ]
                normalized_phrases.append(" ".join(lemmatized_words))

        return normalized_phrases
