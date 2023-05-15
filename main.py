#from selenium import webdriver
#from selenium.webdriver.common.by import By

#browser = webdriver.Chrome(executable_path='./chromedriver')

#browser.get('https://www.amazon.com.br/s?rh=n%3A7841795011&fs=true&ref=lp_7841795011_sar')
#next_pag = browser.find_element(By.XPATH, "//span[@class='s-pagination-strip']//a[last()]")
#next_pag.click()
#hrefs = browser.find_elements(By.XPATH, '//h2//a[@href]')
#print(next_pag.text)
#print([el.get_attribute('href') for el in hrefs])
from DataBaseConection import DB
from Navegation import Navegation
from Book import Book

nav = Navegation('https://www.amazon.com.br/s?rh=n%3A7872854011&fs=true&ref=lp_7872854011_sar')
Book.setBrowser(nav.getBrowser())

db = DB()
db.createDB()

pag = 0
info = []
while pag < 75:
    print(f'=========== PAG {pag+1} ===========')
    books_in_pag = nav.getBooksInPag()
    print(len(books_in_pag))
    for href_book in books_in_pag:
        book = Book(href_book)#.getInfos()
        #isbn10, isbn13, title, price, author, language, company, n_pages, resume
        try:
            data = (
                book.getISBN10(),
                book.getISBN13(),
                book.getTitle(),
                book.getPrice(),
                book.getAuthors(),
                book.getLanguage(),
                book.getCompany(),
                book.getNPages(),
                book.getResume(),
            )
        except Exception as e:
            print('erro ao pegar o livro', e.args)
            data = ('-','-','-','-','-','-','-','-','-',)

        try:
            db.insertData(data)
            print(f'book inserted: {data[2]}')
        except Exception as e:
            print(f'book not inserted: {data[2]}', e.args)
    nav.nextList()
    pag = pag + 1
print(info)
