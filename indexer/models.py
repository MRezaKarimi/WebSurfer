from mongoengine import *


class Doc(EmbeddedDocument):
    id = StringField(regex=r'\d+')
    positions = ListField(IntField())


class Term(Document):
    term = StringField()
    zone = StringField()
    docs = ListField(EmbeddedDocumentField(Doc))