import PublicDataReader as pdr
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import sys

pymysql.install_as_MySQLdb()

serviceKey = "rcgDEvIpX2vlg8irJ5WCOqW2wyalpfAkP291lX8CWF1Ox8K%2BkMpiZuVXMwAukT1JUqf9LdqjMEPGzG36GNCxog%3D%3D"
semas = pdr.StoreInfo(serviceKey)

## 입력: 구분ID(시도:ctprvnCd, 시군구:signguCd, 행정동:adongCd)
# 행정구역코드, 상권업종대분류코드, 상권업종중분류코드, 상권업종소분류코드, 페이지 번호
# key: 행정구역코드 -> 시도는 시도코드값, 시군구는 시군구코드값, 행정동은 행정동코드값
# https://www.data.go.kr/tcs/dss/selectFileDataDetailView.do?publicDataPk=15069599
# --> 여기 가면 업종코드 있음
# indsLclsCd: 상권업종 대분류코드


#divId = 'adongCd'
#divId = input("시도:ctprvnCd, 시군구:signguCd, 행정동:adongCd")
divId = "adongCd"
#key = '1168063000'
# key = input("ex) 1168063000: ")
key = sys.argv[1]
indsLclsCd = 'Q'
pageNo = 1

df = semas.storeListInDong(divId = divId, key = key, indsLclsCd_=indsLclsCd, pageNo = pageNo)
print(df)
engine = create_engine('mysql+pymysql://root@market_db/mysql')
con = engine.connect()
# con.execute("ALTER DATABASE mysql CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci")
# con.execute("ALTER TABLE test CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
con.execute("ALTER TABLE test CONVERT TO CHARSET UTF8")
df.to_sql('test', con, if_exists="replace")
print('finish')