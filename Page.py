from bs4 import BeautifulSoup
from requests_html import HTMLSession
from PIL import Image
import re


class Captcha:
    def __init__(self, session):
        self.SESSION = session

    @staticmethod
    def haveCaptchaGot(soup):
        error = soup.find(string=re.compile(r'Digite os caracteres que você vê abaixo'))
        return True if error != None else False
    
    def getUrlImg(self, soup):
        img = soup.find('img', {'src':re.compile(r'*.jpeg')})
        print(img['src'])
        return img['src']

    def getImg(self, url_img):
        req = self.SESSION.get(url_img,  stream=True)
        img = Image.open(req.raw)
        img.show()

class Page:
    def __init__(self, session, book):
        self.SESSION = session
        self.url = f'https://www.amazon.com.br/dp/{book}/'
        self.html = self.getHTML()

    def getHTML(self):
        html = self.SESSION.get(self.url)
        soup = BeautifulSoup(html.text, 'html.parser')
        if Captcha.haveCaptchaGot(soup): 
            url_img = self.getUrlImg(soup)
            Captcha(self.SESSION).getImg(url_img)
            return 
        else:
            return soup
    
    def extractTitle(self):
        return self.html.find('span',{'id':'productTitle'}).text
    
    def extractAuthors(self):
        info = self.html.find('div', {'id':'bylineInfo'})
        return [author.text for author in info.findAll('a')]

if __name__ == '__main__':
    pag = Page('8555341620')
    #print(pag.extractTitle())
    #print(pag.extractAuthors())