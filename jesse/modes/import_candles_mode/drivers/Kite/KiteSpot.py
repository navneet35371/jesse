import requests
import jesse.helpers as jh
from jesse.models.Account import Account
from jesse.modes.import_candles_mode.drivers.interface import CandleExchange
from jesse.enums import exchanges
from jesse import exceptions
from .kite_utils import timeframe_to_interval
import arrow

# curl 'https://kite.zerodha.com/oms/instruments/historical/256265/minute?oi=1&from=2021-03-23&to=2021-04-22' \
#   -H 'accept: */*' \
#   -H 'accept-language: en-IN,en;q=0.9' \
#   -H 'authorization: enctoken zxuW6TOdMoytkcUjwUeZDypC9/hAjIXeTa3LZ23VQi0WHqsxc6eWHhyESZbhJ0kO5TzFdX72E0MARIt8JTZ+9LDPUL73knzRGJMPZXmcQD4PvftbAVGXVQ==' 

class KiteSpot(CandleExchange):
    def __init__(self) -> None:
        super().__init__(
            name=exchanges.KITE_SPOT,
            count=10080,
            rate_limit_per_second=1.5,
            backup_exchange_class=None
        )

        self.endpoint = 'https://kite.zerodha.com'

    def get_starting_time(self, symbol: str) -> int:
        """
        Because Coinbase's API sucks and does not make this take easy for us,
        we do it manually for as much symbol as we can!

        :param symbol: str
        :return: int
        """
        if symbol == 'BTC-USD':
            return 1438387200000
        elif symbol == 'ETH-USD':
            return 1464739200000
        elif symbol == 'LTC-USD':
            return 1477958400000

        return None

    def fetch(self, symbol: str, start_timestamp: int, timeframe: str) -> list:
        """
        note1: unlike Bitfinex, Binance does NOT skip candles with volume=0.
        note2: like Bitfinex, start_time includes the candle and so does the end_time.
        """
        end_timestamp = start_timestamp + (self.count - 1) * 60000 * jh.timeframe_to_one_minutes(timeframe)

        granularity = timeframe_to_interval(timeframe)
        payload = {
            'from': jh.timestamp_to_time_kite(start_timestamp),
            'to': jh.timestamp_to_time_kite(end_timestamp),
            'oi': 1
        }
        account = Account.get(exchange='kite')
        headers = {'Authorization': 'enctoken ' + account.exchange_token}
        # headers = {'authorization': 'enctoken Wqe1EjmNnuSzUi8Hu7WGn8tVoNbJiXnCq8cNIgNJPIvtbQGRoaOMkLoI+By5C50p/XZDeE2vymRYhPqTaVlHvCAEv3Z5AFN2Tx949AWR4a4K2J+TZUSVhg=='}
        # https://kite.zerodha.com/oms/instruments/historical/256265/minute?oi=1&from=2021-03-23&to=2021-04-22
        response = requests.get(
            f"{self.endpoint}/oms/instruments/historical/{symbol}/{granularity}",
            params=payload,
            headers=headers
        )

        self.validate_response(response)

        data = response.json()["data"]["candles"]
        return [
            {
                'id': jh.generate_unique_id(),
                'exchange': self.name,
                'symbol': symbol,
                'timeframe': timeframe,
                # 2021-01-07T15:28:00+0530
                # 2013-09-30T15:34:00.000-07:00
                'timestamp': jh.arrow_to_timestamp(arrow.get(d[0])),
                # 'timestamp': int(d[0]) * 1000,
                'open': float(d[3]),
                'close': float(d[4]),
                'high': float(d[2]),
                'low': float(d[1]),
                'volume': float(d[5])
            } for d in data
        ]