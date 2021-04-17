FROM ubuntu:latest

RUN apt-get -y update
RUN apt-get -y install python3
RUN apt-get -y install python3-pip

RUN mkdir /data


COPY ./data_from_seoul.py ./data/data_from_seoul.py
COPY ./key.txt ./data/key.txt

RUN pip3 install pymongo
RUN pip3 install requests

WORKDIR /data
CMD ["python3", "data_from_seoul.py", "1", "2", "2019"]