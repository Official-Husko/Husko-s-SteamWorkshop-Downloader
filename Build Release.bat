FOR /F "tokens=* USEBACKQ" %%F IN (`powershell -Command "[guid]::NewGuid().ToString()"`) DO (
SET var=%%F
)
ECHO %var%
pyinstaller --onefile --icon "icon.ico" --console --name "Huskos SteamWorkshop Downloader" --key "%var%" --add-data="C:/Python310/Lib/site-packages/grapheme/data/*;grapheme/data/" bot.py