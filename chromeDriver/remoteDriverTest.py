import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.file_detector import LocalFileDetector
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys


def test_start_remote():
    # Replace 'HUB_IP' with the actual IP address or hostname of your hub
    hub_url = "http://localhost:4444/wd/hub"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "~/dev/Chrome/Google Chrome.app/Contents/MacOS/Google Chrome"
    #capabilities = DesiredCapabilities.CHROME.copy()
    #capabilities['chromeOptions'] = {'binary': "/Users/sami/dev/Chrome"}
    driver = webdriver.Remote(command_executor=hub_url, options=chrome_options    )#desired_capabilities=capabilities)
    # Now you can use 'driver' to interact with the remote Chrome browser
    driver.get("https://www.bing.com")    # Close the browser

    # Find the search input field by name (you can use other methods to locate the element)
    search_input = driver.find_element(By.CSS_SELECTOR, '#sb_form_q')

    # Type a search query 
    search_input.send_keys('selenium')

    # Press Enter
    search_input.send_keys(Keys.RETURN)

    # Wait for a while to see the results (you might want to use explicit waits in a real scenario)
    driver.implicitly_wait(5)
    #driver.quit()
    print("test success")
if __name__ == '__main__':
    test_start_remote()