from crypto_data.models import KrakenOHLC


class LoadDataFromPostSQl:
    """Load data from postSQL database by providing a symbol and an start time"""
    def __init__(self, symbol:str, time:str):
        self._symbol = symbol
        self._time = time
        self._response = None

    def get_response(self):
        return self._response

    def load_data(self):
        # only load data if it has not been loaded yet
        if self._response is None:
            query = (KrakenOHLC.objects
                     .filter(symbol__symbol=self._symbol)
                     .filter(date__gte=self._time))
            if not query.exists():
                raise SystemExit(f'No data found for symbol {self._symbol} and '
                                 f'time {self._time}')
            else:
                self._response = query.all()
        else:
            raise ValueError(f'response can not be modified once initialized '
                             f'on class {self.__class__.__name__}')

    def csv_headers(self):
        return ['symbol', 'date', 'open', 'high', 'low', 'close']

    def __iter__(self):
        """Iterate over given response"""
        if self._response is not None:
            for r in self._response:
                yield (r.symbol.symbol,
                       r.date.strftime('%Y-%m-%d'),
                       r.open,
                       r.high,
                       r.low,
                       r.close)