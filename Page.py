from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re


class Page:
    def __init__(self, session, book):
        self.SESSION = session
        self.url = f'https://www.amazon.com.br/dp/{book}/'
        self.html = self.getHTML()

    def getHTML(self):
        html = self.SESSION.get(self.url)
        soup = BeautifulSoup(html.text, 'html.parser')
        error = soup.find(string=re.compile(r'Desculpe|Algo deu errado'))
        while error != None:
            html = self.SESSION.get(self.url)
            soup = BeautifulSoup(html.text, 'html.parser')
            error = soup.find(string=re.compile(r'Desculpe|Algo deu errado'))
            print(error)
        return soup
    
    def extractTitle(self):
        return self.html.find('span',{'id':'productTitle'})
    
    def extractAuthors(self):
        info = self.html.find('div', {'id':'bylineInfo'})
        return [author for author in info.findAll('a')]

if __name__ == '__main__':
    pag = Page('8555341620')
    print(pag.extractTitle())
    print(pag.extractAuthors())