FROM python:3.7.9-stretch

WORKDIR /mydata

RUN pip install requests \ 
    pymongo

COPY ./resident_population.py /mydata/resident_population.py
COPY ./api_key.txt /mydata/api_key.txt

#CMD tail -f /dev/null
CMD python resident_population.py
