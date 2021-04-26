from flask import Flask,jsonify,request, render_template
from consul_server import *
import requests
import json
import ujson
import pandas as pd
import numpy as np


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# @app.route('/tmp', methods=['POST', 'GET'])
# def tmp():
#     if request.method == 'POST':
#         res_json = json.loads(request.data)
#         print(res_json)
#     data = requests.get('http://52.73.176.237:5000/data/bus_location')
#     return render_template("convert.html", value = jsonify(data))

@app.route('/user_input', methods=['POST', 'GET'])
def user_input():
    if request.method == 'POST':
        res_json = json.loads(request.data)
        with open("dong_coords.json", "r", encoding="utf-8") as f:
            ddata = json.load(f) 
        df = pd.DataFrame(ddata)

        data = df[(df['gu']==(f'{res_json["region_gu"][0]}')) & (df['dong']==(f'{res_json["region_dong"][0]}'))][['lat', 'lng', 'code']]
        d_records = data.to_dict('records')[0]
        d_records['region_gu'] = res_json["region_gu"][0]
        d_records['region_dong'] = res_json["region_dong"][0]

        url = "{}/data/mysql".format(service_url)
        bus_df = pd.read_json(url)
        with open("./test.json", "r", encoding="utf-8") as f:
            ddata = json.load(f)
        bus_stop_df = pd.DataFrame(ddata)

        data = bus_stop_df[(bus_stop_df['gu'].str.contains(f'{res_json["region_gu"][0]}'[:1])) & (bus_stop_df['dong'].str.contains(f'{res_json["region_dong"][0]}'[:1]))][['xcode', 'ycode']]
        output_df = pd.merge(bus_df, data, on=['xcode', 'ycode'])
        stop_nm = np.array(output_df['stop_nm'].tolist())
        xcode = np.array(output_df['xcode'].tolist())
        ycode = np.array(output_df['ycode'].tolist())
        output = {}
        for i in range(len(stop_nm)):
            output[stop_nm[i]] = {"xcode": ycode[i], "ycode": xcode[i]}
        d_records["bus_stop"] = output


        # ----- 사용자 입력에 따른 상권 분석 -----      
        url3 = '{}/data/code_info'.format(service_url)
        res3 = requests.get(url3)
        data3 = res3.json()
        code_df = pd.DataFrame(data3)
        code = code_df[code_df['dong'] == f'{res_json["region_dong"][0]}']['code'].drop_duplicates()
        requests.post('{}/user'.format(service_url), data = str(code.values[0]))

        url2 = '{}/data/market_info'.format(service_url)
        res2 = requests.get(url2)
        data2 = res2.json()

        df2 = pd.DataFrame(data2)
        # 비교 (수정필요)
        output2_df = df2[(df2['adongNm'] == f'{res_json["region_dong"][0]}') & (
        df2['indsMclsNm'] == f'{res_json["service"][0]}')][['bizesNm', 'lnoAdr']]

        store_name = np.array(output2_df['bizesNm'].tolist())
        address = np.array(output2_df['lnoAdr'].tolist())
        output2 = []
        for i in range(len(store_name)):
            output2.append({"store_name": store_name[i],"address": address[i]})
        d_records["service"] = output2
        return json.dumps(d_records, ensure_ascii=False)
    elif request.method == 'GET':
        return "OK"
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
