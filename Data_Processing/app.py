from flask import Flask,jsonify,request
import requests

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

@app.route('/user', methods=['POST'])
def home():
    temp = ''
    if request.method == 'POST':
        temp = request.data
        print(type(temp),temp)
        data = requests.post('http://172.31.18.246:20000/user', data=temp)
    return 'Hello, my second site!{}'.format(temp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
