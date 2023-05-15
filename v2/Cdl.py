from Abstracts import Company, Book
import re
from tqdm import tqdm 


class BookCdl(Book):
    def getTitle(self):
        title = None
        try:
            title = self.pageBook.find('title').text
            title = ' '.join(re.findall(re.compile(r'\w+[,:-]?'), title))
        except:
            reg = re.compile(r'\d+')
            title = re.search(reg, self.url)
        return title

        
class Cdl(Company):
    def getUrlsBooksInPage(self, urlPage=None):
        baseURL = 'https://www.companhiadasletras.com.br/'
        urlPage = self.url if urlPage == None else urlPage
        htmlPage = self.getHTML(urlPage)
        thumbs = htmlPage.find('div', {'class':'vitrine__livros'}).findAll('div',{'class':'card__img'})
        print(thumbs)
        if thumbs != None:
            urlsBooks = [baseURL + thumb.find('a').attrs['href'] for thumb in thumbs]
            return urlsBooks
        else:
            return None


    def nextPage(self):
        next_page = f'https://www.companhiadasletras.com.br/Busca?action=buscar&pg={self.interation}&anoMin=1985&anoMax=2023&idadeMax=18&ordem=cronologica'
        self.setInteration(self.interation+1)
        return next_page
    

    def getBooks(self, urlsBooks):
        BookCdl.setSession(self.SESSION)
        return [BookCdl(urlsBooks[bookID]) for bookID in tqdm(range(len(urlsBooks)))]
    

if __name__ == '__main__':
    books = []
    cdl = Cdl('https://www.companhiadasletras.com.br/Busca?action=buscar&pg=1&anoMin=1985&anoMax=2023&idadeMax=18&ordem=cronologica', 'companhia das letras')
    print(cdl.interation)
    urlsBooks = cdl.getUrlsBooksInPage()
    books = books + cdl.getBooks(urlsBooks)
    next_page = cdl.nextPage()
    while urlsBooks != None and cdl.interation<=1:
        print(cdl.interation)
        urlsBooks = cdl.getUrlsBooksInPage(next_page)
        books = books + cdl.getBooks(urlsBooks)
        next_page = cdl.nextPage()
    print([book.getTitle() for book in books])