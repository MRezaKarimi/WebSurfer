from django.apps import AppConfig
from django.core.cache import cache
from .storage import Storage


class QueryConfig(AppConfig):
    name = 'query'

    def ready(self):
        """
        load words when app starts
        """
        with Storage() as db:
            cache.set('words', db.load_words(), None)
            cache.set('total_docs', db.get_docs_count(), None)