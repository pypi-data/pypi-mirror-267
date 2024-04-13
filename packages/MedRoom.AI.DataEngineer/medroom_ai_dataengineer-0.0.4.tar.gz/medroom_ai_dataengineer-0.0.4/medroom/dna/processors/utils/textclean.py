import re
import string

import spacy
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize
from unidecode import unidecode


class TextPreprocessor:
    RE_PUNCTUATION = re.compile(rf"[{string.punctuation}]")
    RE_DIGITS = re.compile(r"\d+")
    STOP_WORDS = set(stopwords.words("portuguese"))

    def __init__(
        self, remove_accents=True, remove_digits=True, use_lemmatization=True, use_stemming=False, remove_stopwords=True
    ):
        self.remove_accents = remove_accents
        self.remove_digits = remove_digits
        self.use_lemmatization = use_lemmatization
        self.use_stemming = use_stemming
        self.remove_stopwords = remove_stopwords
        self.stemmer = RSLPStemmer() if use_stemming else None
        self.nlp = spacy.load("pt_core_news_sm") if use_lemmatization else None

    @staticmethod
    def remove_consecutive_duplicates(tokens):
        return [t for i, t in enumerate(tokens) if i == 0 or t != tokens[i - 1]]

    def preprocess_text(self, text):
        text = text.lower()
        text = self.RE_PUNCTUATION.sub(" ", text)
        if self.remove_digits:
            text = self.RE_DIGITS.sub("", text)

        tokens = word_tokenize(text)

        result_tokens = []
        for word in tokens:
            if self.remove_stopwords and word in self.STOP_WORDS:
                continue
            if self.use_lemmatization:
                doc = self.nlp(word)
                word = doc[0].lemma_ if doc else word
            if self.use_stemming:
                word = self.stemmer.stem(word)
            if self.remove_accents:
                word = unidecode(word)
            result_tokens.append(word)

        result_tokens = self.remove_consecutive_duplicates(result_tokens)
        return " ".join(result_tokens)
