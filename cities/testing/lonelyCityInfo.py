import bs4 as bs  
import requests
import re  
import nltk
from nltk import pos_tag, word_tokenize
from selenium import webdriver
import requests
from urllib.parse import urlencode
import json
import time
api_key = "AIzaSyAPOOnlu8YXdWsyM3uUkz3tU7AeDWgoQqA"

def extract_lat_lng(address_or_postalcode, data_type = 'json'):
    endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
    params = {"address": address_or_postalcode, "key": api_key}
    url_params = urlencode(params)
    url = f"{endpoint}?{url_params}"
    r = requests.get(url)
    if r.status_code not in range(200, 299): 
        return {}
    latlng = {}
    try:
        latlng = r.json()['results'][0]['geometry']['location']
    except:
        pass
    return latlng.get("lat"), latlng.get("lng")


cities=["Hong Kong","Bangkok","London","Macau","Singapore","Paris","Tahiti","Maui","Tokyo","Rome","Phuket","Barcelona","Bali","Dhubai","New York City"]
cityDescriptions ={}
with open('./cityInformation.json') as f:
    cityDescriptions = json.load(f)


for city in cities:
    url ='https://www.lonelyplanet.com/'+city.replace(" ", "-")
    driver = webdriver.Chrome(r"C:\Users\congh\Downloads\chromedriver")
    driver.get(url)
    
    if(not re.search(r'The page you are looking for', driver.page_source)):
        #create plan by getting top locations and find nearby restruants and optimal path
        #not just ajectives

        if(len( driver.find_elements_by_id('introduction'))>0):
            info={}
            info["summary"] = driver.find_element_by_id('introduction').text

            cityDescriptions[city]["images"]=[]
            while(len(cityDescriptions[city]["images"])<2):
                time.sleep(3)   
                driver.refresh()
                img =  driver.find_element_by_tag_name('img').get_attribute("src")
                if img not in cityDescriptions[city]["images"]:
                    cityDescriptions[city]["images"].append(img)
            print(cityDescriptions[city]["images"])

            #info["images"]=driver.find_element_by_tag_name('img').get_attribute("src")
            lat,lng = extract_lat_lng(city)
            info["coords"] = [lat,lng]

            #cityDescriptions[city]=info
    driver.close()
    driver.quit()

with open('cityInformation.json', 'w') as fp:
    json.dump(cityDescriptions, fp)


