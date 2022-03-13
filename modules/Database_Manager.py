import json
import os

official_database = None
custom_database = None

# This system is currently rather empty until i find a way to make it correct to load custom databases aside of the official one

def Database_System():
    if os.path.exists("./official_database.json"):
        with open("./official_database.json", "r") as database_reader:
            official_database = json.load(database_reader)
        return official_database

official_database = Database_System()