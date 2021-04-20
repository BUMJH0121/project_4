import pandas as pd
import pymysql
from sqlalchemy import create_engine
pymysql.install_as_MySQLdb()

df = pd.read_excel('dong_code_transformation.xlsx',index_col=0)
print(df)
engine = create_engine('mysql+pymysql://root@localhost:13306/mysql')
con = engine.connect()
con.execute("""CREATE table code_data (
            seq INT NOT NULL,
            Gu VARCHAR(20),
            Dong VARCHAR(20),
            Code VARCHAR(15)
            ) ENGINE=MYISAM CHARSET=utf8;""")
con.execute("ALTER DATABASE mysql CHARACTER SET = utf8")
con.execute("ALTER TABLE code_data CONVERT TO CHARACTER SET utf8")
df.to_sql('code_data', con, if_exists="replace")
print('finish')