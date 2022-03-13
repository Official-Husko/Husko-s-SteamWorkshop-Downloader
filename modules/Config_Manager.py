import os
import json
import sys
from time import sleep

# These are the default settings, If the user changed them they will be read and changed
default_settings = {
    "app_settings": {
        "updatechecker": "yes",
        "makemodlist": "no",
        "use_proxies": "yes",
        "randomuseragent": "yes",
        "timeout": "10"
    },
    "game_paths": {}
}

CheckForUpdates = "yes"
MakeModList = "no"
UseProxies = "yes"
RandomUserAgent = "yes"
TimeOut = "10"

# Check if the file exists. If it exists the data is being read and if it doesn't exist it will be created
def Reader():
    os.system("cls")
    if os.path.exists(".\config.json"):
        print("Reading Config...")
        with open(".\config.json", "r") as config_reader:
            config = json.load(config_reader)
            CheckForUpdates = config['app_settings']['updatechecker']
            MakeModList = config['app_settings']['makemodlist']
            UseProxies = config['app_settings']['use_proxies']
            RandomUserAgent = config['app_settings']['randomuseragent']
            TimeOut = config['app_settings']['timeout']
            config_reader.close()
        return CheckForUpdates, MakeModList, UseProxies, RandomUserAgent, TimeOut
    elif not os.path.exists(".\config.json"):
        print("We have detected that this your first time running this tool! We created a new config.json. Please take a minute and configure it then restart the tool.")
        default_create = json.dumps(default_settings, indent = 4)
        with open("config.json", "w") as config_writer:
            config_writer.write(default_create)
        sleep(10)
        sys.exit(0)

CheckForUpdates, MakeModList, UseProxies, RandomUserAgent, Timeout = Reader()

# Class System for later restructure if i will ever find out on how they work
"""class Config:
2	    def __init__(self):
3	        self.options = {"option1": True, "option2": False}
4	
5	    def read_config(filename: str):
6	        with open(filename, "r") as file:
7	            settings = json.load(file)
8	
9	        self.options["option1"] = settings["option1"]"""