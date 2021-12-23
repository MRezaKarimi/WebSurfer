import re
from document import Document

class Parser:

    def parse(self, doc: Document):
        """
        Get a document instance and parse it (exctract title and body from content)
        """
        self.content = doc.content
        del doc.content
        doc.title = self.get_title()
        doc.body = self.get_body()

    def get_title(self):
        """
        Exctract title from doc
        """
        matches = re.search(r"<title>(.+)<\/title>", self.content, re.DOTALL | re.IGNORECASE)
        try:
            title = matches.group(1)
        except AttributeError:
            return None
        return title

    def get_body(self):
        """
        Exctract body from doc: remove <title> tag and return ramaining
        """
        body = re.sub(r"<title>.*<\/title>", "", self.content, 0, re.DOTALL)
        return body