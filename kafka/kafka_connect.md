## kafka-connect 설정

1. kafka connect 설치 후 압축 해제

```
ubuntu@ip-172-31-55-25:~/kafka_connect/$ curl -O http://packages.confluent.io/archive/5.5/confluent-community-5.5.2-2.12.tar.gz
```

```
ubuntu@ip-172-31-55-25:~/kafka_connect/$ tar xvf confluent-community-5.5.2-2.12.tar.gz
```

2. kafka-connect 실행

```
ubuntu@ip-172-31-55-25:~/kafka_connect/confluent-5.5.2$ bin/connect-distributed ./etc/kafka/connect-distributed.properties 
```

3. topic 목록 확인

```
ubuntu@ip-172-31-55-25:~/kafka_connect/confluent-5.5.2$ bin/kafka-topics --list --bootstrap-server localhost:9092
__consumer_offsets
_schemas
bus_stop
connect-configs
connect-offsets
connect-status
mariadb-messages
market
```

4. 