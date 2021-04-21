from flask import Flask,jsonify,request, render_template
import requests
import json
import ujson
import pandas as pd
import numpy as np

with open("dong_coords.json", "r", encoding="utf-8") as f:
    ddata = json.load(f) 
df = pd.DataFrame(ddata)

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
    data = requests.get('http://52.73.176.237:5000/data/bus_location')
    return render_template("convert.html", value = jsonify(data))

@app.route('/user_input', methods=['POST'])
def user_input():
    if request.method == 'POST':
        res_json = json.loads(request.data)
        data = df[(df['gu'] == f'{res_json["region_gu"][0]}') & (df['dong'] == f'{res_json["region_dong"][0]}')][['lat', 'lng', 'code']]
        d_records = data.to_dict('records')[0]
        d_records['region_gu'] = res_json["region_gu"][0]
        d_records['region_dong'] = res_json["region_dong"][0]

        url = "http://18.206.167.14:20000/data/mysql"
        bus_df = pd.read_json(url)
        with open("./test.json", "r", encoding="utf-8") as f:
            ddata = json.load(f)
        df = pd.DataFrame(ddata)

        data = df[(df['gu'] == f'{res_json["region_gu"][0]}') & (df['dong'] == f'{res_json["region_dong"][0]}')][['xcode', 'ycode']]
        output_df = pd.merge(bus_df, data, on=['xcode', 'ycode'])
        stop_nm = np.array(output_df['stop_nm'].tolist())
        xcode = np.array(output_df['xcode'].tolist())
        ycode = np.array(output_df['ycode'].tolist())
        output = {}
        for i in range(len(stop_nm)):
            output[stop_nm[i]] = {"xcode": ycode[i], "ycode": xcode[i]}
        d_records["bus_stop"] = output
        print(d_records, type(d_records))
        print(json.dumps(d_records, ensure_ascii=False))
    return json.dumps(d_records, ensure_ascii=False)

# @app.route('/data/bus_location', methods=['GET', 'POST'])
# def bus_stop():
#     url = "http://18.206.167.14:20000/data/mysql"

#     bus_df = pd.read_json(url)
#     xcode = np.array(bus_df['xcode'].tolist())
#     ycode = np.array(bus_df['ycode'].tolist())
#     location = {}
#     for i in range(len(xcode)):
#         location[i] = {"xcode": xcode[i],
#                     "ycode": ycode[i]}
#     return jsonify(location)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
