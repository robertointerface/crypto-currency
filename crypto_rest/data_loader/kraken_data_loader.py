import datetime
import requests
from collections import namedtuple
from decimal import *
from requests.exceptions import Timeout, HTTPError, ConnectionError
from .resource_content_abs import ContentResourceFetcher
from .errors import NonRelatedResponseError

START_DATE = 1570834800  # 12/oct/2019 00:00:00
END_DATE = 1633993200  # 12/oct/2021 00:00:00
INCREMENT_STEPS = 1440  # 60 minutes * 24 hours, increments by day
KRAKEN_URLS = {
    'OHLC': 'https://api.kraken.com/0/public/OHLC'
}

OHLC_data = namedtuple('OHLC_data', 'open high low close')



def convert_unix_to_date(unix_time: int):
    return datetime.datetime.fromtimestamp(unix_time).strftime('%d/%m/%Y')

class KrakenResponseIndex:
    DATE = 0
    OPEN = 1
    HIGH = 2
    LOW = 3
    CLOSE = 4

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

    def __init__(self, response: dict, symbol: str, *args, **kwargs):
        self._response = response
        self._symbol = symbol
        self._response_sequence = None

    def is_error_response(self):
        errors = self._response.get('error')
        if errors is not None:
            return len(errors) > 0

    @property
    def response_result(self):
        return self._response.get('result')

    def set_response_sequence(self):
        """Set request response to a sequence that can be iterated"""
        request_response = self.response_result.get(self._symbol)
        if request_response is not None:
            self._response_sequence = request_response
        else:
            raise NonRelatedResponseError

    def create_serializer_input(self, OHLC_response: list):
        # first need to convert to float as response is in JSON
        OHLC_response = [float(i) for i in OHLC_response]
        try:
            return {
                'open': round(OHLC_response[KrakenResponseIndex.OPEN], 2),
                'high': round(OHLC_response[KrakenResponseIndex.HIGH], 2),
                'low': round(OHLC_response[KrakenResponseIndex.LOW], 2),
                'close': round(OHLC_response[KrakenResponseIndex.CLOSE], 2),
                #'date': convert_unix_to_date(OHLC_response)
            }
        except IndexError:
            # log in file not completed
            #raise data not completed for this time stamp
            pass
            # need to raise error to not save this data and log it

    def __iter__(self):
        return (self.create_serializer_input(i)
                for i in self._response_sequence)


class ResponseExtractor:

    def __init__(self):
        self.extractor = None

    def extract_response(self, extractor):
        self.extractor = extractor
        # call if is not error response
        # then call set response sequence
        pass


