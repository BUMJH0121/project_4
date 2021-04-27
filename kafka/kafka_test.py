# kafka_test.py
from flask import Flask, jsonify,request
from pymongo import MongoClient
import json
from bson.json_util import dumps
import pymysql

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = flask_restful.Api(app)

config = {
    'host' : '127.0.0.1',
    'user' : 'root',
    'password' : '',
    'database' : 'bus_stop',
    'charset' : 'utf8'
}
'''
@app.route('/data/mongo')
def data():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.test
    collection = db.seoul
    cursor = collection.find()
    return dumps(cursor, ensure_ascii=False)

@app.route('/data/population')
def get():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.population
    collection = db.population_2020
    cursor = collection.find()
    return dumps(cursor, ensure_ascii=False)

@app.route('/data/market_info')
def show_mk():
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

'''
class Bus(flask_restful.Resource):
    def __init__(self):
        self.conn = pymysql.connect(**config)
        self.cursor = self.conn.cursor()
        self.producer = KafkaProducer(bootstrap_servers=['184.73.31.161:9092'])

    def get(self):
        sql = "select * from bus_stop"
        self.cursor.execute(sql)
        row = self.cursor.fetchall()

        data_list = []
        for obj in row:
            data_dic = {
                    'stop_no' : obj[0],
                    'stop_nm' : obj[1],
                    'xcode' : obj[2],
                    'ycode' : obj[3]
            }
            data_list.append(data_dic)

        self.conn.close
        return jsonify(data_list)

    def post(self):
        json_data = request.get_json()
        
        self.producer.send('bus_stop', value=json.dumps(json_data).encode())
        self.producer.flush()

        response = jsonify(json_data)
        response.status_code = 201

        return response

@app.route('/user', methods=['POST'])
def user():
     print(request.data)
     return request.data

api.add_resource(Bus, '/data/mysql')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=20001, debug=True)