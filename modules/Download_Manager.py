from cgi import test
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

def downloader(MakeModList):
    if MakeModList == "yes":
        print(MakeModList)
        counter = 0
        filename = config_names.get(game) + "_modlist{}.txt"
        while os.path.isfile(filename.format(counter)):
            counter += 1
        filename = filename.format(counter)
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
            config2()
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
            downloader()
        amount = str(len(collection))
        if int(amount) <= 1:
            collection.clear()
        if int(app_id) != int(game):
            print(colored("You Tried to download a mod for a different game then you selected!", "red"))
            sleep(3)
            game_selection()
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
        if not_supported == True:
            destination = 'manual/' + safe_name
            if not os.path.exists('manual'):
                os.makedirs('manual')
        else:
            destination = 'temp/' + safe_name