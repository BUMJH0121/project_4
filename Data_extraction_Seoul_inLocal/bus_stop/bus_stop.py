# -*- conding:utf-8 -*-'
import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import MySQLdb
import pymysql

startpg = 1
endpg = 1000
rows = []
key = '725a71456470616c37314671576f7a'
for _ in range(12):
    url = f"http://openapi.seoul.go.kr:8088/725a71456470616c37314671576f7a/xml/busStopLocationXyInfo/{startpg}/{endpg}"

    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    for i in soup.find_all('row'):
        rows.append({"stop_no": i.stop_no.string,
                     "stop_nm": i.stop_nm.string,
                     "xcode": i.xcode.string,
                     "ycode": i.ycode.string})
    startpg = endpg + 1
    endpg = endpg + 1000

columns = ["stop_no", "stop_nm", "xcode", "ycode"]
bus_stop_df = pd.DataFrame(rows, columns=columns)
# bus_stop_df
# bus_stop_df.to_csv("bus_stop.csv", mode='w', encoding='utf-8-sig', index=False)

engine = create_engine("mysql+mysqldb://root:"+"" +
                       "@bus_stop_db/bus_stop?charset=utf8", encoding='utf8')
conn = engine.connect()

bus_stop_df.to_sql(name='bus_stop', con=engine,
                   if_exists='replace', index=False)
