# Kafka with Python
binance에서 코인 시세 데이터 받아오기

## TroubleShooting
```
WebSocket connection closed: connection was closed uncleanly ("SSL error: unregistered scheme (in )"), code: 1006, clean: False, reason: connection was closed uncleanly ("SSL error: unregistered scheme (in )")
Lost connection to Server. Reason: [Failure instance: Traceback (failure with no frames): <class 'twisted.internet.error.ConnectionDone'>: Connection was closed cleanly.
```
- 환경 변수에 `SSL_CERT_FILE`로 `python3 -m certifi` 반환값을 설정