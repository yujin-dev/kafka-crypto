from binance.websocket.spot.websocket_client import SpotWebsocketClient as WebsocketClient

class WebsocketStreams:

    def __init__(self):
        self.client = WebsocketClient()
        self.client.start()

    def terminate(self):
        self.client.stop()

    def get_ticker(self, symbol:str):

        def on_event(event):
            print(event)

        self.client.mini_ticker(
            symbol=symbol,
            id=1,
            callback=on_event
        )

    def subscribe(self, stream:list):

        def on_event(event):
            print(event["data"])

        self.client.instant_subscribe(
            stream=stream,
            callback=on_event
        )

    def get_orderbook(self, symbols: list):
        streams = ["%s@bookTicker"%symbol for symbol in symbols]
        self.subscribe(streams)


if __name__ == "__main__":

    ws = WebsocketStreams()
    # ws.get_ticker(symbol="bnbusdt")
    ws.get_orderbook(["bnbusdt", "ethusdt"])