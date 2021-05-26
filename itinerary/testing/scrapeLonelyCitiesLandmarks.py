import bs4 as bs  
import requests
import re  
import nltk
from nltk import pos_tag, word_tokenize
from selenium import webdriver
import json
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
#customize plan by removing locations and seeing best and worst reviews
cities=["Hong Kong","Bangkok","London","Macau","Singapore","Paris","Tahiti","Maui","Tokyo","Rome","Phuket","Barcelona","Bali","Dubai","New York City"]
cityLandmarks ={}

for city in cities:
    url ='https://www.lonelyplanet.com/'+city.replace(" ", "-")
    driver = webdriver.Chrome(r"C:\Users\congh\Downloads\chromedriver")
    driver.get(url)
    
    #create plan by getting top locations and find nearby restruants and optimal path
    #not just ajectives
    driver.find_element_by_css_selector("[title*='Accept All Cookies']").click()


    types = ["Attractions","Restaurants","Nightlife","Hotels"]
    landmarks={}
    for t in types:
        select = Select(driver.find_element_by_id('poiSelect'))
        select.select_by_visible_text('Top ' + t)
        locs = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='responsive-md font-medium leading-tight']")))
        print(locs)
        attractions = []
        #locs=driver.find_elements_by_xpath("//*[@class='responsive-md font-medium leading-tight']")
        for i in locs:
            attractions.append(i.text)
        landmarks[t]=attractions
    cityLandmarks[city]=landmarks
    driver.close()
    driver.quit()

with open('cityLandmarks.json', 'w') as fp:
    json.dump(cityLandmarks, fp)


