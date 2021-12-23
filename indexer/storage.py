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

    def save_docs(self, docs_list: list):
        self.client[self.DB_NAME][self.DOCS_COLL].insert_many(docs_list, False)
    
    def save_words(self, words_list: list):
        first_set: set = words_list.pop()
        total_words_set = first_set.union(*words_list)
        self.client[self.DB_NAME][self.WORDS_COLL].insert_one({'words': list(total_words_set)})

    def save_title_dict(self, dic_list: list):
        for dic in dic_list:
            word = dic['word']
            self.client[self.DB_NAME][self.TITLE_DICT_COLL].update_one({'word': word}, {'$set': dic}, upsert=True)

    def save_body_dict(self, dic_list: list):
        for dic in dic_list:
            word = dic['word']
            self.client[self.DB_NAME][self.BODY_DICT_COLL].update_one({'word': word}, {'$set': dic}, upsert=True)

    def load_words(self, words_list: set)-> set:
        self.client[self.DB_NAME][self.WORDS_COLL].find([])

    def load_title_dicts(self, words: list):
        self.client[self.DB_NAME][self.TITLE_DICT_COLL].find([])
        
    def load_body_dicts(self, words: list):
        self.client[self.DB_NAME][self.BODY_DICT_COLL].find([])