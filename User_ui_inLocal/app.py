from flask import Flask, request, render_template, jsonify
import requests
from pymongo import MongoClient
import json
import csv

app = Flask(__name__)
region_name_gu = []
region_name_dong = []
with open('./project_4/region_name_gu.csv', newline='') as f:
    reader = csv.reader(f)
    region_name_gu = list(reader)

with open('./project_4/region_name_dong.csv', newline='') as f:
    reader = csv.reader(f)
    region_name_dong = list(reader)

convert_gu = json.dumps(region_name_gu[0], ensure_ascii=False).split(',')
for i in range(len(convert_gu)):
    convert_gu[i] = convert_gu[i].replace('"','').replace('[','').replace(']','').strip()

convert_dong = json.dumps(region_name_dong[0], ensure_ascii=False).split(',')
for i in range(len(convert_dong)):
    convert_dong[i] = convert_dong[i].replace('"','').replace('[','').replace(']','').strip()

region_dict = {}
for i in range(424):
    try:
        region_dict[convert_gu[i]].append(convert_dong[i])
    except:
        temp = [convert_dong[i]]
        region_dict[convert_gu[i]] = temp

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        value = json.dumps(request.form.to_dict(flat=False))
        print(type(value), value)
        requests.post("http://127.0.0.1:26030/", data = value)
    return render_template('index.html', region_json_gu= set(convert_gu), region_json_dong= region_dict)
    # service_json=, year_json=

# @app.route('/data')
# def get_data():
#     return 'HI'

# @app.route('/mongo')
# def mongoTest():
#     client = MongoClient('mongodb://localhost:27017/')
#     db = client.test
#     collection = db.seoul
#     cursor = collection.find()
#     return dumps(cursor, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=True)