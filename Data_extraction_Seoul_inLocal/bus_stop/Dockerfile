FROM python:3.7.9-stretch

WORKDIR /mydata

RUN pip install requests
RUN pip install bs4
RUN pip install pandas
RUN pip install sqlalchemy
RUN pip install pymysql
RUN pip install mysqlclient

COPY ./bus_stop.py /mydata/bus_stop.py

CMD tail -f /dev/null