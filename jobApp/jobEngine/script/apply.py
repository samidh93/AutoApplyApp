from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import json

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--headless')

ACCOUNT_EMAIL = "dhiebzayneb89@gmail.com"
ACCOUNT_PASSWORD = "8862468@"
PHONE = "20094923"
JOB = "recruiting"
LOCATION = "Berlin"

chrome_driver_path = "/Users/sami/dev/AutoApplyApp/jobApp/chromedriver"
option = webdriver.ChromeOptions()
s = Service(chrome_driver_path)
driver = webdriver.Chrome(service=s, options=option)
driver.maximize_window()
driver.get(f'https://www.linkedin.com/jobs/search/?f_AL=true&keywords={JOB}&location={LOCATION}&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0')


time.sleep(2)
sign_in_button = driver.find_element('link text', "Sign in")
sign_in_button.click()

time.sleep(5)
email_field = driver.find_element('id', "username")
email_field.send_keys(ACCOUNT_EMAIL)
password_field = driver.find_element("id", "password")
password_field.send_keys(ACCOUNT_PASSWORD)
password_field.send_keys(Keys.ENTER)

time.sleep(50)

# jobs_block = driver.find_elements("class name",'jobs-search-results__list')
# jobs_list = jobs_block.find_elements(By.CSS_SELECTOR, ".jobs-search-results__list-item")
page = 2
while page < 5 :
    i = 0
# print(len(jobs_list))
    while i < 4:
        jobs_list = driver.find_elements("css selector", ".job-card-container--clickable")
        print(len(jobs_list))
        driver.execute_script("arguments[0].scrollIntoView();", jobs_list[-1])
        time.sleep(2)
        i += 1

    for listing in jobs_list:
        listing.click()
        print("called")

        time.sleep(3)
        try:

            apply_button = driver.find_element("css selector",".jobs-apply-button--top-card")
            if apply_button.text == 'Easy Apply':
                apply_button.click()
                time.sleep(5)
                submit_button = driver.find_element("class name", "artdeco-button--primary")
                # first page
                if submit_button.text == 'Next':
                    time.sleep(5)
                    # resume_button = driver.find_element("css selector", "[aria-label='Choose Resume']")
                    submit_button.click()
                    # Second page
                    resume_button = driver.find_element("css selector", "[aria-label='Choose Resume']")
                    resume_button.click()
                    time.sleep(3)
                    # Third page
                    review_button = driver.find_element("class name", "artdeco-button--primary")
                    print(review_button)
                    if review_button.text == 'Review':
                        print('review section')
                        review_button.click()
                        time.sleep(3)
                        fin_button = driver.find_element("css selector", "[aria-label='Submit application']")
                        fin_button.click()
                        time.sleep(3)
                    else:
                        print('continue section')
                        review_button.click()
                        time.sleep(5)

                        # Forth page
                        qCheck = driver.find_element("class name", "t-16")
                        if qCheck.text == 'Additional Questions':
                            time.sleep(3)
                            close_button = driver.find_element("class name", "artdeco-modal__dismiss")
                            close_button.click()
                            time.sleep(5)
                            # save application which needs more info

                            save_button = driver.find_elements("class name", "artdeco-modal__confirm-dialog-btn")[1]
                            save_button.click()
                            time.sleep(5)
                        else:
                            next_button = driver.find_element("css selector", "[aria-label='Review your application']")
                            next_button.click()
                            time.sleep(3)
                            fin_button = driver.find_element("css selector", "[aria-label='Submit application']")
                            fin_button.click()
                            time.sleep(3)

                elif submit_button.text == 'Submit application':
                    resume_button = driver.find_element("css selector", "[aria-label='Choose Resume']")
                    resume_button.click()
                    submit_button.click()
                    time.sleep(3)
                else:
                    close_button = driver.find_element("class name", "artdeco-modal__dismiss")
                    close_button.click()
                    time.sleep(5)
            #make sure window is closed
            try:
                check_close_btn = driver.find_element("class name", "artdeco-modal__dismiss")
                check_close_btn.click()
                try:
                    time.sleep(5)
                    save_button = driver.find_elements("class name", "artdeco-modal__confirm-dialog-btn")[1]
                    save_button.click()
                except :
                    pass
            except NoSuchElementException:
                pass
        except NoSuchElementException:
            print("No application button, skipped.")
            try:
                check_close_btn = driver.find_element("class name", "artdeco-modal__dismiss")
                check_close_btn.click()
                try:
                    time.sleep(5)
                    save_button = driver.find_elements("class name", "artdeco-modal__confirm-dialog-btn")[1]
                    save_button.click()
                except :
                    pass
            except NoSuchElementException:
                pass
            continue
    driver.find_elements("xpath", f"//button[@aria-label='Page {page}']")[0].click()
    page += 1
time.sleep(5)
driver.quit()