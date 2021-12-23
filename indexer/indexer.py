import re
import hazm
from document import Document
from normalizer import Normalizer
from parser import Parser

class Indexer:

    def __init__(self):
        self.words = set()
        self.titles_dictionary = {}
        self.bodies_dictionary = {}
        self.parser = Parser()
        self.normalizer = Normalizer()
        self.stopwords = set(hazm.utils.stopwords_list())
        self.invalid_chars = re.compile(r"\\|\/|\?|\.|,|\(|\)|\[|\]|؟|،|!|–|-|!|_|ـ|:|<|>|»|«|\*")
        self.tokenizer = hazm.WordTokenizer(replace_emails=True, replace_numbers=True, replace_links=True).tokenize

    def index(self, doc: Document):
        """
        Get doc, tokenize it's content and create dictionary
        """
        self.normalizer.normalize(doc)
        self.parser.parse(doc)

        # Check if document has title
        title_dic = []
        if doc.title is not None:
            
            title_words = self.validate(self.tokenizer(doc.title))
            for word in set(title_words):
                indices = [i for i, x in enumerate(title_words) if x == word]
                title_dic.append({
                    'word': word,
                    str(doc.id): indices
                    })
                self.words.add(word)

        body_words = self.validate(self.tokenizer(doc.body))
        body_dic = []
        for word in set(body_words):
            indices = [i for i, x in enumerate(body_words) if x == word]
            body_dic.append({
                'word': word,
                doc.id: indices
                })
            self.words.add(word)

        return title_dic, body_dic

    def validate(self, words_list: list)-> list:
        """
        Get word list and remove invalid chars
        """
        validated = []

        for word in words_list:
            if word not in self.stopwords:
                if not word.startswith(('NUM', 'EMAIL', 'LINK')):
                    if not self.invalid_chars.match(word):
                        validated.append(word)
        return validated
