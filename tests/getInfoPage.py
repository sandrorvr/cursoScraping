from bs4 import BeautifulSoup
import requests
import re

with open('./tests/pageBook.html') as html:
    #req = requests.get('https://www.amazon.com.br/dp/8542221532/')
    #html.write(req.text)
    soup = BeautifulSoup(html, 'html.parser')

#def format(txt):
 #   return ' '.join(i.strip() for i in txt.split('\n'))
format = lambda txt: ' '.join(i.strip() for i in txt.split('\n'))
carousel = soup.find('div',{'class':'a-carousel-viewport'})
labels = carousel.select('div[class="a-section a-spacing-small a-text-center rpi-attribute-label"] span')
values = carousel.select('div[class="a-section a-spacing-none a-text-center rpi-attribute-value"] span')
info = {format(inf[0].text.strip()): format(inf[1].text.strip()) for inf in zip(labels,values)}
print(info)
