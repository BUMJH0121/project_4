import requests
import json
from pymongo import MongoClient

client = MongoClient("mongodb://mongo:27017/")

db = client.population
col = db.population_2020

api_key = open("./api_key.txt").readlines()[0].strip()
api = 'http://openapi.seoul.go.kr:8088/{api_key}/json/VwsmTrdarRepopQq/1/1000/2020'

url = api.format(api_key=api_key)
req = requests.get(url).json()

post_id = col.insert_one(req).inserted_id

