import os
from document import Document
from xml.etree import ElementTree
from queue import Queue

class Repository:

    def __init__(self, root: str, doc_queue: Queue, finished):
        self.root = root
        self.doc_queue = doc_queue
        self.finished = finished
        self.visited_docs = set()

    def load(self):
        """
        Start from root, walk through subfolders nad read xml files
        """
        for root, _, files in os.walk(self.root):
            if files:
                for xml_file in files:
                    file_path = root + '/' + xml_file
                    self.parse(file_path)
                    # with open(file_path, 'r') as f:
                    #     self.parse_xml(f.read())
        self.finished.set()

    def parse_xml(self, xml_content: str):
        """
        Get content of xml file, parse it, exctract docs, create doc objects and put them in doc queue
        """
        doc_root = ElementTree.fromstring(xml_content)
        for doc in doc_root.findall('DOC'):
            self.doc_queue.put(Document(doc.find('DOCID').text, doc.find('URL').text, doc.find('HTML').text))


    def parse(self, file_path: str):
        """
        Get xml filename, iter over it, exctract docs, create doc objects and put them in doc queue
        """
        for event, element in ElementTree.iterparse(file_path):
            if event=='end':
                if element.tag == 'DOC':
                    doc = element
                    if doc.find('DOCID').text not in self.visited_docs:
                        self.doc_queue.put(Document(doc.find('DOCID').text, doc.find('URL').text, doc.find('HTML').text))
                        self.visited_docs.add(doc.find('DOCID').text)

# r = Repository('/home/mohammad/Python Projects/search engines/hw2/Repository', [])
# r.load()