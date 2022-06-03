import subprocess


# Main Downloader Script
class Download_Manager():
    def SteamCMD():
        steamcmd = ['contained\steamcmd.exe','+login anonymous']
        steamcmd.append(f'+workshop_download_item {appid} {workshop_id}')
        #args.append("+quit")
        process = subprocess.run(steamcmd, stdout=subprocess.PIPE, universal_newlines=True)