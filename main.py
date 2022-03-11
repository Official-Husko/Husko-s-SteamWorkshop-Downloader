import requests
import random
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()
timeout = 10

id = "2674456883"

backend = ["node01","node02","node03","node04","node05"]
bd = random.choice(backend)
header = "User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"
url = "https://" + bd + ".steamworkshopdownloader.io/prod/api/details/file"
mod_id = "[" + id + "]"

@app.get("/")
def read_root():
    return {"Nothing Here Currently"}


@app.get("/mod_info")
def mod_info():
    page = requests.post(url,headers={"User-Agent":header},timeout=timeout,data=mod_id).text
    return JSONResponse(content=page)