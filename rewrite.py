from modules import Proxy_Manager, Config_Manager, Database_Manager
import random
from termcolor import colored
import os

os.system("cls")

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

header = random.choice(user_agents)
cm = Config_Manager.Reader()
pm = Proxy_Manager.Scraper(header, Config_Manager.UseProxies)
dbm = Database_Manager.Database_System()


#print(Database_Manager.custom_database)
#print(Database_Manager.official_database)
print("Proxies Loaded: " + colored(str(len(Proxy_Manager.proxy_list)), "green"))
print("Check For Updates: ", colored(Config_Manager.CheckForUpdates, "green"))
print("Check For Updates: ", colored(Config_Manager.MakeModList, "green"))
print("Check For Updates: ", colored(Config_Manager.UseProxies, "green"))
print("Check For Updates: ", colored(Config_Manager.RandomUserAgent, "green"))
print("Check For Updates: ", colored(Config_Manager.TimeOut, "green"))