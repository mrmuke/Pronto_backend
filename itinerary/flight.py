from time import sleep, strftime
import pandas as pd
from selenium import webdriver


    
def page_scrape(driver):
    """This function takes care of the scraping part"""
    
    xp_sections = '//div[starts-with(@class,"section duration")]'
    sections = driver.find_elements_by_xpath(xp_sections)
    sections_list = [value.text for value in sections]
    section_a_list = sections_list[::2] # This is to separate the two flights
    section_b_list = sections_list[1::2] # This is to separate the two flights
    print(sections_list)
    # if you run into a reCaptcha, you might want to do something about it
    # you will know there's a problem if the lists above are empty
    # this if statement lets you exit the bot or do something else
    # you can add a sleep here, to let you solve the captcha and continue scraping
    # i'm using a SystemExit because i want to test everything from the start
    if section_a_list == []:
        raise SystemExit
    
    # I'll use the letter A for the outbound flight and B for the inbound
    a_duration = []
    a_section_names = []
    for n in section_a_list:
        # Separate the time from the cities
        a_section_names.append(''.join(n.split()[2:5]))
        a_duration.append(''.join(n.split()[0:2]))
    b_duration = []
    b_section_names = []
    for n in section_b_list:
        # Separate the time from the cities
        b_section_names.append(''.join(n.split()[2:5]))
        b_duration.append(''.join(n.split()[0:2]))

    xp_dates = '//div[@class="section date"]'
    dates = driver.find_elements_by_xpath(xp_dates)
    dates_list = [value.text for value in dates]
    a_date_list = dates_list[::2]
    b_date_list = dates_list[1::2]
    # Separating the weekday from the day
    a_day = [value.split()[0] for value in a_date_list]
    a_weekday = [value.split()[1] for value in a_date_list]
    b_day = [value.split()[0] for value in b_date_list]
    b_weekday = [value.split()[1] for value in b_date_list]
    
    # getting the prices
    xp_prices = '//a[starts-with(@class,"booking-link")]/span[@class="price option-text"]'
    prices = driver.find_elements_by_xpath(xp_prices)
    prices_list = [int(price.text.replace('$','').replace(',','')) for price in prices if price.text != '']

    # the stops are a big list with one leg on the even index and second leg on odd index
    xp_stops = '//div[@class="section stops"]/div[1]'
    stops = driver.find_elements_by_xpath(xp_stops)
    stops_list = [stop.text[0].replace('n','0') for stop in stops]
    a_stop_list = stops_list[::2]
    b_stop_list = stops_list[1::2]

    xp_stops_cities = '//div[@class="section stops"]/div[2]'
    stops_cities = driver.find_elements_by_xpath(xp_stops_cities)
    stops_cities_list = [stop.text for stop in stops_cities]
    a_stop_name_list = stops_cities_list[::2]
    b_stop_name_list = stops_cities_list[1::2]
    
    # this part gets me the airline company and the departure and arrival times, for both legs
    xp_schedule = '//div[@class="section times"]'
    schedules = driver.find_elements_by_xpath(xp_schedule)
    hours_list = []
    carrier_list = []
    for schedule in schedules:
        hours_list.append(schedule.text.split('\n')[0])
        carrier_list.append(schedule.text.split('\n')[1])
    # split the hours and carriers, between a and b legs
    a_hours = hours_list[::2]
    a_carrier = carrier_list[::2]
    b_hours = hours_list[1::2]
    b_carrier = carrier_list[1::2]

    
    cols = (['OutDay','OutTime','OutWeekday','OutAirline','OutCities','OutDuration','OutStops','OutStopCities',
'ReturnDay','ReturnTime','ReturnWeekday','ReturnAirline','ReturnCities','ReturnDuration','ReturnStops','ReturnStopCities',
'Price'])
    print(len(b_day))
    print(len(b_weekday))
    print(len(b_duration))
    print(len(b_section_names))
    print(len(b_stop_list))
    print(len(b_stop_name_list))
    print(len(b_hours))
    print(len(b_carrier))
    print(len(prices_list))
    
    print(len(a_day))
    print(len(a_weekday))
    print(len(a_duration))
    print(len(a_section_names))
    print(len(a_stop_list))
    print(len(a_stop_name_list))
    print(len(a_hours))
    print(len(a_carrier))
    flights_df = pd.DataFrame({'OutDay':a_day,
                               'OutWeekday': a_weekday,
                               'OutDuration': a_duration,
                               'OutCities': a_section_names,
                               'ReturnDay': b_day,
                               'ReturnWeekday': b_weekday,
                               'ReturnDuration': b_duration,
                               'ReturnCities': b_section_names,
                               'OutStops': a_stop_list,
                               'OutStopCities': a_stop_name_list,
                               'ReturnStops': b_stop_list,
                               'ReturnStopCities': b_stop_name_list,
                               'OutTime': a_hours,
                               'OutAirline': a_carrier,
                               'ReturnTime': b_hours,
                               'ReturnAirline': b_carrier,                           
                               'Price': prices_list})[cols]
    
    flights_df['timestamp'] = strftime("%Y%m%d-%H%M") # so we can know when it was scraped
    return flights_df
