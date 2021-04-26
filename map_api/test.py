from flask import Flask, request, render_template
import json
import pandas as pd
import numpy as np
import requests

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/tmp', methods=['GET', 'POST'])
def tmp():
    # ----- 지도 중심 좌표 -----
    value = {"xcode": 37.497117,
             "ycode": 127.152393}

    # ----- 사용자 입력(예시) -----
    x = "송파구"
    y = "마천1동"

    # ----- 버스 데이터 읽어오기 -----
    url = "http://18.206.167.14:20000/data/mysql"
    bus_df = pd.read_json(url)

    # ----- 버스 정류장 좌표와 주소 파일 읽기 -----
    with open("./test.json", "r", encoding="utf-8") as f:
        ddata = json.load(f)
    df = pd.DataFrame(ddata)

    # ----- 지역 별로 정류장 데이터 추출 -----
    data = df[(df['gu'] == f'{x}') & (
        df['dong'] == f'{y}')][['xcode', 'ycode']]
    output_df = pd.merge(bus_df, data, on=['xcode', 'ycode'])
    stop_nm = np.array(output_df['stop_nm'].tolist())
    xcode = np.array(output_df['xcode'].tolist())
    ycode = np.array(output_df['ycode'].tolist())
    output = {}
    for i in range(len(stop_nm)):
        output[stop_nm[i]] = {"xcode": ycode[i], "ycode": xcode[i]}
    bus_stop = output
    # print(bus_stop)

    ## 예시 데이터 ##
    # bus_stop = {"카카오": {"xcode": 33.450705, "ycode": 126.570677},
    #             "생태연못": {"xcode": 33.450936, "ycode": 126.569477},
    #             "텃밭": {"xcode": 33.450879, "ycode": 126.56994},
    #             "근린공원": {"xcode": 33.451393, "ycode": 126.570738}}
    ######

    return render_template('test.html', value=value, bus_stop=bus_stop)


@ app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        return render_template("test.html", prediction=result)


if __name__ == "__main__":
    app.run(port=6060, debug=True)
