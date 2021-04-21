:koala: 참고 : https://velog.io/@jwpark06/AWS-EC2%EC%97%90-Kafka-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0

### AWS console

1. ec2 인스턴스의 보안그룹 인바운드 규칙 추가

- 9092, 2181

### Kafka 환경 설정

1. Kafka 설치파일 다운로드

```
ubuntu@ip-172-31-63-57:~$ wget https://archive.apache.org/dist/kafka/2.5.0/kafka_2.12-2.5.0.tgz
```

2. 설치파일 압축 해제

```
ubuntu@ip-172-31-63-57:~$ tar xvf kafka_2.12-2.5.0.tgz
```

3. heap memory 설정 추가
```
ubuntu@ip-172-31-63-57:~$ sudo vi ~/.bashrc
```

```bash
# ~./bashrc
KAFKA_HEAP_OPTS="-Xms400m -Xmx400m"
```

4. kafka 설정 파일 수정 (config/server.properties)
```properties
advertised.listeners=PLAINTEXT://{ec2_instance_address}:9092
zookeeper.connect=localhost:2181
```

5. zookeeper, kafka 실행

```
ubuntu@ip-172-31-63-57:~/kafka_2.12-2.5.0$ bin/zookeeper-server-start.sh -daemon config/zookeeper.properties
ubuntu@ip-172-31-63-57:~/kafka_2.12-2.5.0$ bin/kafka-server-start.sh -daemon config/server.properties
```

6. 실행 확인 

```
ubuntu@ip-172-31-63-57:~/kafka_2.12-2.5.0$ jps -m
8920 QuorumPeerMain config/zookeeper.properties
9368 Jps -m
9273 Kafka config/server.properties
```

<br>

:warning: java 설치 에러 -> java 설치 후 버전 확인

```
ubuntu@ip-172-31-55-25:~/kafka_2.12-2.5.0$ sudo apt install default-jdk
```

```
ubuntu@ip-172-31-55-25:~/kafka_2.12-2.5.0$ java -version
openjdk version "11.0.10" 2021-01-19
OpenJDK Runtime Environment (build 11.0.10+9-Ubuntu-0ubuntu1.18.04)
OpenJDK 64-Bit Server VM (build 11.0.10+9-Ubuntu-0ubuntu1.18.04, mixed mode, sharing)
```

<br>

### 토픽

1. 토픽 생성 

- bus_stop
- market
- (option) population

```
ubuntu@ip-172-31-63-57:~/kafka_2.12-2.5.0$ bin/kafka-topics.sh --create --bootstrap-server 184.73.31.161:9092 --topic bus_stop
```

2. 토픽 목록 확인
```
ubuntu@ip-172-31-63-57:~/kafka_2.12-2.5.0$ bin/kafka-topics.sh --list --bootstrap-server 184.73.31.161:9092
bus_stop
market
population
```

3. (TEST) console-consumer

```
ubuntu@ip-172-31-63-57:~/kafka_2.12-2.5.0$ bin/kafka-console-consumer.sh --topic bus_stop --from-beginning --bootstrap-server 184.73.31.161:9092
```

4. (TEST) console-producer

```
ubuntu@ip-172-31-18-246:~/kafka_2.12-2.5.0$ bin/kafka-console-producer.sh --topic population --bootstrap-server test-broker02:9092
```

consumer-producer 통신

![image](https://user-images.githubusercontent.com/77096463/115344453-68f05e80-a1e8-11eb-8491-9de9b6421957.png)

<br>

### Kafka, DynamoDB 연동

1. kafka_test.py 파일에 bus_stop 토픽에 데이터 전송하는 코드 추가

```python
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
```

2. curl 명령어로 POST 메서드 확인

```
ubuntu@ip-172-31-18-246:~/flask$ curl -d '{
    "stop_nm": "종로2가사거리", 
    "stop_no": "﻿01001", 
    "xcode": "126.9877498816", 
    "ycode": "37.5697651251"
  }' -H "Content-Type: application/json" -X POST http://18.206.167.14:20001/data/mysql
{
  "stop_nm": "종로2가사거리", 
  "stop_no": "﻿01001", 
  "xcode": "126.9877498816", 
  "ycode": "37.5697651251"
}

ubuntu@ip-172-31-18-246:~/flask$ curl -d '{
    "stop_nm": "창경궁.서울대학교병원", 
    "stop_no": "﻿01002", 
    "xcode": "126.9965660023", 
    "ycode": "37.5791830159"
  }' -H "Content-Type: application/json" -X POST http://18.206.167.14:20001/data/mysql
{
  "stop_nm": "창경궁.서울대학교병원", 
  "stop_no": "﻿01002", 
  "xcode": "126.9965660023", 
  "ycode": "37.5791830159"
}
```

3. kafka 서버에서 bus_stop 토픽에 POST 메서드로 전송한 데이터가 저장됨을 확인

```
ubuntu@ip-172-31-55-25:~/kafka_2.12-2.5.0$ bin/kafka-console-consumer.sh --topic bus_stop --from-beginning --bootstrap-server 184.73.31.161:9092
{"stop_no": "\ufeff01001", "xcode": "126.9877498816", "stop_nm": "\uc885\ub85c2\uac00\uc0ac\uac70\ub9ac", "ycode": "37.5697651251"}
{"stop_no": "\ufeff01002", "xcode": "126.9965660023", "stop_nm": "\ucc3d\uacbd\uad81.\uc11c\uc6b8\ub300\ud559\uad50\ubcd1\uc6d0", "ycode": "37.5791830159"}
```

4. DynamoDB의 bus_stop 테이블로 bus_stop 토픽의 데이터 전송하는 코드 작성

```python
# kafka_consumer.py
from kafka import KafkaConsumer
from json import loads
import time
import json
import boto3
import ast

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

consumer = KafkaConsumer('bus_stop',
            bootstrap_servers=['184.73.31.161:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            auto_commit_interval_ms=1000,
            consumer_timeout_ms=1000)

# get bus_stop data
# for data in consumer:
#     topic = data.topic
#     value = data.value
#     print("Topic:{}, Value:{}".format(topic,value))

def get_data():
    batch = consumer.poll(100)
    if len(batch) > 0:
        for data in list(batch.values())[0]:
            value = data.value.decode('utf8')
            data = ast.literal_eval(value)
            print(type(data))

            table = dynamodb.Table('bus_stop')
            response = table.put_item(Item=data)
            
if __name__ == '__main__' :
    get_data()
```

`python kafka_consumer.py` 명령어 실행 시 bus_stop 테이블로 데이터가 들어감을 확인

-> <u>인코딩 문제 해결해야 함</u>

![image](https://user-images.githubusercontent.com/77096463/115520060-b80bc180-a2c4-11eb-9319-7ed85283c9b7.png)

<br>

:pencil: TODO

1. topic으로 데이터 전송 시 인코딩 형식 변경
2. sample data 말고 실제 데이터를 이용해서 bus_stop, market 데이터 모두 kafka로 통신할 수 있도록 설정

