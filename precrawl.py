from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time, requests

def readHTML(filename):
    content = ''
    with open(filename, 'r') as file:
        content = file.read()
    return BeautifulSoup(content, 'html.parser')

class ChromeDriver:
    def __init__(self):
        driverPath = "./chromedriver"
        s = Service(executable_path=driverPath)
        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s)
        self.driver.set_page_load_timeout(500)
    def drive(self, url):
        self.driver.get(url)
    def waitUntil(self, selector):
        WebDriverWait(self.driver, 200).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
    def writeHTML(self, filename):
        with open(filename, 'w') as file:
            file.write(str(self.driver.page_source))
        self.sp = BeautifulSoup(self.driver.page_source, 'html.parser')
    def quit(self):
        self.driver.quit()

class Starlux:
    # param will be a constraint of selector or a filename 
    def __init__(self, option, param):
        self.driver = None
        if option == 0:
            self.driver = ChromeDriver()
            self.driver.drive('https://www.starlux-airlines.com/zh-TW')
            self.driver.waitUntil(param)
            self.driver.writeHTML('s_html_src.txt')
            self.sp = readHTML('s_html_src.txt')
        else:
            self.sp = readHTML(param)
    def getCity(self):
        ct_tag = self.sp.select_one('#swiper-wrapper-a86864110fe5d26fd').select('.swiper-slide-custom')
        self.city = []
        for city in ct_tag:
            link = city['href']
            name = city.text.replace(' ', '').replace('\n', '')
            eng = link.split('/')[-1].split('-', 4)[-1].replace('-', ' ').title()
            img = city.find('img')['src']
            self.city.append((name, eng, link, img))
class Lion:
    # param will be a constraint of selector or a filename 
    def __init__(self, option, param):
        self.driver = None
        if option == 0:
            self.driver = ChromeDriver()
            self.driver.drive('https://travel.liontravel.com/search?TravelPavilionGroupID=5611&Platform=APP')
            self.driver.waitUntil(param)
            self.driver.writeHTML('l_html_src.txt')
            self.sp = readHTML('l_html_src.txt')
        else:
            self.sp = readHTML(param) 
    def getInfo(self):
        self.infos = [] 
        blocks = self.sp.select('.cardsList--2cG2D')
        for block in blocks:
            div1 = block.find('div')
            nDays = div1.find_all('div')[1].text
            imgSrc = div1.find('img')['src']
            title = block.select_one('.caption--mphmX').text
            s_date = [blk.text for blk in block.select_one('.goDate--15jBZ').select('span') if blk.text != '...']
            self.infos.append([nDays, imgSrc, title, s_date])

            
if __name__ == '__main__':
    lion = Lion(1, 'l_html_src.txt')
    lion.getInfo()
    print(lion.infos)
    