from binance.websocket.spot.websocket_client import SpotWebsocketClient as WebsocketClient

class WebsocketStreams:

    def __init__(self, callback):
        self.callback = callback
        self.client = WebsocketClient()
        self.client.start()

    def terminate(self):
        self.client.stop()

    def get_ticker(self, symbol:str):

        self.client.mini_ticker(
            symbol=symbol,
            id=1,
            callback=self.callback
        )

    def subscribe(self, stream:list):

        self.client.instant_subscribe(
            stream=stream,
            callback=self.callback
        )

    def get_orderbook(self, symbols: list):
        streams = ["%s@bookTicker"%symbol for symbol in symbols]
        self.subscribe(streams)


if __name__ == "__main__":

    ws = WebsocketStreams()
    # ws.get_ticker(symbol="bnbusdt")
    ws.get_orderbook(["bnbusdt", "ethusdt"])