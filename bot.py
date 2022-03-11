from socket import timeout
from time import sleep
from tkinter import E
import requests
import random
import ctypes
import os
import configparser
import json
import zipfile
import shutil
from pypresence import Presence
from termcolor import colored
from alive_progress import alive_bar
import datetime
import sys
import re

# Defined Variables
global cfg
cfg = configparser.RawConfigParser()
version = "1.5"
threads = 1
get_date = datetime.datetime.now()
month = get_date.month
collection = []

# Connect to Discord RPC
client_id = '945401698401284116'
try:
    RPC = Presence(client_id)
    RPC.connect()
    discord_active = 1
except:
    discord_active = 0

# Check if folder exists else create it
if os.path.exists('temp'):
    shutil.rmtree('temp', ignore_errors=True)
    os.makedirs('temp')
elif not os.path.exists('temp'):
    os.makedirs('temp')

if not os.path.exists('configs'):
    os.makedirs('configs')

chrome_win = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
firefox_lin = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0"
safari_osx = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
    
# Checking for updates on startup
def update_checker():
    os.system('cls')
    import platform
    op_sys = platform.system()
    if op_sys == 'Windows':
        header = "User-Agent':'"+chrome_win
    elif op_sys == 'Darwin':
        header = "User-Agent':'"+safari_osx
    elif op_sys == 'Linux':
        header = "User-Agent':'"+firefox_lin
    else
        header = "User-Agent':'"+chrome_win # we don't want to set no user agent if someone's using another OS
    git_up = "https://api.github.com/repos/Official-Husko/Husko-s-SteamWorkshop-Downloader/releases/latest"
    latest = requests.get(git_up,headers={"User-Agent":header}).text
    git_data = json.loads(latest)
    cv = str(git_data.get('tag_name'))
    u_info = str(git_data.get('body'))
    dir_url = str(git_data['assets'][0]['browser_download_url'])
    updt_name = str(git_data.get('name'))
    updt_rel = str(git_data.get('published_at'))
    if float(version) < float(cv):
        if discord_active == 1:
            RPC.update(state="Updating Downloader to " + cv,buttons=[{"label": "GitHub", "url": "https://github.com/Official-Husko/Husko-s-SteamWorkshop-Downloader"},],small_text="Updating",small_image="update",large_image="bridge")
        print(colored("A new Update is available!", "green"))
        print("")
        print("Name: " + colored(updt_name, "green"))
        print("Version: " + colored(cv, "green"))
        print("Released: " + colored(updt_rel.strip("tz"), "green"))
        print("")
        print("")
        print("==================<[ " + colored("What's New ", "green") + "]>==================")
        print(u_info)
        print("")
        sleep(3)
        print("Download Update? (Y/n)")
        fetch_u = input(">> ")
        if fetch_u == "y" or fetch_u == "Y":
            if not os.path.exists('update'):
                os.makedirs('update')
            fetch = requests.get(dir_url,headers={"User-Agent":header},stream=True)
            file_path = os.path.join("update/","Huskos SteamWorkshop Downloader.exe")
            file = open(file_path, 'wb')
            with alive_bar(int(int(fetch.headers.get('content-length')) / 1024 + 1), title="Downloading Update") as bar:
                for chunk in fetch.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                        file.flush()
                        bar()
                file.close()
            print("")
            print("The Update has been downloaded into the update folder in your directory. the bot will close so you can replace the old exe with the new one. This will not delete any of the configs!")
            sleep(5)
            sys.exit(0)
        else:
            print("Proceeding to Downloader")
            sleep(3)
            proxy_scraper(cfg)
    else:
        proxy_scraper(cfg)

# Set CMD Title
ctypes.windll.kernel32.SetConsoleTitleW("Husko's Steam Workshop Downloader | v" + version)

