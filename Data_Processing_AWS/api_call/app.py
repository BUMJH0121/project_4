from flask import Flask, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)


@app.route('/data/bus_location', methods=['GET', 'POST'])
def index():
    url = "http://18.206.167.14:20000/data/mysql"

    # url으로 제공되는 json을 dataframe으로 저장
    bus_df = pd.read_json(url)
    xcode = np.array(bus_df['xcode'].tolist())
    ycode = np.array(bus_df['ycode'].tolist())
    location = {}
    for i in range(len(xcode)):
        location[i] = {"xcode": xcode[i],
                    "ycode": ycode[i]}
    return jsonify(location)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
