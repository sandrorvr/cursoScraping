from Abstracts import Company
class Intrinseca(Company):
    def getUrlsBooksInPage(self, urlPage=None):
        urlPage = self.url if urlPage == None else urlPage
        htmlPage = self.getHTML(urlPage)
        thumbs = htmlPage.findAll('article', {'class':'book-summary'})
        urlsBooks = [thumb.find('a').attrs['href'] for thumb in thumbs]
        return urlsBooks
    
    def nextPage(self):
        print('x')

if __name__ == '__main__':
    intrinseca = Intrinseca('https://www.intrinseca.com.br/catalogo/', 'intrinseca')
    urlsBooks = intrinseca.getUrlsBooksInPage()
    print(urlsBooks)