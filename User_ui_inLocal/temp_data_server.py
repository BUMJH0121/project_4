from flask import Flask, request, render_template, jsonify
import requests
from pymongo import MongoClient
import json

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():
    temp = ""
    if request.method == 'POST':
        temp = request.data
        print(type(temp), temp)
    return {"name": "temp", "region":"인사동"}

@app.route('/data')
def get_data():
    res = requests.get("http://127.0.0.1:5000/mongo")
    data = json.loads(res.text)
    return "{}".format(data)

# @app.route('/mongo')
# def mongoTest():
#     client = MongoClient('mongodb://localhost:27017/')
#     db = client.test
#     collection = db.seoul
#     results = collection.find()
#     temp = []
#     for r in results:
#         temp.append(r)
#     return "{}".format(temp)


if __name__ == '__main__':
    app.run(port=26030, debug=True)