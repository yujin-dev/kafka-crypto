from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from data.binance_stream import WebsocketStreams
import json
from dotenv import load_dotenv
import os
import time

load_dotenv()

def create_topic(topics:list):
    client = KafkaAdminClient(
        bootstrap_servers = os.environ.get("BOOTSTRAP_SERVER"),
        client_id = "admin-client"
    )
    topics = [NewTopic(name=topic, num_partitions=1, replication_factor=1) for topic in topics]
    client.create_topics(new_topics=topics, validate_only=False)


class OrderbookProducer:
    def __init__(self, producer:KafkaProducer, topic:str):
        self.producer = producer
        self.topic = topic

    def publish(self, targets:list):
        websocket = WebsocketStreams(handler=self.send_event)
        websocket.get_orderbook(symbols=targets)
        
    def send_event(self, event):
        data = event["data"]
        msg = {
            "time": time.time(),
            "bidPrice": data["b"],
            "bidQty": data["B"],
            "askPrice": data["a"],
            "askQty": data["A"]
        }
        self.producer.send(self.topic, msg)


if __name__ == "__main__":

    # create_topic(["bnbusdt", "ethusdt"])

    PRODUCER = KafkaProducer(
        bootstrap_servers = os.environ.get("BOOTSTRAP_SERVER"),
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
        # acks=0
    )

    producer = OrderbookProducer(producer=PRODUCER, topic="bnbusdt")
    producer.publish(targets=["bnbusdt"])
    
    producer = OrderbookProducer(producer=PRODUCER, topic="ethusdt")
    producer.publish(targets=["ethusdt"])