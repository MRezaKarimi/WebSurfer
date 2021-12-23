from pymongo import MongoClient

class Document:

    def __init__(self, id: int, url: str, content: str):
        self.id = id
        self.url = url
        self.content = content
        self.title = None
        self.body = None
    
    def to_dict(self):
        """
        Convert document to dict object
        """
        return {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'body': self.body
        }
