from requests_html import HTMLSession
from bs4 import BeautifulSoup
import json
import re

from Page import Page

class ExtractPages:
    def __init__(self):
        self.SESSION = HTMLSession()
        self.URL_AMAZON = 'https://www.amazon.com.br'
        self.DEPARTMENTS = {}
    
    def getHTML(self, url):
        html = self.SESSION.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        return soup
    
    def getHref(self, element, tp):
        if tp == 'department':
            tag = 'a'
        elif tp == 'book':
            tag = 'sapn'
        else:
            raise('Type off out escoupe')
        try:
            href = element.find(tag).attrs['href']
            info = element.find(tag).text.strip()
        except AttributeError:
            href = None
            info = None
        return (info, href)
    
    def extractIdNumberHref(href):
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
            dp_href = self.getHref(li, 'department')
            self.DEPARTMENTS[dp_href[0]] = self.extractIdNumberHref(dp_href[1])
        with open('departments.json', 'w', encoding='UTF-8') as file:
            json.dump(self.DEPARTMENTS, file, ensure_ascii=False)
    
    
    def getBooksByDepartmentByPage(self, department_node, pag=1):
        '''
            {
                pag:str,
                books:[
                    {
                        id:str,
                        title:str,
                        authors:[str],
                        valor:str,
                        language:str

                    }
                ]
            }
        '''
        dic = {'pag':pag, 'books':[]}
        url_pag_books = f'{self.URL_AMAZON}/s?rh=n%3A{department_node}&fs=true&page={pag}'
        articles = []
        while articles == []:
            soup = self.getHTML(url_pag_books)
            articles = soup.select('h2 a')
        for card in articles:
            bk_href = self.getHref(card, 'department')
            idPage = self.extractIdNumberHref(bk_href[1])
            page = Page(idPage)
        return dic
    

