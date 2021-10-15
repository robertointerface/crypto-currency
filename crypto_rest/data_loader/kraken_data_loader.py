import datetime
import requests
import numbers
import logging
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

# Define loggers
logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.ERROR)
c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)

f_handler = logging.FileHandler('logs/kraken_extractor.log', mode='a', encoding='utf-8')
f_format = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
f_handler.setFormatter(f_format)


logger.addHandler(c_handler)
logger.addHandler(f_handler)

UNIX_TIME_2010 = 1262304000
CURRENT_TIME = int(datetime.datetime.utcnow().timestamp())


def convert_unix_to_date(unix_time: int):
    return datetime.datetime.fromtimestamp(unix_time).strftime('%d/%m/%Y')


def later_than_first_crypto_transaction(time_stamp):
    return time_stamp >= UNIX_TIME_2010


def less_than_today(time_stamp):
    return time_stamp <= CURRENT_TIME


def is_valid_unix_time(time_stamp: int):
    """validate if a time stamp is a valid time stamp for crypto trading.
    - check if is a integer as unix times are integers.
    - check if time stamp is bigger than 2010 when first crypto transanction
    took place.
    - check that is not a less than the current time, No time travel yet
    unfortunately.
    """
    return all([isinstance(time_stamp, numbers.Integral),
               later_than_first_crypto_transaction(time_stamp),
               less_than_today(time_stamp)])


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

    def _is_length_of_result_1(self):
        """check if the request result returned results belonging to one
        crypto coin or to multiple or empty"""
        return len(self.response_result.keys()) == 1

    def _first_response_result_key(self):
        """get the first key from result dictionary"""
        return self.response_result.keys()[1]

    def set_response_first_result_date(self):
        """Logs the date of the first item on response, this is necessary as
        sometimes when we request data starting from a specific date, there
        might be no data from that specific date but the Kraken API returns the
        data from the closest date to the requested one, therefore is important
        to log this date so we are aware."""
        first_item = self._response_sequence[0][0]
        if is_valid_unix_time(first_item):
            logger.info(f'First date for {self._symbol} is '
                        f'{convert_unix_to_date(first_item)}')


    def set_response_sequence(self):
        """Set request response to a sequence that can be iterated"""
        request_response = self.response_result.get(self._symbol)
        if request_response is not None:
            self._response_sequence = request_response
        # Sometimes the requests returns the correct requested information
        # but under different symbol name, in those cases just get the
        # returned result.
        elif self._is_length_of_result_1():
            request_response_symbol = self._first_response_result_key()
            self._response_sequence = self.response_result.get(request_response_symbol)
        else:
            raise NonRelatedResponseError

    def create_serializer_input(self, OHLC_response: list):
        # first need to convert to float as response is in JSON
        OHLC_response = [float(i) for i in OHLC_response]
        try:
            # create a dictionary that can be used by KrakenSymbolSerializer
            return {
                'open': round(OHLC_response[KrakenResponseIndex.OPEN], 2),
                'high': round(OHLC_response[KrakenResponseIndex.HIGH], 2),
                'low': round(OHLC_response[KrakenResponseIndex.LOW], 2),
                'close': round(OHLC_response[KrakenResponseIndex.CLOSE], 2),
                'date': convert_unix_to_date(
                    OHLC_response[KrakenResponseIndex.DATE])
            }
        except IndexError as e:
            # log error to analyze
            logger.error(f'Index exception at symbol {self._symbol} {e.args}')

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
        # then call set first date on logging file
        # then iterate over it and save data
        pass


