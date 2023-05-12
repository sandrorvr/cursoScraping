from Abstracts import Company, Book
import re
from tqdm import tqdm 
class BookIntrinseca(Book):
    def getTitle(self):
        title = None
        try:
            title = self.pageBook.find('header',{'class':'book-header'}).find('h1').text
            title = ' '.join(re.findall(re.compile(r'\w+[,:-]?'), title))
        except:
            reg = re.compile(r'\d+')
            title = re.search(reg, self.url)
        return title

        
class Intrinseca(Company):
    def getUrlsBooksInPage(self, urlPage=None):
        urlPage = self.url if urlPage == None else urlPage
        htmlPage = self.getHTML(urlPage)
        thumbs = htmlPage.findAll('article', {'class':'book-summary'})
        if thumbs != None:
            urlsBooks = [thumb.find('a').attrs['href'] for thumb in thumbs]
            return urlsBooks
        else:
            return None

    def nextPage(self):
        next_page = f'https://www.intrinseca.com.br/catalogo/?pagenum={self.interation}'
        self.setInteration(self.interation+1)
        return next_page
    
    def getBooks(self, urlsBooks):
        BookIntrinseca.setSession(self.SESSION)
        return [BookIntrinseca(urlsBooks[bookID]) for bookID in tqdm(range(len(urlsBooks)))]
    

    
if __name__ == '__main__':
    books = []
    intrinseca = Intrinseca('https://www.intrinseca.com.br/catalogo/', 'intrinseca')
    print(intrinseca.interation)
    urlsBooks = intrinseca.getUrlsBooksInPage()
    books = books + intrinseca.getBooks(urlsBooks)
    next_page = intrinseca.nextPage()
    while urlsBooks != None and intrinseca.interation<=1:
        print(intrinseca.interation)
        urlsBooks = intrinseca.getUrlsBooksInPage(next_page)
        books = books + intrinseca.getBooks(urlsBooks)
        next_page = intrinseca.nextPage()
    print([book.getTitle() for book in books])