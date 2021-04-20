from flask import Flask,jsonify,request, render_template
import requests
import json
import pandas as pd
import numpy as np

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    return "Hello"

@app.route('/data/mongo')
def mongo_data():
    url = 'http://172.31.18.246:20000/data/mongo'
    res = requests.get(url)
    data = res.json()
    return jsonify(data)

@app.route('/data/mysql')
def mysql_data():
    url = 'http://172.31.18.246:20000/data/mysql'
    res = requests.get(url)
    data = res.json()
    return jsonify(data)

@app.route('/user', methods=['POST', 'GET'])
def home():
    temp = ''
    if request.method == 'POST':
        temp = request.data
        print(type(temp),temp)
        data = requests.get('http://localhost:5000/data/mysql')
    return jsonify(data)


@app.route('/tmp', methods=['POST', 'GET'])
def tmp():
    if request.method == 'POST':
        res_json = json.loads(request.data)
        print(res_json)
    data = requests.get('http://54.156.131.155:5000/data/bus_location')
    return render_template("convert.html", value = jsonify(data))

@app.route('/user_input', methods=['POST'])
def user_input():
    if request.method == 'POST':
        res_json = json.loads(request.data)
    return res_json

@app.route('/data/bus_location', methods=['GET', 'POST'])
def bus_stop():
    url = "http://18.206.167.14:20000/data/mysql"

    bus_df = pd.read_json(url)
    xcode = np.array(bus_df['xcode'].tolist())
    ycode = np.array(bus_df['ycode'].tolist())
    location = {}
    for i in range(len(xcode)):
        location[i] = {"xcode": xcode[i],
                    "ycode": ycode[i]}
    return jsonify(location)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