def game_selection(cfg):
    if discord_active == 1:
        RPC.update(state="Selecting a Game",buttons=[{"label": "GitHub", "url": "https://github.com/Official-Husko/Husko-s-SteamWorkshop-Downloader"},],small_text="Game Selection",small_image="selection",large_image="bridge")
    os.system('cls')
    print(colored("======================================================================================================================", "red"))
    print(colored("|                                                                                                                    |", "red"))
    print(colored("|     " + colored("Product: ", "white") + colored("Husko's Steam Workshop Downloader", "green") + colored("                                                                     |", "red"), "red"))
    print(colored("|     " + colored("Version: ", "white") + colored(version, "green") + colored("                                                                                                   |", "red"), "red"))
    print(colored("|     " + colored("Description: ", "white") + colored("Download and Install SteamWorkshop mods with a few simple clicks.", "green") + colored("                                 |", "red"), "red"))
    print(colored("|                                                                                                                    |", "red"))
    print(colored("======================================================================================================================", "red"))
    print("")
    print("Supported Games: " + colored(str(len(supported_games)), "green"))
    print("")
    print("Please Enter a App ID")
    global game
    global not_supported
    try:
        game = int(input(">> "))
    except ValueError:
        print(colored("Please enter a correct App ID", "red"))
        sleep(3)
        game_selection(cfg)
    if game in supported_games:
        not_supported = False
        check_config(cfg)
    else:
        print("")
        print(colored("This game has not yet received a special installation instruction in this Tool. I will be downloaded but it won't be installed automatically!", "yellow"))
        sleep(7)
        not_supported = True
        config(cfg)

def config(cfg):
    os.system('cls')
    print(colored("======================================================================================================================", "red"))
    print(colored("|                                                                                                                    |", "red"))
    print(colored("|     " + colored("Product: Husko's Steam Workshop Downloader", "white") + colored("                                                                     |", "red"), "red"))
    print(colored("|     " + colored("Version: ", "white") + version + colored("                                                                                                   |", "red"), "red"))
    print(colored("|     " + colored("Description: Download and Install SteamWorkshop mods with a few simple clicks.", "white") + colored("                                 |", "red"), "red"))
    print(colored("|                                                                                                                    |", "red"))
    print(colored("======================================================================================================================", "red"))
    print("")
    global mods
    global proxies
    global rua
    global timeout
    if not_supported == False:
        print("-----------<[ Using the Following Config: " + config_names.get(game) + "_config.ini ]>-----------")
        configFilePath = "configs/" + config_names.get(game) + "_config.ini"
        cfg.read(configFilePath)
        mods = cfg.get('Default', 'ModsPath')
        proxies = cfg.get('Default', 'Proxies')
        rua = cfg.get('Default', 'RandomUserAgent')
        timeout = cfg.getint('Default', 'TimeOut')
        print("Game: " + colored(game_names.get(game), "green"))
        print("App ID: " + colored(game, "green"))
        print("Mods Path: " + colored(mods, "green"))
    else:
        print("-----------<[ Using the Following Config: default_config.ini ]>-----------")
        print("Game: " + colored("Unknown", "green"))
        print("App ID: " + colored(game, "green"))
        print("Mods Path: " + colored("Manual Installation", "green"))
        timeout = 10
        proxies = "yes"
        rua = "yes"
    print("Gather & Use Proxies: " + colored(proxies, "green"))
    print("Randomize User-Agents: " + colored(rua, "green"))
    print("Connection TimeOut: " + colored(str(timeout) + " Seconds", "green"))
    print("Proxies Loaded: " + colored(str(len(proxy_list)), "green"))
    print("")
    print("Please Enter the Workshop Link")
    if discord_active == 1:
        RPC.update(state="Looking for a mod to Download",buttons=[{"label": "GitHub", "url": "https://github.com/Official-Husko/Husko-s-SteamWorkshop-Downloader"},],small_text=game_names.get(game),small_image=config_names.get(game),large_image="bridge")
    config2(cfg)


def config2(cfg):
    if discord_active == 1:
        RPC.update(state="Looking for a mod to Download",buttons=[{"label": "GitHub", "url": "https://github.com/Official-Husko/Husko-s-SteamWorkshop-Downloader"},],small_text=game_names.get(game),small_image=config_names.get(game),large_image="bridge")
    global id
    global xid
    xid = input(">> ")
    if "https://steamcommunity.com/workshop/filedetails/?id=" in xid:
        xxid = xid.strip("https://steamcommunity.com/workshop/filedetails/?id=")
    elif "https://steamcommunity.com/sharedfiles/filedetails/?id=" in xid:
        xxid = xid.strip("https://steamcommunity.com/sharedfiles/filedetails/?id=")
    else:
        print(colored("Something Went Wrong! Either wrong workshop URL or another error.", "red"))
        sleep(5)
        config2(cfg)
    id = re.match(r"(.*\d+)", xxid).group()
    if id.isnumeric() == False:
        print(colored("Something Went Wrong! Either wrong workshop URL or another error.", "red"))
        sleep(3)
        config2(cfg)
    else:
        collection.append(id)
        downloader(cfg)

