from abc import abstractclassmethod, ABC
from bs4 import BeautifulSoup
from requests_html import HTMLSession

class Book(ABC):
    SESSION = None

    def __init__(self, url):
        self.url = url
        self.pageBook = self.getHTML(self.url)
    
    @classmethod
    def setSession(cls, session):
        cls.SESSION = session
    
    @classmethod
    def getHTML(cls, url):
        html = cls.SESSION.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        return soup

    @abstractclassmethod
    def getTitle(self):
        pass

 #   @abstractclassmethod
 #   def getNPages(self):
 #       pass
 #
 #   @abstractclassmethod
 #   def getISBN(self):
 #       pass

 #   @abstractclassmethod
 #   def getResume(self):
 #       pass

 #   @abstractclassmethod
 #   def getKind(self):
 #       pass

 #   @abstractclassmethod
 #   def getPrice(self):
 #       pass


class Company(ABC):
    def __init__(self, url, company=None):
        self.SESSION = HTMLSession()
        self.url = url
        self.company = company
        self.interation = 1
    
    def setInteration(self, interation):
        self.interation = interation
    
    def getHTML(self, url):
        html = self.SESSION.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        return soup
    
    def getCompany(self):
        return self.company
    
    @abstractclassmethod
    def getUrlsBooksInPage(self, urlPage):
        pass 

    @abstractclassmethod
    def nextPage(self):
        pass 

    



    