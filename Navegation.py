from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

class Navegation:
    def __init__(self, url):
        self.url = url
        self.browser = webdriver.Chrome(executable_path='./chromedriver')
        self.GET(url)

    def GET(self, url, n_interation=0):
        print('GET url da lista', url)
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

    
    def getBrowser(self):
        return self.browser

    def getBooksInPag(self):
        hrefs = self.browser.find_elements(By.XPATH, '//h2//a[@href]')
        return [elements.get_attribute('href') for elements in hrefs]
    
    def nextList(self):
        self.GET(self.url)
        next_list = self.browser.find_element(By.XPATH, "//span[@class='s-pagination-strip']//a[last()]")
        self.url = next_list.get_attribute('href')
        print('url da lista anterior', self.url)
        next_list.click()
        sleep(5)
    