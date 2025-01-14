import json
import unittest
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os


class ConfigureChromeDriver:
    def __init__(self, config_file) -> None:
        #script_directory = os.path.dirname(os.path.abspath(__file__))
        self.hub_url = "http://localhost:4444/wd/hub"
        self.config_file = config_file
        self.chrome_options = webdriver.ChromeOptions()
        #self.chrome_options.binary_location = "~/dev/Chrome/Google Chrome.app/Contents/MacOS/Google Chrome"
        self.chrome_services = Service()
        self.add_driver_options_path()
        # Replace the following User-Agent string with the one you want to use
        new_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.139 Safari/537.36"
        self.chrome_options.add_argument(f"user-agent={new_user_agent}")
        self.driver = webdriver.Chrome(options=self.chrome_options, service=Service()) # for testing
        print(f"chrome binary location:  {self.driver.capabilities}")
        #self.driver = webdriver.Remote(command_executor=self.hub_url, options=self.chrome_options    )#desired_capabilities=capabilities)


    def configure_chromedriver_variables(self):
        try:
            # the env variable
            chromedriver_path_key = "driver_path"
            chromedriver_path_value = "usr/bin"
            with open(self.config_file, 'r') as file:
                data = json.load(file)
                # Update the variable value
                if chromedriver_path_key in data["driver"]:
                    data["driver"][chromedriver_path_key] = chromedriver_path_value
                else:
                    print(
                        f"Variables '{chromedriver_path_key} not found in the JSON file.")
                # Write the updated JSON back to the file
                with open(self.config_file, 'w') as file:
                    json.dump(data, file, indent=2)
                print(
                    f"Updated '{chromedriver_path_key}' to '{chromedriver_path_value}' in '{self.config_file}'.")
            return chromedriver_path_value
        except Exception as e:
            print(f"Error updating JSON file: {e}")

    def load_config_json_data(self):
        with open(self.config_file, 'r') as file:
            config = json.load(file)
        return config

    def is_running_on_aws_linux_ec2(self):
        try:
            # Check if the EC2 metadata service is reachable
            response = urllib.request.urlopen(
                "http://169.254.169.254/latest/meta-data/", timeout=5)
            print("running on aws linux ec2 ")
            return True
        except Exception as e:
            return False

    def add_driver_options_path(self):
        # check if runnning on ec2 headless
        self.config = self.load_config_json_data()
        self.debug =self.config.get("driver", {}).get("debug", False)
        print("is debug mode: ", self.debug)
        if self.is_running_on_aws_linux_ec2():
            # load options
            # If running on an EC2 instance, add browser options dynamically
            driver_options = self.config.get("driver", {}).get("options", [])
            # load driver options --arg
            for option in driver_options:
                print(f"option: {option}")
                self.chrome_options.add_argument(option)
            return
        print("not running on ec2, searching for driver path")
        self.chrome_path = self.configure_chromedriver_variables()
        # set the path to driver
        self.chrome_services.path= self.chrome_path
        if self.debug==False:
            self.chrome_options.add_argument("--headless")

if __name__ == '__main__':
    config_file_path = "../jobApp/secrets/config.json"
    driver = ConfigureChromeDriver(config_file_path).driver
    driver.get("https://www.linkedin.com")
    user_agent = driver.execute_script("return navigator.userAgent;")
    print("User-Agent:", user_agent)
