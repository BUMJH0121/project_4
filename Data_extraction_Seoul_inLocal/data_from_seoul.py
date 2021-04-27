import sys
import requests
import json
from pymongo import MongoClient

start_index = str(sys.argv[1])
last_index = str(sys.argv[2])
try:
    year = str(sys.argv[3])
except:
    year = ""

api_key = ""
with open("./key.txt", "r") as f:
     api_key = f.readline()

my_client = MongoClient("mongodb://Mongo:27017/")
db = my_client.test
db.seoul


data = requests.get("http://openapi.seoul.go.kr:8088/{}/json/VwsmTrdhlStorQq/{}/{}/{}".format(api_key ,start_index, last_index, year))
postid = db.seoul.insert_one(data.json()).inserted_id