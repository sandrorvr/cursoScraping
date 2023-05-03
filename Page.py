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
        with open('./tests/pageBook2.html', 'w') as file:
            file.write(html.text)
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
    
    def extractPrice(self):
        price = self.html.find('span',{'id':'price'}).text
        return price
    
    
    def extractMoreInformations(self):
        format = lambda txt: ' '.join(i.strip() for i in txt.split('\n'))
        carousel = self.html.find('div',{'class':'a-carousel-viewport'})
        labels = carousel.select('div[class="a-section a-spacing-small a-text-center rpi-attribute-label"] span')
        values = carousel.select('div[class="a-section a-spacing-none a-text-center rpi-attribute-value"] span')
        info = {format(inf[0].text): format(inf[1].text) for inf in zip(labels,values)}
        return info

    

if __name__ == '__main__':
    pag = Page('8555341620')
    #print(pag.extractTitle())
    #print(pag.extractAuthors())