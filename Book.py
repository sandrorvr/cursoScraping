from selenium.webdriver.common.by import By
import re
from time import sleep

class Book:
    browser = None
    def __init__(self, url):
        self.info = {}
        self.GET(url)
    
    def GET(self, url, n_interation=0):
        status = False
        while not status:
            seconds = 10**(n_interation/5)
            try:
                self.browser.get(url)
                status = True
            except:
                print(url)
                sleep(seconds)
                n_interation = n_interation + 1

    @classmethod
    def setBrowser(cls, browser):
        cls.browser = browser
    
    @classmethod
    def getBrowser(cls):
        return cls.browser
    
    def getTitle(self):
        span_title = self.browser.find_element(By.XPATH, "//h1[@id='title']//span")
        return span_title.text
    
    def getAuthors(self):
        span_author = self.browser.find_element(By.XPATH, "//span[@class='author notFaded']")
        span_author = re.search(re.compile(r'[\w\s]+'), span_author.text).group().strip()
        return span_author
    
    def getPrice(self):
        span_price = self.browser.find_element(By.XPATH, "//span[@class='a-size-base a-color-price a-color-price']")
        return span_price.text
    
    def getCompany(self):
        spans = self.browser.find_elements(By.XPATH, "//div[@id='detailBullets_feature_div']//ul//li//span[@class='a-list-item']")
        for i in range(len(spans)):
            span_company = spans[i].text.split(' : ')
            if span_company[0].strip() == 'Editora':
                return span_company[1].strip()
        return '-'
    
    def getLanguage(self):
        spans = self.browser.find_elements(By.XPATH, "//div[@id='detailBullets_feature_div']//ul//li//span[@class='a-list-item']")
        for i in range(len(spans)):
            span_company = spans[i].text.split(' : ')
            if span_company[0].strip() == 'Idioma':
                return span_company[1].strip()
        return '-'
    
    def getNPages(self):
        spans = self.browser.find_elements(By.XPATH, "//div[@id='detailBullets_feature_div']//ul//li//span[@class='a-list-item']")
        for i in range(len(spans)):
            span_company = spans[i].text.split(' : ')
            if span_company[0].strip() == 'Capa comum':
                return span_company[1].strip()
        return '-'
    
    def getISBN10(self):
        spans = self.browser.find_elements(By.XPATH, "//div[@id='detailBullets_feature_div']//ul//li//span[@class='a-list-item']")
        for i in range(len(spans)):
            span_company = spans[i].text.split(' : ')
            if span_company[0].strip() == 'ISBN-10':
                return span_company[1].strip()
        return '-'
    
    def getISBN13(self):
        spans = self.browser.find_elements(By.XPATH, "//div[@id='detailBullets_feature_div']//ul//li//span[@class='a-list-item']")
        for i in range(len(spans)):
            span_company = spans[i].text.split(' : ')
            if span_company[0].strip() == 'ISBN-13':
                return span_company[1].strip()
        return '-'
    
    def getResume(self):
        span_Resume = self.browser.find_element(By.XPATH, "//div[@class='a-expander-content a-expander-partial-collapse-content']//span")
        return span_Resume.text
    
    def getInfos(self):
        self.info['title'] = self.getTitle()
        self.info['author'] = self.getAuthors()
        self.info['price'] = self.getPrice()
        self.info['language'] = self.getLanguage()
        self.info['company'] = self.getCompany()
        self.info['n_pages'] = self.getNPages()
        self.info['isbn10'] = self.getISBN10()
        self.info['isbn13'] = self.getISBN13()
        self.info['resume'] = self.getResume()
        return self.info

if __name__ == '__main__':
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    browser = webdriver.Chrome(executable_path='./chromedriver')
    #browser.get('https://www.amazon.com.br/Busca-Mesmos-Cl%C3%B3vis-Barros-Filho/dp/8568014453/ref=sr_1_6?qid=1684026033&s=books&sr=1-6')
    #spans = browser.find_elements(By.XPATH, "//div[@id='detailBullets_feature_div']//ul//li//span[@class='a-list-item']")
    #result = '-'
    #for i in range(len(spans)):
    #    span_company = spans[i].text.split(' : ')
    #    print(span_company)
    #    if span_company[0].strip() == 'Editora':
    #        result = span_company[1].strip()
    #        break
    #print(result)
    #print([e.text for e in span_language])
    Book.setBrowser(browser)
    book = Book('https://www.amazon.com.br/livro-ouro-mitologia-Hist%C3%B3rias-deuses/dp/8595082316?ref_=Oct_d_otopr_d_7842838011_0&pd_rd_w=cfI3A&content-id=amzn1.sym.578aa6a5-6bfa-4747-975c-cee0f889732e&pf_rd_p=578aa6a5-6bfa-4747-975c-cee0f889732e&pf_rd_r=HJ9CBB2TN97A7T16V9AB&pd_rd_wg=tgKpi&pd_rd_r=4b5fa47d-8daa-4b0b-9543-6470494db376&pd_rd_i=8595082316')
    print(book.getInfos())