def start_kayak(city_from, city_to, date_start, date_end):

    driver = webdriver.Chrome(r"C:\Users\mxing\Downloads\chromedriver")

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
    sleep(3)
    
    
    print('starting first scrape.....')
    df_flights_best = page_scrape(driver)
    df_flights_best['sort'] = 'best'
    sleep(2)
    
    # Let's also get the lowest prices from the matrix on top
    matrix = driver.find_elements_by_xpath('//*[contains(@id,"FlexMatrixCell")]')
    matrix_prices = [int(price.text.replace('$','').replace(',','')) for price in matrix if price.text != '']
    matrix_min = min(matrix_prices)
    matrix_avg = sum(matrix_prices)/len(matrix_prices)
    
    print('switching to cheapest results.....')
    cheap_results = '//a[@data-code = "price"]'
    driver.find_element_by_xpath(cheap_results).click()
    sleep(2)

    
    print('starting second scrape.....')
    df_flights_cheap = page_scrape(driver)
    df_flights_cheap['sort'] = 'cheap'
    sleep(1)
    
    print('switching to quickest results.....')
    quick_results = '//a[@data-code = "duration"]'
    driver.find_element_by_xpath(quick_results).click()  
    sleep(2)
    print('loading more.....')
    
    
    print('starting third scrape.....')
    df_flights_fast = page_scrape(driver)
    df_flights_fast['sort'] = 'fast'
    sleep(1)
    
    # saving a new dataframe as an excel file. the name is custom made to your cities and dates
    final_df = df_flights_cheap.append(df_flights_best).append(df_flights_fast)
    print(final_df)
    final_df.to_excel('{}_flights_{}-{}_from_{}_to_{}.xlsx'.format(strftime("%Y%m%d-%H%M"),
                                                                                   city_from, city_to, 
                                                                                   date_start, date_end), index=False)
    print('saved df.....')
    
    # We can keep track of what they predict and how it actually turns out!
    xp_loading = '//*[contains(@id,"advice")]'
    loading = driver.find_element_by_xpath(xp_loading).text
    xp_prediction = '//span[@class="info-text"]'
    prediction = driver.find_element_by_xpath(xp_prediction).text
    print(loading+'\n'+prediction)
    
    # sometimes we get this string in the loading variable, which will conflict with the email we send later
    # just change it to "Not Sure" if it happens
    weird = '¯\\_(ツ)_/¯'
    if loading == weird:
        loading = 'Not sure'
  
    msg = ('Cheapest Flight: {}\nAverage Price: {}\n\nRecommendation: {}'.format(matrix_min, matrix_avg, (loading+'\n'+prediction)))
    driver.save_screenshot('pythonscraping.png')
    driver.quit()
    return final_df.to_dict(orient='records')[0]
    

def get_best_flight(city_from,city_to, date_start,date_end):


    flight = start_kayak(city_from, city_to, str(date_start), str(date_end))

    
    return flight

