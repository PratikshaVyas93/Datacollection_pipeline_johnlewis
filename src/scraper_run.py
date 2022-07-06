import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Chrome("src/chromedriver")
driver.get("https://www.johnlewis.com") 
def __get_each_element(data):
        elements = driver.find_element(by=By.XPATH, value=data) 
        return elements 
try:
    accept_cookies_by_clicking = __get_each_element("//*[@data-test='allow-all']") 
    accept_cookies_by_clicking.click()
except AttributeError:
    pass
except Exception as e:
    print(str(e))
    pass  

res = requests.get("https://www.johnlewis.com/search?search-term=mobile")
content = res.text
soup = BeautifulSoup(content)
print(soup)