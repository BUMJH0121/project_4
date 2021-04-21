import requests
import json

d0a3643f2db2f5870c7b2fd9e900633d
?x=127.1086228&y=37.4012191

res = requests.get('http://34.227.101.182:5000/data/bus_location')
res_json = json.loads(res.text)
bus_to_json = {}
url = "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json"
for key in res_json:
    temp_dict = {}
    temp[]

with open('test.json', 'w', encoding='utf-8') as file:
    json.dump(bus_to_json, file, ensure_ascii=False)