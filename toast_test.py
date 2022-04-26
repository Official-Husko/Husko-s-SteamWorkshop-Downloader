from winotify import Notification
import win32gui
import win32con

toast = Notification(app_id="Steamworkshop Downloader",
                     title="Download Finished",
                     msg='Mod "More Loot" Successfully installed!',
                     icon=r"Z:\Projects\Python\Husko's SteamWorkshop Downloader\icon.ico")
toast.add_actions(label="Visit Update Page", 
                  launch="https://github.com/Official-Husko/Husko-s-SteamWorkshop-Downloader/releases/latest")
toast.add_actions(label="Button text 2", 
                  launch="https://github.com/versa-syahptr/winotify/")
toast.show()

window = win32gui.FindWindow("Notepad", None)
if window:
    tup = win32gui.GetWindowPlacement(window)
    if tup[1] == win32con.SW_SHOWMAXIMIZED:
        print("maximized")
    elif tup[1] == win32con.SW_SHOWMINIMIZED:
        print("minimized")
    elif tup[1] == win32con.SW_SHOWNORMAL:
        print("normal")