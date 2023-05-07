from requests_html import HTMLSession
from bs4 import BeautifulSoup
import json
import re

from PageBook import PageBook
from DataBaseConection import DB


class ExtractPages:
    def __init__(self):
        self.SESSION = HTMLSession()
        self.URL_AMAZON = 'https://www.amazon.com.br'
        self.DEPARTMENTS = {}
    
    def getHTML(self, url):
        html = self.SESSION.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        return soup
    
    def getDepartmentAndHref(self, li):
        try:
            href = li.find('a').attrs['href']
            department = li.find('a').text.strip()
        except AttributeError:
            print('attribute not find')
            href = None
            department = None
        return [department, href]

    def getBookAndHref(self, card):
        try:
            href = card.attrs['href']
            titleOfBook = card.find('span').text.strip()
        except AttributeError:
            print('attribute not find')
            href = None
            titleOfBook = None
        return (titleOfBook, href)
    
    def extractIdNumberHref(self, href):
        com = re.compile(r'.{3}dp/[\d\w]{10,}|&node=[\d\w]{10,}|.{3}%[\d\w]{2}[\d\w]{10,}')
        try:
            extracted = re.findall(com, href)[0][6:]
            return extracted
        except IndexError:
            print(href) 
    
    def getAllDepartments(self):
        url_books = self.URL_AMAZON + '/gp/browse.html?node=6740748011'
        soup = self.getHTML(url_books)
        div_refinements = soup.find('div',{'id':'s-refinements'})
        div_department = div_refinements.find('span',string='Livros').parent.parent.parent
        li_links = div_department.findAll('li')
        for li in li_links[1:]:
            dp_href = self.getDepartmentAndHref(li)
            self.DEPARTMENTS[dp_href[0]] = self.extractIdNumberHref(dp_href[1])
        with open('departments.json', 'w', encoding='UTF-8') as file:
            json.dump(self.DEPARTMENTS, file, ensure_ascii=False)
    
    def saveBooks(self, dic):
        with open('books.json', 'a') as file:
            file.write(json.dumps(dic, ensure_ascii=False))
            file.write(',\n')

    def getBooksByDepartmentByPage(self, department_node, pag=1):
        books = []
        url_pag_books = f'{self.URL_AMAZON}/s?rh=n%3A{department_node}&fs=true&page={pag}'
        articles = []
        while articles == []:
            soup = self.getHTML(url_pag_books)
            articles = soup.select('h2 a')
        for card in articles:
            bk_href = self.getBookAndHref(card)
            if bk_href[1] != None:
                idBook = self.extractIdNumberHref(bk_href[1])
                book = PageBook(self.SESSION, idBook)
                books.append(book)
        return books

if __name__ == '__main__':

    extrator = ExtractPages()
    extrator.getBooksByDepartmentByPage('12764254011')
