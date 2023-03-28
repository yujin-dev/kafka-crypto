from binance.websocket.spot.websocket_client import SpotWebsocketClient as WebsocketClient

class WebsocketStreams:

    def __init__(self, handler):
        self.handler = handler
        self.client = WebsocketClient()
        self.client.start()

    def terminate(self):
        self.client.stop()

    def __subscribe(self, stream:list):
        self.client.instant_subscribe(
            stream=stream,
            callback=self.handler
        )

    def get_ticker(self, symbol:str):
        self.client.mini_ticker(
            symbol=symbol,
            id=1,
            callback=self.handler
        )

    def get_orderbook(self, symbols: list):
        streams = ["%s@bookTicker"%symbol for symbol in symbols]
        self.__subscribe(streams)