from flask import Flask, jsonify,request
from pymongo import MongoClient
import json
from bson.json_util import dumps
import pymysql
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def home():
    return 'Hello, ec2 here'

# @app.route('/data/mongo')
# def data():
#     client = MongoClient('mongodb://localhost:27017/')
#     db = client.test
#     collection = db.seoul
#     cursor = collection.find()
#     return dumps(cursor, ensure_ascii=False)

@app.route('/data/population')
def get():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.population
    collection = db.population_2020
    cursor = collection.find()
    return dumps(cursor, ensure_ascii=False)

@app.route('/data/market_info')
def show_mk():
    os.system('docker run -d -e')
    conn = pymysql.connect(host='127.0.0.1',port=13306, user='root',password='', db='mysql', charset='utf8')
    sql = ' select * from test'
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchall()
    data_list = []
    for obj in row:
        data_dic = {
                'bizesNm': obj[2],
                'indsMclsNm': obj[7],
                'indsSclsNm':obj[9],
                'signguCd':obj[14],
                'signguNm':obj[15],
                'adongCd':obj[16],
                'adongNm':obj[17],
                'lnoAdr': obj[25],
                'rdnmAdr': obj[32],
                'flrNo':obj[36],
                 'lon':obj[38],
                'lat':obj[39]
                } 
        data_list.append(data_dic)
    conn.close
    return jsonify(data_list)

@app.route('/data/mysql')
def show():
    # client = pymysqlClient('mysqldb://localhost:3306/')
    # db = client.test
    # collection = db.bus_stop
    # cursor = collection.find()
    # return dumps(cursor, ensure_ascii=False)
    conn = pymysql.connect(host='127.0.0.1', user='root',
                           password='', db='bus_stop', charset='utf8')
    sql = '''
        select *
        from bus_stop
    '''

    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchall()

    data_list = []

    for obj in row:
        data_dic = {
            'stop_no': obj[0],
            'stop_nm': obj[1],
            'xcode': obj[2],
            'ycode': obj[3]
        }
        data_list.append(data_dic)
    conn.close
    return jsonify(data_list)

@app.route('/user', methods=['POST'])
def user():
     print(request.data)
     print(json.loads(request.data), type(json.loads(request.data)))
     return request.data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=20000, debug=True)