def downloader(cfg):
    for id in collection:
        backend = ["node01","node02","node03","node04","node05"]
        bd = random.choice(backend)
        header = "User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"
        url = "https://" + bd + ".steamworkshopdownloader.io/prod/api/details/file"
        mod_id = "[" + id + "]"
        if rua == "yes":
            header = random.choice(user_agents)
        if proxies == "yes":
            proxy = random.choice(proxy_list)
            proxyy = {"http":proxy}
            page = requests.post(url,headers={"User-Agent":header},proxies=proxyy,timeout=timeout,data=mod_id).text
        else:
            page = requests.post(url,headers={"User-Agent":header},timeout=timeout,data=mod_id).text
        if page == "[]":
            print(colored("Mod Not Found. If this seems to be a mistake please open an issue report.", "red"))
            sleep(3)
            config2(cfg)
        data = json.loads(page)
        for i in data:
                pubid = str(i.get('publishedfileid'))
                safe_name = str(i.get('title_disk_safe'))
                fil_name = str(i.get('filename'))
                name = str(i.get('title'))
                app_id = str(i.get('consumer_appid'))
                dformat = str(i.get('download_format'))
                coll = str(i.get('children'))
        if coll != "None" and fil_name != "None" and int(len(collection)) <= 1:
            """if int(len(collection)) <= 1 and ".png" or ".jpg" or ".jpeg" in fil_name:
                collection.clear()""" # Stripped the id out after it "detected" it as a collection but is disabled due to not working as intended
            fcoll = coll.replace("'",'"')
            cdata = json.loads(fcoll)
            for g in cdata:
                tidd = str(g.get('publishedfileid'))
                collection.append(tidd)
            amount = str(len(collection))
            if ".png" or ".jpg" or ".jpeg" in fil_name:
                print("Downloading Collection: " + colored(name, "green") + " with " + colored(str(len(collection)), "green") + " Mods")
                print("")
            downloader(cfg)
        amount = str(len(collection))
        if int(amount) <= 1:
            collection.clear()
        if int(app_id) != int(game):
            print(colored("You Tried to download a mod for a different game then you selected!", "red"))
            sleep(3)
            game_selection(cfg)
        print("Downloading: " + colored(name, "green"))
        if discord_active == 1:
            RPC.update(details="Downloading " + name,buttons=[{"label": "GitHub", "url": "https://github.com/Official-Husko/Husko-s-SteamWorkshop-Downloader"},{"label": "Mod Page", "url": "" + xid +""}],small_text="Stormworks: Build and Rescue",small_image="stormworks",large_image="bridge")
        url2 = "https://" + bd + ".steamworkshopdownloader.io/prod/api/download/request"
        req_data = '{"publishedFileId":' + pubid + ',"collectionId":null,"hidden":false,"downloadFormat":"' + dformat + '","autodownload":false}'
        if proxies == "yes":
            proxy = random.choice(proxy_list)
            proxyy = {"http":proxy}
            page2 = requests.post(url2,headers={"User-Agent":header},proxies=proxyy,timeout=timeout,data=req_data).text
        else:
            page2 = requests.post(url2,headers={"User-Agent":header},timeout=timeout,data=req_data).text
        data2 = json.loads(page2)
        uuid = data2.get('uuid')
        url3 = "https://" + bd + ".steamworkshopdownloader.io/prod/api/download/status"
        check = '{"uuids":["' + uuid + '"]}'
        if proxies == "yes":
            proxy = random.choice(proxy_list)
            proxyy = {"http":proxy}
            page3 = requests.post(url3,headers={"User-Agent":header},proxies=proxyy,timeout=timeout,data=check).text
        else:
            page3 = requests.post(url3,headers={"User-Agent":header},timeout=timeout,data=check).text
        data3 = json.loads(page3)
        status = data3[uuid]['status']
        while status != "prepared":
            sleep(2)
            if proxies == "yes":
                proxy = random.choice(proxy_list)
                proxyy = {"http":proxy}
                page3 = requests.post(url3,headers={"User-Agent":header},proxies=proxyy,timeout=timeout,data=check).text
            else:
                page3 = requests.post(url3,headers={"User-Agent":header},timeout=timeout,data=check).text
            data3 = json.loads(page3)
            status = data3[uuid]['status']
        data4 = json.loads(page3)
        node = data4[uuid]['storageNode']
        spath = data4[uuid]['storagePath']
        url4 = "https://" + node + "/prod//storage/" + spath + "?uuid=" + uuid
        if os.path.exists("temp/" + safe_name + ".zip"):
            os.remove("temp/" + safe_name + ".zip")
        if proxies == "yes":
            r = requests.get(url4,headers={"User-Agent":header},proxies=proxyy,timeout=timeout,stream=True)
        else:
            r = requests.get(url4,headers={"User-Agent":header},timeout=timeout,stream=True)
        file_path = os.path.join("temp/", safe_name + ".zip")
        file = open(file_path, 'wb')
        with alive_bar(int(int(r.headers.get('content-length')) / 1024 + 1)) as bar:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    file.flush()
                    bar()
        file.close()
        zip = "temp/" + safe_name + '.zip'
        destination = 'temp/' + safe_name
        badzip = False
        with zipfile.ZipFile(zip) as zf:
            try:
                zf.extractall(destination)
            except zipfile.BadZipFile:
                print(colored("Received Corrupt Zip File. Try to download the mod again. If the issue persists try to open it manually and if it works report this issue to the mod author else the server sent a corrupt file.", "red"))
                badzip = True
        os.remove("temp/" + safe_name + ".zip")
        if not_supported == True:
            print("You can now proceed to manually install the mod " + colored(name, "green") + " located in the temp folder.")
            print("")
            collection.clear()
            config2(cfg)

        # Stormworks: Build and Rescue
        if int(game) == 573090:

            # Installing Vehicles
            if os.path.exists(destination + "/vehicle.xml") & os.path.exists(destination + "/workshop_preview.png"):
                mod_path = mods + "/vehicles/"
                if not os.path.exists(mod_path):
                    os.makedirs(mod_path)
                os.rename(destination + "/vehicle.xml", destination + "/" + safe_name + ".xml")
                os.rename(destination + "/workshop_preview.png", destination + "/" + safe_name + ".png")
                file_names = os.listdir(destination)
                if os.path.exists(mod_path + safe_name + ".xml"):
                    os.remove(mod_path + safe_name + ".xml")
                if os.path.exists(mod_path + safe_name + ".png"):
                    os.remove(mod_path + safe_name + ".png")
                for file_name in file_names:
                    shutil.move(os.path.join(destination, file_name), mod_path)

             # Installing Addons
            elif os.path.exists(destination + "/playlist") & os.path.exists(destination + "/workshop_preview.png"):
                mod_path = mods + "/missions/"
                if not os.path.exists(mod_path):
                    os.makedirs(mod_path)
                os.rename(destination + "/playlist", destination + "/" + safe_name)
                os.rename(destination + "/workshop_preview.png", destination + "/" + safe_name + ".png")
                file_names = os.listdir(destination)
                if os.path.exists(mod_path + safe_name):
                    shutil.rmtree(mod_path + safe_name, ignore_errors=True)
                if os.path.exists(mod_path + safe_name + ".png"):
                    os.remove(mod_path + safe_name + ".png")
                for file_name in file_names:
                    shutil.move(os.path.join(destination, file_name), mod_path)

        # Project Zomboid
        elif int(game) == 108600:
            mod_path = mods + "/mods/"
            file_names = os.listdir(destination + '/mods')
            for file_name in file_names:
                shutil.rmtree(mod_path + file_name, ignore_errors=True)
                shutil.move(os.path.join(destination + '/mods', file_name), mod_path)
        
        # Hunt and Snare
        elif int(game) == 944330:
            mod_path = mods + safe_name
            if os.path.exists(mod_path):
                shutil.rmtree(mod_path, ignore_errors=True)
            source_dir = 'temp/'
            file_names = os.listdir(source_dir)
            for file_name in file_names:
                shutil.move(os.path.join("temp/", file_name), mod_path)
        
        # Rimworld
        elif int(game) == 294100:
            mod_path = mods
            if not os.path.exists(mod_path):
                os.makedirs(mod_path)
            source_dir = 'temp/'
            file_names = os.listdir(source_dir)
            shutil.rmtree(mod_path + "/" + safe_name, ignore_errors=True)
            for file_name in file_names:
                shutil.move(os.path.join("temp/", file_name), mod_path)

        # Call to Arms - Gates of Hell: Ostfront
        elif int(game) == 400750:
            mod_path = mods + safe_name
            if os.path.exists(mod_path):
                shutil.rmtree(mod_path, ignore_errors=True)
            source_dir = 'temp/'
            file_names = os.listdir(source_dir)
            for file_name in file_names:
                shutil.move(os.path.join("temp/", file_name), mod_path)

        else:
            print("Couldn't Determine mod while installing. Please report this issue to the dev")
        if badzip == True:
            print("Mod " + colored(name, "red") + " Failed to Install!")
        else: 
            print("Mod " + colored(name, "green") + " Successfully Installed!")
        print("")
        shutil.rmtree('temp', ignore_errors=True)
        os.makedirs('temp')
    collection.clear()
    config2(cfg)

