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