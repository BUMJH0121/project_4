from flask import Flask, request, render_template, jsonify
import requests
import json
from data_make_list import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        value = json.dumps(request.form.to_dict(flat=False))
        print(type(value), value)
        requests.post("http://54.156.131.155:5000/", data = value)
        res = requests.get("http://54.156.131.155:5000")
        data = json.loads(res.text)
        return render_template('result.html', data = data)
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