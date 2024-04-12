import re

import nltk
from nltk.corpus import stopwords

from text_tagging_model.processing.normalizers.base_normalizer import BaseNormalizer
from text_tagging_model.processing.utils import languages


class StopwordsDeleter(BaseNormalizer):
    def __init__(self, language: str, drop_english=False, remove_non_alpha=True) -> None:
        if language not in languages:
            raise ValueError(f"Wrong language!\nAvailable languages: {languages.keys()}")

        nltk.download("stopwords")
        self.stop_words = set(stopwords.words(language))

        if drop_english:
            self.stop_words = self.stop_words.union(set(stopwords.words("english")))

        self.remove_non_alpha = remove_non_alpha

    def normalize(self, text: str) -> str:
        if self.remove_non_alpha:
            text = re.sub(r"[^a-zA-Zа-яА-Я\s]", " ", text)

        words = text.split()

        clear_text = [word for word in words if word.lower() not in self.stop_words and word != ""]

        return " ".join(clear_text)