user_agents = [
"Mozilla/5.0 (Windows NT 6.1 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.2 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
"Mozilla/5.0 (Macintosh Intel Mac OS X 10.10 rv34.0) Gecko/20100101 Firefox/34.0",
"Mozilla/5.0 (Windows NT 6.3 WOW64 rv34.0) Gecko/20100101 Firefox/34.0",
"Mozilla/5.0 (Windows NT 6.1 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
"Mozilla/5.0 (compatible MSIE 8.0 Windows NT 6.1 Trident/5.0)",
"Mozilla/4.0 (compatible MSIE 6.0 Windows NT 5.1 SV1 Media Center PC",
"Mozilla/5.0 (Windows NT 6.2 WOW64 rv34.0) Gecko/20100101 Firefox/34.0",
"Mozilla/5.0 (Windows NT 6.1 WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1",
"Mozilla/5.0 (Windows NT 6.1 WOW64 rv30.0) Gecko/20100101 Firefox/30.0",
"Mozilla/5.0 (Windows NT 6.1 WOW64 Trident/7.0 rv11.0) like Gecko",
"Mozilla/5.0 (Windows NT 6.3 WOW64 Trident/7.0 rv11.0) like Gecko",
"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
"Mozilla/5.0 (compatible MSIE 9.0 Windows NT 6.0 Trident/5.0 Trident/5.0)",
"Mozilla/5.0 (Windows NT 6.3 WOW64 rv41.0) Gecko/20100101 Firefox/41.0",
"Mozilla/5.0 (iPad U CPU OS 5_1 like Mac OS X) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B367 Safari/531.21.10 UCBrowser/3.4.3.532",
"Mozilla/5.0 (Linux Android 11 Samsung SM-A025G) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",
"Mozilla/5.0 (Linux Android 11 SM-A426U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36",
"Mozilla/5.0 (Linux Android 7.0 SM-G930VC Build/NRD90M wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36",
"Mozilla/5.0 (Linux Android 11 SM-M127N) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36",
"Mozilla/5.0 (Linux Android 11 SM-G9910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36",
"Mozilla/5.0 (Linux Android 11 SM-G998W) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36",
"Mozilla/5.0 (Linux Android 6.0.1 Nexus 6P Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36",
"Mozilla/5.0 (Linux Android 11 moto g(10) power Build/RRBS31.Q1-3-34-1-2 wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.105 Mobile Safari/537.36",
"Mozilla/5.0 (Linux Android 10 motorola one 5G ace Build/QZK30.Q4-40-55 wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.152 Mobile Safari/537.36",
"Mozilla/5.0 (Linux Android 10 moto e(7) power Build/QOM30.255-12 wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.101 Mobile Safari/537.36",
"Mozilla/5.0 (Linux Android 11 moto g(50) Build/RRFS31.Q1-59-76-2 wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.159 Mobile Safari/537.36 EdgW/1.0",
"Mozilla/5.0 (Linux Android 10 moto g play (2021)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36",
"Mozilla/5.0 (Linux Android 10 NOH-NX9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
"Mozilla/5.0 (Linux U Android 10 zh-cn BRQ-AN00 Build/HUAWEIBRQ-AN00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/11.9 Mobile Safari/537.36 COVC/045717",
"Mozilla/5.0 (Linux Android 10 Nokia C1 Plus Build/QP1A.190711.020 wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.138 Mobile Safari/537.36",
"Mozilla/5.0 (Linux Android 11 Nokia G10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.88 Mobile Safari/537.36",
"Mozilla/5.0 (Linux Android 11 Nokia G20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.88 Mobile Safari/537.36",
"Mozilla/5.0 (Linux Android 11 V2108) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36",
"Mozilla/5.0 (Linux Android 10 moto e(7) power Build/QOM30.255-12 wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.101 Mobile Safari/537.36",
"Mozilla/5.0 (Linux Android 11 V2045) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36",
"Mozilla/5.0 (Linux Android 11 Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.111 Mobile Safari/537.36",
"Mozilla/5.0 (Linux Android 11 Pixel 4a Build/RP1A.200720.005 wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/84.0.4147.111 Mobile Safari/537.36",
"Mozilla/5.0 (Linux Android 11 M2102J20SG Build/RKQ1.200826.002 wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36",
"Mozilla/5.0 (Linux Android 11 M2103K19PG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Mobile Safari/537.3",
"Mozilla/5.0 (Linux Android 11 M2102K1G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Mobile Safari/537.36"
]

