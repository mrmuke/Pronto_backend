from time import sleep
from selenium import webdriver
import os
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
    
def page_scrape(driver):
    """This function takes care of the scraping part"""
    
    xp_sections = '//div[starts-with(@class,"section duration")]'
    sections = driver.find_elements_by_xpath(xp_sections)
    sections_list = [value.text for value in sections]
    section_a = sections_list[0] # This is to separate the two flights
    section_b = sections_list[1] # This is to separate the two flights

    # if you run into a reCaptcha, you might want to do something about it
    # you will know there's a problem if the lists above are empty
    # this if statement lets you exit the bot or do something else
    # you can add a sleep here, to let you solve the captcha and continue scraping
    # i'm using a SystemExit because i want to test everything from the start
    if section_a == None:
        raise SystemExit
    
    # I'll use the letter A for the outbound flight and B for the inbound
    a_section_name = ''.join(section_a.split()[2:5])
    a_duration = ''.join(section_a.split()[0:2])

    b_duration = ''.join(section_b.split()[0:2])
    b_section_name = ''.join(section_b.split()[2:5])


    xp_dates = '//div[@class="section date"]'
    dates = driver.find_elements_by_xpath(xp_dates)
    dates_list = [value.text for value in dates]
    a_date = dates_list[0]
    b_date = dates_list[1]
    # Separating the weekday from the day
    a_day = a_date.split()[0]
    a_weekday = a_date.split()[1]
    b_day = b_date.split()[0]
    b_weekday = b_date.split()[1]
    
    # getting the prices
    xp_prices = '//a[starts-with(@class,"booking-link")]/span[@class="price option-text"]'
    price = driver.find_elements_by_xpath(xp_prices)[0]
    price_text = int(price.text.replace('$','').replace(',',''))

    # the stops are a big list with one leg on the even index and second leg on odd index
    xp_stops = '//div[@class="section stops"]/div[1]'
    stops = driver.find_elements_by_xpath(xp_stops)
    a_stop_list = stops[0].text.replace('n','0')
    b_stop_list = stops[1].text.replace('n','0')

    xp_stops_cities = '//div[@class="section stops"]/div[2]'
    stops_cities = driver.find_elements_by_xpath(xp_stops_cities)
    a_stop_name_list = stops_cities[0].text
    b_stop_name_list = stops_cities[1].text
    
    # this part gets me the airline company and the departure and arrival times, for both legs
    xp_schedule = '//div[@class="section times"]'
    schedules = driver.find_elements_by_xpath(xp_schedule)
    hours_list = []
    carrier_list = []
    for schedule in schedules:
        hours_list.append(schedules[0].text.split('\n')[0])
        carrier_list.append(schedule.text.split('\n')[1])
    # split the hours and carriers, between a and b legs
    a_hours = hours_list[0]
    a_carrier = carrier_list[0]
    b_hours = hours_list[1]
    b_carrier = carrier_list[1]

    
    

    flight={'OutDay':a_day,
                               'OutWeekday': a_weekday,
                               'OutDuration': a_duration,
                               'OutCities': a_section_name,
                               'ReturnDay': b_day,
                               'ReturnWeekday': b_weekday,
                               'ReturnDuration': b_duration,
                               'ReturnCities': b_section_name,
                               'OutStops': a_stop_list,
                               'OutStopCities': a_stop_name_list,
                               'ReturnStops': b_stop_list,
                               'ReturnStopCities': b_stop_name_list,
                               'OutTime': a_hours,
                               'OutAirline': a_carrier,
                               'ReturnTime': b_hours,
                               'ReturnAirline': b_carrier,                           
                               'Price': price_text}  
    print(flight) 
    return flight
def start_kayak(city_from, city_to, date_start, date_end):

    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


    kayak = ('https://www.kayak.com/flights/' + city_from + '-' + city_to +
             '/' + date_start + '-flexible/' + date_end + '-flexible?sort=bestflight_a')
    driver.get(kayak)
    sleep(4)
    
    # sometimes a popup shows up, so we can use a try statement to check it and close
    try:
        xp_popup_close = '//button[contains(@id,"dialog-close") and contains(@class,"Button-No-Standard-Style close ")]'
        print("found")
        driver.find_elements_by_xpath(xp_popup_close)[len(driver.find_elements_by_xpath(xp_popup_close))-1].click()
    except Exception as e:
        pass
    sleep(10)
    
    
    print('starting first scrape.....')
    info = page_scrape(driver)
    sleep(2)
    
    # We can keep track of what they predict and how it actually turns out!
    xp_loading = '//*[contains(@id,"advice")]'
    loading = driver.find_element_by_xpath(xp_loading).text
    xp_prediction = '//span[@class="info-text"]'
    prediction = driver.find_element_by_xpath(xp_prediction).text
    
    # sometimes we get this string in the loading variable, which will conflict with the email we send later
    # just change it to "Not Sure" if it happens
    weird = '¯\\_(ツ)_/¯'
    if loading == weird:
        loading = 'Not sure'
    info["prediction"]=prediction
    driver.quit()
    return info
    

def get_best_flight(city_from,city_to, date_start,date_end):


    flight = start_kayak(city_from, city_to, str(date_start), str(date_end))

    
    return flight

