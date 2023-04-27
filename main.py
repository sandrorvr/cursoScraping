from requests_html import HTMLSession
from bs4 import BeautifulSoup
import json
import re

URL_AMAZON = 'https://www.amazon.com.br'
DEPARTMENTS = {}
SESSION = HTMLSession()

def getDepartmentAndHref(li):
    try:
        href = li.find('a').attrs['href']
        department = li.find('a').text.strip()
    except AttributeError:
        print('attribute not find')
        href = None
        department = None
    return [department, href]

def getBookAndHref(card):
    try:
        href = card.attrs['href']
        titleOfBook = card.find('span').text.strip()
    except AttributeError:
        print('attribute not find')
        href = None
        titleOfBook = None
    return (titleOfBook, href)

def extractNumberDepartment(href):
    com = re.compile(r'.{3}dp/[\d\w]{10,}|&node=[\d\w]{10,}|.{3}%[\d\w]{2}[\d\w]{10,}')
    try:
        extracted = re.findall(com, href)[0][6:]
        return extracted
    except IndexError:
        print(href) 

def getAllDepartments():
    url_books = URL_AMAZON + '/gp/browse.html?node=6740748011'
    req = SESSION.get(url_books)
    soup = BeautifulSoup(req.text, 'html.parser')
    div_refinements = soup.find('div',{'id':'s-refinements'})
    div_department = div_refinements.find('span',string='Livros').parent.parent.parent
    li_links = div_department.findAll('li')
    for li in li_links[1:]:
        dp_href = getDepartmentAndHref(li)
        DEPARTMENTS[dp_href[0]] = extractNumberDepartment(dp_href[1])
    with open('departments.json', 'w', encoding='UTF-8') as file:
        json.dump(DEPARTMENTS, file, ensure_ascii=False)

def saveBooks(dic):
    with open('books.json', 'a') as file:
        file.write(json.dumps(dic, ensure_ascii=False))
        file.write(',\n')

def getBooksByDepartmentByPage(department_node, pag=1):
    dic = {'pag':pag, 'books':[]}
    url_books_department = f'{URL_AMAZON}/s?rh=n%3A{department_node}&fs=true&page={pag}'
    articles = []
    while articles == []:
        req = SESSION.get(url_books_department)
        soup = BeautifulSoup(req.text, 'html.parser')
        articles = soup.select('h2 a')
    for card in articles:
        book_href = getBookAndHref(card)
        dic['books'].append({'title': book_href[0], 'book':extractNumberDepartment(book_href[1])})
    return dic


if __name__ == '__main__':
    #getAllDepartments()
    #print(len(BOOKS_BY_DEPARTMENT), BOOKS_BY_DEPARTMENT)
    with open('departments.json') as file:
        DEPARTMENTSJSON = json.load(file)

    for key in DEPARTMENTSJSON.keys():
        BOOKS_BY_DEPARTMENTS = {'department':key, 'books':[]}
        for pg in range(2):
            BOOKS_BY_DEPARTMENTS['books'].append(getBooksByDepartmentByPage(DEPARTMENTSJSON[key], pag=pg))
        saveBooks(BOOKS_BY_DEPARTMENTS)