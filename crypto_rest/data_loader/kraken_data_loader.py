import datetime
import requests
from requests.exceptions import Timeout, HTTPError, ConnectionError
from .resource_content_abs import ContentResourceFetcher
from .errors import NonRelatedResponseError

START_DATE = 1570834800  # 12/oct/2019 00:00:00
END_DATE = 1633993200  # 12/oct/2021 00:00:00
INCREMENT_STEPS = 1440  # 60 minutes * 24 hours, increments by day
KRAKEN_URLS = {
    'OHLC': 'https://api.kraken.com/0/public/OHLC'
}


def convert_unix_to_date(unix_time: int):
    return datetime.datetime.fromtimestamp(unix_time).strftime('%d/%m/%Y')


class KrakenContentFetcher(ContentResourceFetcher):

    def __init__(self, url: str, params: dict):
        """Initialize instance.
        @params:
        - Url: valid kraken base URL
        - params: valid kraken parameters to be used on building query URL
        """
        self._url = url
        self._params = params

    @property
    def kraken_symbol(self):
        """Symbol representing the crypto currency value, the value can be in
         monetary currency or in another crypto value"""
        return self._params.get('pair')

    @property
    def request_since(self):
        """starting date for which data is requested, this is in unix time"""
        return self._params.get('since')

    def fetch(self):
        """Fetch data from kraken API"""
        try:
            response = requests.get(self._url,
                                    params=self._params,
                                    timeout=5)
            if response.status_code == requests.codes.ok:
                return response.json()
            else:
                raise HTTPError(f'Error response at requesting data for symbol '
                                f'{self.kraken_symbol} for starting date '
                                f'{convert_unix_to_date(self.request_since)}')
        except Timeout:
            print('Timeout Error')


class KrakenResponseExtractor:

    def __init__(self, response: dict):
        self._response = response
        self._response_sequence = None

    def is_error_response(self):
        errors = self._response.get('error')
        if errors is not None:
            return len(errors) > 0

    @property
    def response_result(self):
        return self._response.get('result')

    def set_response_sequence(self, symbol):
        symbol_response = self.response_result.get(symbol)
        if symbol_response is not None:
            self._response_sequence = symbol_response
        else:
            raise NonRelatedResponseError

    def __iter__(self):
        return (i for i in self._response_sequence)


class ResponseExtractor:

    def __init__(self):
        self.extractor = None

    def extract_response(self, extractor):
        pass
