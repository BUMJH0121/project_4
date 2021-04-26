from flask import Flask,jsonify,request, render_template
from data_convert import *
import requests
import json
import ujson
import pandas as pd
import numpy as np


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

global res_json
# @app.route('/tmp', methods=['POST', 'GET'])
# def tmp():
#     if request.method == 'POST':
#         res_json = json.loads(request.data)
#         print(res_json)
#     data = requests.get('http://52.73.176.237:5000/data/bus_location')
#     return render_template("convert.html", value = jsonify(data))

@app.route('/user_input', methods=['POST'])
def user_input():
    if request.method == 'POST':
        global res_json
        res_json = json.loads(request.data)
    return json.dumps(d_records, ensure_ascii=False)

#@app.route('/data/bus_location', methods=['GET', 'POST'])
#def bus_stop():
#    url = "http://18.206.167.14:20000/data/mysql"

#    bus_df = pd.read_json(url)
#    xcode = np.array(bus_df['xcode'].tolist())
#    ycode = np.array(bus_df['ycode'].tolist())
#    location = {}
#    for i in range(len(xcode)):
#        location[i] = {"xcode": xcode[i],
#                    "ycode": ycode[i]}
#    return jsonify(location)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
