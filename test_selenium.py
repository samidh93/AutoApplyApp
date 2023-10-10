from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import os
import csv
import time
from collections.abc import Iterable
from googletrans import Translator
# Abstract base class for Divss
from concurrent.futures import ThreadPoolExecutor
import threading
from jobApp.jobEngine.linkedin.linkedinSeleniumBase import LinkedinSeleniumBase

def process_elem(elem: WebElement):
    try:
        # Sleep for 3 seconds (adjust as needed)
        time.sleep(3)
        # Print the text of the element and the thread name
        print("Element Text:", elem.text)
        print("Thread Name:", threading.current_thread().name)
        # Try to find an input element inside 'elem', and if not found, try to find a textarea
        input_element = None
        try:
            input_element = elem.find_element(By.TAG_NAME, "input")
        except:
            try:
                input_element = elem.find_element(By.TAG_NAME, "textarea")
            except:
                pass

        if input_element:
            # Sleep for 10 seconds (adjust as needed)
            time.sleep(5)
            # Send keys to the input element
            input_element.send_keys("abcdef")
        else:
            print("No input or textarea element found inside the element.")
    except Exception as e:
        print("Error processing element:", str(e))

# Define the fill_data function
def fill_data(data_in):
    # Initialize the Selenium WebDriver (you may need to specify the path to your driver)
    linkObj = LinkedinSeleniumBase(linkedin_data=data_in)
    driver = linkObj.driver
    driver.keep_alive = True
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSdMxDauEatgZGCVoAG3XGuDaCFs9emRPSx9hLUkgtTOf47pqg/viewform")
    try:
        listElems = driver.find_elements(By.XPATH, '//div[@class="Qr7Oae" and @role="listitem"]')
        # Create a ThreadPoolExecutor with a specified number of threads
        max_threads = 2  # You can adjust the number of threads as needed
        with ThreadPoolExecutor(max_threads) as executor:
            # Submit tasks to the ThreadPoolExecutor
            for elem in listElems:
                executor.submit(process_elem, elem)
    except:
        print("error")


if __name__ == "__main__":
    applyReq = {
        "user": {
            "email": "dhiebzayneb89@gmail.com",
            "password": "8862468@",
            "_owner": "_owner",
            "field_id": "id",
            "created_date": "created_date",
        },
        "search_params": {
            "job": "project manager",
            "location": "Germany",
        },
        "candidate": {
            "firstname": "zayneb",
            "lastname": "dhieb",
            "gender": "female",
            "resume": "https://708f8437-9497-45e7-a86f-8a969c24d91c.usrfiles.com/ugd/4b8c91_0cd5bf0096924bb6990c679beeaa257c.pdf",
            "phone_number": "+4915731294281",
            "address": {
                "street": "coppistr",
                "city": "berlin",
                "plz": "10365"
            },
            "limit": "20",
            "visa_required": "yes",
            "years_experience": "5",
            "desired_salary": "50000",
            "experiences":   [
                {
                    "job_title": "engineer",
                    "company": "google",
                    "duration": "2 years"
                }
            ],
            "educations": [
                {
                    "university": "tu",
                    "degree": "master",
                    "duration": "2 years"
                }
            ],
            "skills":   {
                "Languages":
                    {
                        "english": "advanced",
                        "german": "basic"
                    },
                "Softwares":
                    {
                        "ms_word": "good",
                        "powerpoint": "basic",
                        "sql": "good"
                    }
            }
        }
    }
    fill_data(applyReq)
    while True:
        time.sleep(5)