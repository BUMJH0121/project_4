from flask import Flask, request, render_template, jsonify
import requests
from pymongo import MongoClient
import json
from bson.json_util import dumps

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        value = request.form
        print(value['region'], value['service'], value['year'])
    return render_template('index.html')

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