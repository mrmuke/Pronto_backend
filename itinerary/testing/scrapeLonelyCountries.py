import bs4 as bs  
import requests
import re  
import nltk
from nltk import pos_tag, word_tokenize
from selenium import webdriver
import json
countries={}
cityAdjectives ={}
with open('./countries.json') as f:
  countries = json.load(f)
  
for country in countries:
    for city in countries[country]:
        url ='https://www.lonelyplanet.com/'+country.replace(" ", "-")+'/'+city.replace(" ", "-")
        driver = webdriver.Chrome(r"C:\Users\mxing\Downloads\chromedriver")
        driver.get(url)
        
        if(not re.search(r'The page you are looking for', driver.page_source)):
            #create plan by getting top locations and find nearby restruants and optimal path
            #not just ajectives
            driver.find_element_by_css_selector("[title*='Accept All Cookies']").click()
            if(len(driver.find_elements_by_css_selector("[title*='Read More']"))>0):
                driver.find_element_by_css_selector("[title*='Read More']").click()
            if(len( driver.find_elements_by_id('introduction'))>0):

                intro = driver.find_element_by_id('introduction')
                adjectives=[]
                print(intro.text)
                for tag in pos_tag(word_tokenize(intro.text)):
                    if(tag[1]=="JJ" and tag[1] not in adjectives):
                        adjectives.append(tag[0])
                cityAdjectives[city]=adjectives

        driver.close()
        driver.quit()

with open('cityAdjectives.json', 'w') as fp:
    json.dump(cityAdjectives, fp)


print(adjectives)
