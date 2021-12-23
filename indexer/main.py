import time
from os import path
from storage import Storage
from utils import create_final_dictionary
from repository import Repository
from worker import IndexerWorker
from multiprocessing import Manager, Process, Queue

ROOT = path.join(path.dirname(__file__), 'example repository')

manager = Manager()
doc_queue = Queue()
words = manager.list()
finished = manager.Event()

repo = Repository(ROOT, doc_queue, finished)
repo_worker = Process(target=repo.load, args=[])

indexer_worker_1 = IndexerWorker(doc_queue, finished, words)
indexer_worker_2 = IndexerWorker(doc_queue, finished, words)
indexer_worker_3 = IndexerWorker(doc_queue, finished, words)
indexer_worker_4 = IndexerWorker(doc_queue, finished, words)

if __name__ == '__main__':
    start = time.time()

    repo_worker.start()
    
    indexer_worker_1.start()
    indexer_worker_2.start()
    indexer_worker_3.start()
    indexer_worker_4.start()

    repo_worker.join()

    indexer_worker_1.join()

    indexer_worker_2.join()

    indexer_worker_3.join()

    indexer_worker_4.join()

    with Storage() as db:
        db.save_words(words)

    print(time.time() - start)
    print('****************\n')
