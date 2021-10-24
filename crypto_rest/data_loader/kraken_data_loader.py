"""Fetch data from Kraken API and filter its response"""
import datetime
import logging
import numbers
import pprint
from collections import namedtuple
import requests
from requests.exceptions import Timeout, HTTPError
from data_loader.resource_content_abs import ContentResourceFetcher
from data_loader.errors import NonRelatedResponseError


OHLC_data = namedtuple('OHLC_data', 'open high low close')

# Define loggers
logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.ERROR)
c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)

f_handler = logging.FileHandler('logs/kraken_extractor.log',
                                mode='a',
                                encoding='utf-8')
f_format = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
f_handler.setFormatter(f_format)


logger.addHandler(c_handler)
logger.addHandler(f_handler)

UNIX_TIME_2010 = 1262304000
CURRENT_TIME = int(datetime.datetime.utcnow().timestamp())


def convert_unix_to_date(unix_time: int):
    """convert unix time stamp into a date of format year-month-day"""
    return datetime.datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')


def is_later_than_first_crypto_transaction(time_stamp: int):
    """is time_stamp later than 2010"""
    return time_stamp >= UNIX_TIME_2010


def is_less_than_today(time_stamp: int):
    """is time_stamp less than today"""
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
               is_later_than_first_crypto_transaction(time_stamp),
               is_less_than_today(time_stamp)])


class KrakenResponseIndex:
    """
    Kraken api returns an array with HOLC data, each item in the array is
    an array with all the HOLC info for a specific date, i.e
    [[OHLC data for 1 january],[OHLC data for 2 january]], use the indexes
    below to know where to locate specific OHLC data on every array,
    i.e the date is in index 0 or open value on index 1."""
    DATE = 0
    OPEN = 1
    HIGH = 2
    LOW = 3
    CLOSE = 4


class KrakenContentFetcher(ContentResourceFetcher):
    """Fetch data from Kraken API or report error.
    Methods:
        - fetch: fetch data.
    Properties:
    - kraken_symbol: Kraken symbol for requested information
    - request_since: start time for requested information.
    """
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

            raise HTTPError(f'Error response at requesting data for symbol '
                            f'{self.kraken_symbol} for starting date '
                            f'{convert_unix_to_date(self.request_since)}')
        except Timeout as e:
            raise HTTPError(f'Time out when requesting url {self._url} with '
                            f'params {self._params}') from e

    def __repr__(self):
        class_name = self.__class__.__name__
        return f'{class_name}({self._url, self._params})'

    def __str__(self):
        return f'Kraken fetcher for params {self._params}'


class KrakenResponseExtractor:
    """Convert a JSON response returned from Kraken into a dictionary that
    can be used by a serializer to save content.
    Methods:
        - is_error_response: Kraken response includes error messages.
        - _is_length_of_result_1: Kraken response includes more than 1 result
        object, Kraken returns 1 result per coin, this method tells us if the
        result includes data from multiple coins or only one.
        - find_result_key: provided that method _is_length_of_result_1 returns
        True, find the coin symbol.
        - set_response_first_result_date: Logs the date of the first item on
        response.
        - set_response_sequence: Response from Kraken is contained in a list
        , this method saves that list to self._response_sequence so later it
        can be iterated.

    """
    def __init__(self, response: dict, symbol: str, *args, **kwargs):
        self._response = response
        self._symbol = symbol
        self._response_sequence = None

    def is_error_response(self):
        """Check if the response returned form kraken api has error on it"""
        errors = self._response.get('error')
        if errors is not None:
            return len(errors) > 0

    @property
    def response_result(self):
        """Get result object from kraken response."""
        return self._response.get('result')

    def _is_length_of_result_1(self):
        """check if the request result returned results belonging to one
        crypto coin or to multiple or empty"""
        return len(self.response_result.keys()) == 1

    def find_result_key(self):
        """call this method in case the returned response does not include the
        requested symbol, sometimes Kraken will understand your request and
        return the data correctly but under different symbol that the one
        you requested, i.e you requested data for BTCUSD (Bitcoin in US dollars)
        but kraken returns data for XXBTUSD, so you need to find out this
        symbol in order to extract the data
        """
        # filter the keys that are not equal to 'last', you could use filter
        # in function also but the filter is simple enough to understand like
        # this.
        response_keys = [k for k in self.response_result.keys() if k != 'last']
        if len(list(response_keys)) == 1:
            return response_keys[0]
        return None

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
        elif self.find_result_key() is not None:
            request_response_symbol = self.find_result_key()
            self._response_sequence = self.response_result.get(request_response_symbol)
        else:
            raise NonRelatedResponseError #PRINT THIS AS IS NOT HANDLE AT THE MOMENT

    def create_serializer_input(self, OHLC_response: list):
        """Use OHLC data returned form Kraken API to create a dictionary
        object that can be used by KrakenSymbolSerializer."""
        # first need to convert to float all OHLC numbers from kraken api as
        # numbers are provided in JSON format.
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
            # log error to analyze later and try next OHLC item.
            logger.error(f'Index exception at symbol {self._symbol} {e.args}')

    def __iter__(self):
        """iterate over the items obtained from Kraken api and pass them in a
         format that ca be used to be saved on database."""
        return (self.create_serializer_input(i)
                for i in self._response_sequence)

    def __repr__(self):
        class_name = self.__class__.__name__
        return f'<{class_name} ' \
               f'response={pprint.pprint(self._response, depth=1)} ' \
               f'symbol={self._symbol}>'

    def __str__(self):
        class_name = self.__class__.__name__
        return f'{class_name} for symbol {self._symbol}'
