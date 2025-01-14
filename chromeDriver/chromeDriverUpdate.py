import os
import platform
import requests
import zipfile
import shutil
from pathlib import Path
import json


class ChromedriverManager:
    def __init__(self):
        self.json_url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
        self.chrome_path = ""
        self.chromedriver_path = ""
        self.config_file = self.config_json_path_resolve()
        self.os_platform = "mac"

    def determine_platform(self):
        self.os_platform = platform.system().lower()

        if self.os_platform == "darwin":
            return "mac-x64" if platform.machine() == "x86_64" else "mac-arm64"
        elif self.os_platform == "windows":
            return "win32" if platform.architecture()[0] == "32bit" else "win64"
        elif self.os_platform == "linux":
            return "linux64"
        else:
            return None
        
    def get_latest_stable_version(self):
        try:
            response = requests.get(self.json_url)
            response.raise_for_status()
            data = response.json()

            if 'channels' in data and 'Stable' in data['channels']:
                stable_channel = data['channels']['Stable']

                # Fetch the latest stable version
                return stable_channel['version']

        except requests.exceptions.RequestException as e:
            print(f"Error fetching JSON data: {e}")
            return None

    def find_chromedriver_recursive(self, folder):
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.startswith("chromedriver"):
                    return os.path.join(root, file)
        return None

    def get_chromedriver_url(self, version, platform):
        try:
            response = requests.get(self.json_url)
            response.raise_for_status()
            data = response.json()

            if 'channels' in data and 'Stable' in data['channels']:
                stable_channel = data['channels']['Stable']

                if 'downloads' in stable_channel and 'chromedriver' in stable_channel['downloads']:
                    chromedriver_downloads = stable_channel['downloads']['chromedriver']

                    for entry in chromedriver_downloads:
                        if entry['platform'] == platform:
                            return entry['url']

        except requests.exceptions.RequestException as e:
            print(f"Error fetching JSON data: {e}")

        return None

    def download_chrome_for_testing(self, version, platform):
        url = self.get_chrome_for_testing_url(version, platform)

        if not url:
            print(
                f"Chrome for Testing for version {version} and platform {platform} not found.")
            return

        response = requests.get(url)
        zip_filename = f"{self.os_platform}/chrome_for_testing_{version}_{platform}.zip"
        extract_folder = f"{self.os_platform}/"

        # Use absolute paths to ensure correct directory handling
        script_directory = os.path.dirname(os.path.abspath(__file__))
        zip_filepath = os.path.join(script_directory, zip_filename)
        extract_folder_path = os.path.join(script_directory, extract_folder)
        self.chrome_path = extract_folder_path
        with open(zip_filepath, 'wb') as zip_file:
            zip_file.write(response.content)

        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            # Extract directly to the desired location without creating an extra folder
            zip_ref.extractall(extract_folder_path)

            # Clean up - remove the downloaded zip file and unnecessary extraction folder
            os.remove(zip_filepath)
            #shutil.rmtree(extract_folder_path)

            print(
                f"Chrome for Testing {version} for {platform} downloaded and added to the system PATH successfully.")

    def download_chromedriver(self, version, platform):
        url = self.get_chromedriver_url(version, platform)

        if not url:
            print(
                f"Chromedriver for version {version} and platform {platform} not found.")
            return

        response = requests.get(url)
        zip_filename = f"{self.os_platform}/chromedriver_{version}_{platform}.zip"
        extract_folder = f"{self.os_platform}/chromedriver_{version}_{platform}"

        # Use absolute paths to ensure correct directory handling
        script_directory = os.path.dirname(os.path.abspath(__file__))
        zip_filepath = os.path.join(script_directory, zip_filename)
        extract_folder_path = os.path.join(script_directory, extract_folder)

        with open(zip_filepath, 'wb') as zip_file:
            zip_file.write(response.content)

        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            # Extract directly to the desired location without creating an extra folder
            zip_ref.extractall(extract_folder_path)

        old_chromedriver_executable = self.find_chromedriver_recursive(
            os.path.abspath(__file__))
        # just remove old version
        if old_chromedriver_executable:
            os.remove(old_chromedriver_executable)

        chromedriver_executable = self.find_chromedriver_recursive(
            extract_folder_path)

        if chromedriver_executable:
            # Move Chromedriver executable to the script's directory
            self.chromedriver_path = shutil.move(
                chromedriver_executable, extract_folder_path)

            # Clean up - remove the downloaded zip file and unnecessary extraction folder
            os.remove(zip_filepath)
            #shutil.rmtree(extract_folder_path)

            print(
                f"Chromedriver {version} for {platform} downloaded and moved to the script's directory successfully.")
        else:
            print(
                f"Chromedriver executable not found in {extract_folder_path}. Cleanup skipped.")



    def get_chrome_for_testing_url(self, version, platform):
        try:
            response = requests.get(self.json_url)
            response.raise_for_status()
            data = response.json()

            if 'channels' in data and 'Stable' in data['channels']:
                stable_channel = data['channels']['Stable']

                if 'downloads' in stable_channel and 'chrome' in stable_channel['downloads']:
                    chrome_downloads = stable_channel['downloads']['chrome']

                    for entry in chrome_downloads:
                        if entry['platform'] == platform:
                            return entry['url']

        except requests.exceptions.RequestException as e:
            print(f"Error fetching JSON data: {e}")

        return None

    def config_json_path_resolve(self):

      # Read the JSON file
        # Get the directory of the current script
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Navigate to the parent directory (assuming you want to go up one level)
        parent_directory = os.path.dirname(script_directory)

        # Construct the file path to the JSON file
        json_file_path = os.path.join(
            parent_directory, 'jobApp', 'secrets', 'config.json')

        print("config json at: ", json_file_path)
        return json_file_path

    def update_config_driver_paths(self):
        try:
         # Assign the file path to the class attribute
            chrome_path_key = "browser_bin_location"
            chrome_path_value = self.chrome_path
            chromedriver_path_key = "driver_path"
            chromedriver_path_value = self.chromedriver_path
            with open(self.config_file, 'r') as file:
                data = json.load(file)
                # Update the variable value
                if chrome_path_key in data["driver"] and chromedriver_path_key in data["driver"]:
                    data["driver"][chrome_path_key] = chrome_path_value
                    data["driver"][chromedriver_path_key] = chromedriver_path_value
                else:
                    print(
                        f"Variables '{chrome_path_key}' or {chromedriver_path_key} not found in the JSON file.")
                # Write the updated JSON back to the file
                with open(self.config_file, 'w') as file:
                    json.dump(data, file, indent=2)
                print(
                    f"Updated '{chrome_path_key}' to '{chrome_path_value}' in '{self.config_file}'.")
                print(
                    f"Updated '{chromedriver_path_key}' to '{chromedriver_path_value}' in '{self.config_file}'.")
        except Exception as e:
            print(f"Error updating JSON file: {e}")

    def download_and_configure(self):

        version = self.get_latest_stable_version()
        platform = self.determine_platform()
        if version and platform:
            self.download_chrome_for_testing(version, platform)
            self.download_chromedriver(version, platform)
        self.update_config_driver_paths()

if __name__ == "__main__":
    chromedriver_manager = ChromedriverManager()
    chromedriver_manager.download_and_configure()



