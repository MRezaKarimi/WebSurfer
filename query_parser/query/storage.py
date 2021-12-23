from pymongo import MongoClient


class Storage:
    
    def __init__(self):
        self.DB_NAME = 'hw'
        self.TITLE_DICT_COLL = 'title_dict'
        self.BODY_DICT_COLL = 'body_dict'
        self.WORDS_COLL = 'words'
        self.DOCS_COLL = 'docs'
        
    def __enter__(self):
        self.client = MongoClient()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.client.close()

    def load_docs(self, doc_id_list: list):
        return self.client[self.DB_NAME][self.DOCS_COLL].find({'id': {'$in': doc_id_list}})

    def load_words(self)-> set:
        return set(self.client[self.DB_NAME][self.WORDS_COLL].find_one()['words'])

    def get_docs_count(self)-> int:
        return self.client[self.DB_NAME][self.DOCS_COLL].count_documents({})

    def load_title_dicts(self, words: list):
        return self.client[self.DB_NAME][self.TITLE_DICT_COLL].find({'word': {'$in': words}})
        
    def load_body_dicts(self, words: list):
        return self.client[self.DB_NAME][self.BODY_DICT_COLL].find({'word': {'$in': words}})
