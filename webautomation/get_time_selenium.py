#Description: runs a query on time and counts the image objects we find as a result.

from selenium import webdriver
from selenium.webdriver.common.by import By

def check_duckduckgo_time():
    # Launch Firefox browser
    driver = webdriver.Firefox()

    # Open DuckDuckGo and search for time
    driver.get('https://duckduckgo.com')
    #id="search_form_input_homepage"
    search_input = driver.find_element('id','search_form_input_homepage')
    search_input.send_keys('time now in EST')
    search_input.submit()

    #get all the image objects that are referenced on the result
    all_images=driver.find_elements(By.XPATH, '//img')
    all_image_count=len(all_images)

    print(f"We found {all_image_count} images on the page.")


    driver.quit()



    # Close the browser
    

check_duckduckgo_time()
