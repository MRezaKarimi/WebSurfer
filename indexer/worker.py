from indexer import Indexer
from queue import Empty
from storage import Storage
from document import Document
from multiprocessing import Process, Queue

class IndexerWorker(Process):

    def __init__(self, doc_queue: Queue, finished, words: list):
        super().__init__()
        self.doc_queue = doc_queue
        self.finished = finished
        self.indexer = Indexer()
        self.doc_list = []
        self.words = words

    def run(self):
        with Storage() as db:
            while not (self.finished.is_set() and self.doc_queue.empty()):
                try:
                    doc: Document = self.doc_queue.get(timeout=5)
                    title_dic, body_dic = self.indexer.index(doc)
                    self.doc_list.append(doc.to_dict())
                    db.save_title_dict(title_dic)
                    db.save_body_dict(body_dic)
                except Empty:
                    pass

            db.save_docs(self.doc_list)
                
        self.words.append(self.indexer.words)
        
