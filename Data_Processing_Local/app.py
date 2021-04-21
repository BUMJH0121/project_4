from flask import Flask,jsonify,request, render_template
import requests
import json
import ujson
import pandas as pd

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


@app.route('/user_input', methods=['POST'])
def user_input():
    if request.method == 'POST':
        res_json = json.loads(request.data)
        data = df[(df['gu'] == f'{res_json["region_gu"][0]}') & (df['dong'] == f'{res_json["region_dong"][0]}')][['lat', 'lng', 'code']]
        d_records = data.to_dict('records')[0]
        d_records['region_gu'] = res_json["region_gu"][0]
        d_records['region_dong'] = res_json["region_dong"][0]
        print(d_records, type(d_records))
    return json.dumps(d_records, ensure_ascii=False)

# @app.route('/tmp', methods=['POST', 'GET'])
# def tmp():
#     if request.method == 'POST':
#         bus_to_json = json.loads(request.data)
#         with open('test.json', 'w', encoding='utf-8') as file:
#             json.dump(bus_to_json, file, ensure_ascii=False) 
#     res = requests.get('http://34.227.101.182:5000/data/bus_location')
#     res_json = json.loads(res.text)
#     return render_template("convert.html", value = res_json)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=25500, debug=True)
