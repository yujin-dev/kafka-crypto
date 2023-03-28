# Kafka streaming - binance coin data ( Python )

Binance API를 활용하여 시세 데이터를 받아오자

## Requirements

- 클러스터 셋업 : kafka-cluster내의 `docker-compose.yml`를 기반으로 클러스터를 띄운다.
- dependency 설치 : `pip install -r requirements.txt`로 필요한 패키지를 설치한다.

## Run

먼저 데이터를 적재할 토픽을 생성한다. 예시로 `bnbusdt`, `ethusdt`라는 이름의 토픽을 생성하였다.
```python
from producer import create_topic

create_topic(["bnbusdt", "ethusdt"])
```

사용하려는 kafka 클러스터 정보를 기반으로 `kafka.KafkaProducer` 인스턴스를 생성하여 binance 시세 데이터( bnbusdt, ethusdt )를 스트리밍한다.
```python 
from producer import KafkaProducer, OrderbookProducer

kafka_producer = KafkaProducer(
    bootstrap_servers = os.environ.get("BOOTSTRAP_SERVER"),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
    # acks=0
)

producer = OrderbookProducer(producer=kafka_producer, topic="bnbusdt")
producer.publish(targets=["bnbusdt"])

producer = OrderbookProducer(producer=kafka_producer, topic="ethusdt")
producer.publish(targets=["ethusdt"])
```

## TroubleShooting
```
WebSocket connection closed: connection was closed uncleanly ("SSL error: unregistered scheme (in )"), code: 1006, clean: False, reason: connection was closed uncleanly ("SSL error: unregistered scheme (in )")
Lost connection to Server. Reason: [Failure instance: Traceback (failure with no frames): <class 'twisted.internet.error.ConnectionDone'>: Connection was closed cleanly.
```
- 해결 : 환경 변수에 `SSL_CERT_FILE`로 `python3 -m certifi` 반환값을 설정