proxy_source_list = [
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/Volodichev/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/roma8ok/proxy-list/main/proxy-list-http.txt"
]

supported_games = [
    573090,
    108600,
    944330,
    294100,
    400750
]

config_names = {
    573090: "stormworks",
    108600: "pz",
    944330: "hunt_snare",
    294100: "rimworld",
    400750: "cta_goh"
}

game_names = {
    573090: "Stormworks: Build and Rescue",
    108600: "Project Zomboid",
    944330: "Hunt and Snare",
    294100: "Rimworld",
    400750: "Call to Arms - Gates of Hell: Ostfront"
}

# Check if the stormworks_config.ini exists else create it
def check_config(cfg):
    if not os.path.exists("configs/" + config_names.get(game) + "_config.ini"):
        cfg.add_section('Default')
        cfg.set('Default', '# Enter the Path to the games mod folder', '')
        cfg.set('Default', 'ModsPath', 'insert-path-here')
        cfg.set('Default', '# if proxies should be scraped and used', '')
        cfg.set('Default', 'Proxies', 'yes')
        cfg.set('Default', '# Seconds Wait time for each request (Default 5)', '')
        cfg.set('Default', 'WaitSeconds', '5')
        cfg.set('Default', '# Randomize User Agent', '')
        cfg.set('Default', 'RandomUserAgent', 'yes')
        cfg.set('Default', '# Request Timeout', '')
        cfg.set('Default', 'TimeOut', '10')
        with open(r"configs/" + config_names.get(game) + "_config.ini", 'w') as configfile:
            cfg.write(configfile)
        configfile.close()
        print("New Config file was generated! Please configure it and then start the bot again")
        sleep(5)
        sys.exit(0)
    config(cfg)

# scrape proxies from a given destination
def proxy_scraper(cfg):
    proxy_source = random.choice(proxy_source_list)
    header = random.choice(user_agents)
    response = requests.get(proxy_source,headers={"User-Agent":header},timeout=10)
    proxy_raw = response.text
    fix_proxy = proxy_raw.split()
    global proxy_list
    proxy_list = fix_proxy
    game_selection(cfg)

if __name__ == '__main__':
    update_checker()

# Credits
#
# h110m - Helping and explaining on how to add a fancy download bar
#
