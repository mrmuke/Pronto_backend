from selenium import webdriver
import json

import time
cities=["Hong Kong","Bangkok","London","Macau","Singapore","Paris","Tahiti","Maui","Tokyo","Rome","Phuket","Barcelona","Bali","Dubai","New York City"]
cityLandmarks ={}

for city in cities:
    url='https://www.lonelyplanet.com/'+city.replace(" ", "-")
    driver = webdriver.Chrome(r"C:\Users\congh\Downloads\chromedriver")

    driver.get(url)
    city_full_url=driver.current_url
    driver.close()
    driver.quit()

    types=["attractions","restaurants","entertainment","nightlife","shopping","hotels","transportation"]#&subtypes=Breakfast  events find times?

    landmarks={}
    for t in types:
        landmarks[t]=[]
        for page in range(1,3):
            url =city_full_url+"/"+t+"?page="+str(page)+("&subtypes=Train%20Station%2CBus" if t=="transportation" else "")
            driver = webdriver.Chrome(r"C:\Users\congh\Downloads\chromedriver")

            driver.get(url)
            time.sleep(2)
            if(len(driver.find_elements_by_css_selector("[title*='Accept All Cookies']"))>0):
                driver.find_element_by_css_selector("[title*='Accept All Cookies']").click()
            landmarks[t]+=[x.text for x in driver.find_elements_by_xpath("//h2")]
            if(len(driver.find_elements_by_xpath('//a[@class="jsx-1214509586 lm-pill pagePill"]'))==0):
                driver.close()
                driver.quit()
                break
            driver.close()
            driver.quit()

    cityLandmarks[city]=landmarks

with open('cityLandmarks.json', 'w') as fp:
    json.dump(cityLandmarks, fp)


