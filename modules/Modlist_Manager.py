import os
import json
import sys
from time import sleep
from termcolor import colored

CheckForUpdates = "yes"
MakeModList = "no"
UseProxies = "yes"
RandomUserAgent = "yes"
TimeOut = "10"
DiscordRPC = "yes"

# Check if the file exists. If it exists the data is being read and if it doesn't exist it will be created
def Reader():
    if os.path.exists(".\config.json"):
        with open(".\config.json", "r") as config_reader:
            config = json.load(config_reader)
            CheckForUpdates = config['app_settings']['updatechecker']
            MakeModList = config['app_settings']['makemodlist']
            UseProxies = config['app_settings']['use_proxies']
            RandomUserAgent = config['app_settings']['randomuseragent']
            TimeOut = config['app_settings']['timeout']
            DiscordRPC = config['app_settings']['discordrpc']
        return CheckForUpdates, MakeModList, UseProxies, RandomUserAgent, TimeOut, DiscordRPC
    elif not os.path.exists(".\config.json"):
        print(colored("No Modlist with this name found!", "yellow"))

CheckForUpdates, MakeModList, UseProxies, RandomUserAgent, Timeout, DiscordRPC = Reader()

def Writer():
    print("Modlist Name?")
    name = input(">> ")
    print("Modlist Description?")
    desc = input(">> ")
    print("Modlist Version? (e.g. 1.0.0)")
    ver = input(">> ")
    print("Modlist Author? (I would recommend to add your discord name and id)")
    auth = input(">> ")
    print("Modlist Source?")
    src = input(">> ")

    settings = {
        "name": "{name}",
        "desc": "{desc}",
        "version": "{ver}",
        "author": "{auth}",
        "source": "{src}",
        "mods": []
    }

    create = json.dumps(settings, indent = 4)
    with open("config.json", "w") as modlist_writer:
        modlist_writer.write(create)
