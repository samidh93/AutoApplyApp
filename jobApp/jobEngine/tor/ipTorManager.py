import requests
import stem.process
from stem.control import Controller
import json
import subprocess
class IpTorManager:
    def __init__(self, tor_json):
        with open(tor_json, "r")as f:
            tor_data = json.load(f)

        self.tor_path = tor_data["tor_path"]
        self.torrc_path = tor_data["torrc_path"]
        self.tor_port = tor_data["tor_port"]
        self.tor_password = tor_data["tor_password"]
        self.proc = None

    def start_tor(self):
        self.proc = stem.process.launch_tor_with_config(
            #tor_cmd=self.tor_path,
            config={
                'ControlPort': '9051',
                #'HashedControlPassword': '16:BF30C69FE1066D5E605B011B5B5B5B5B5B5B5B5B5B5B5B5B5B5B5B5B5B5C9690'
            },
            #torrc_path=self.torrc_path
        )
    def start_tor_proc(self):
        self.proc = subprocess.Popen([self.tor_path])

    def stop_tor(self):
        self.proc.kill()

    def get(self, url):
        with Controller.from_port(port=self.tor_port) as controller:
            controller.authenticate()#password=self.tor_password)
            controller.signal(stem.Signal.NEWNYM)

        print("Current public IP address: {}".format(requests.get('https://api.ipify.org').text))
        response = requests.get(url, proxies={'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'})
        print("New public IP address: {}".format(requests.get('https://api.ipify.org').text))

        return response.text


if __name__ == "__main__":
    # start tor deamon:
    # tor --defaults-torrc path_to_torrc 
    # as a default
    # tor --defaults-torrc "C:/Users/user1/Desktop/Tor Browser/Browser/TorBrowser/Data/Tor/torrc"
    # or copy torrc here "C:/Users/<username>/AppData/Roaming/tor/torrc" 
    tor_config_path = 'jobApp/secrets/tor.json'
    ip_tor_manager = IpTorManager(tor_config_path)
    #ip_tor_manager.start_tor()
    response_text = ip_tor_manager.get("https://linkedin.com")
    r = ip_tor_manager.get("https://indeed.com")
    #ip_tor_manager.stop_tor()

