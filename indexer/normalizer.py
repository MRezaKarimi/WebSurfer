import re
import html
import hazm
from document import Document
from bleach import clean
from xml.sax import saxutils

class Normalizer:

    def __init__(self):
        """
        docstring
        """
        self.compile_regex()
        self.hazm_normalizer = hazm.Normalizer().normalize

    def compile_regex(self):
        """
        Compile regex for later use
        """
        self.__scripts_regex = re.compile(r"(<script.*?>.*?</script>)", re.IGNORECASE | re.DOTALL | re.MULTILINE)
        self.__styles_regex = re.compile(r"(<style.*?>.*?</style>)", re.IGNORECASE | re.DOTALL | re.MULTILINE)
        self.__useless_regex = re.compile(r"-|\d|\.\.+|٬")
        self.__whitespace_regex = re.compile(r"\s+")
    
    def normalize(self, doc: Document):
        self.content = doc.content
        self.__unescape()
        self.__remove_scripts()
        self.__remove_styles()
        self.__remove_tags()
        self.__remove_useless_chars()
        self.content = self.hazm_normalizer(self.content)
        self.__remove_spaces()
        doc.content = self.content

    def __unescape(self):
        """
        Unescape the escaped characters
        """
        self.content = html.unescape(self.content)

    def __remove_scripts(self):
        """
        Remove <script> tags using regex because bleach somtimes does not remove them
        """
        self.content = self.__scripts_regex.sub("", self.content, 0)

    def __remove_styles(self):
        """
        Remove <style> tags using regex because bleach somtimes does not remove them
        """
        self.content = self.__styles_regex.sub("", self.content, 0)

    def __remove_tags(self):
        """
        Remove all HTML tags except <title> using bleach
        """
        self.content = clean(self.content, tags=['title', 'body'], attributes={}, styles=[], protocols=[], strip=True, strip_comments=True)

    def __remove_useless_chars(self):
        """
        Remove '-' and digits and …
        """
        self.content = self.__useless_regex.sub(" ", self.content, 0)

    def __remove_spaces(self):
        """
        Remove additional whitespaces
        """
        self.content = self.__whitespace_regex.sub(" ", self.content, 0)
