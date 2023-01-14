import time
from kafka import KafkaProducer
from data.binance import WebsocketStreams

class CryptoProducer:
    def __init__(self, topic:str):
        self.producer = KafkaProducer(acks=0, bootstrap_servers=['localhost:9092'])
        self.topic = topic

    def publish(self, event):
        self.producer.send(self.topic, self.producer)
        self.producer.flush()


if __name__ == "__main__":

    producer = CryptoProducer(topic = "binance-test")
    websocket = WebsocketStreams(producer.publish)
    websocket.get_orderbook(["bnbusdt", "ethusdt"])