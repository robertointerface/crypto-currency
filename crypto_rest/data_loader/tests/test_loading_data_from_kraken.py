"""
Tests for module kraken_data_loader, test loading data from kraken website
and save it on SQL database using models on app crypto_data
"""
from collections.abc import Mapping
from unittest.mock import patch
from django.test import TestCase
from data_loader.kraken_data_loader import (convert_unix_to_date,
                                            KrakenContentFetcher)
from requests.exceptions import HTTPError, ConnectionError


def mocked_requests_get(response_json_data, response_status_code):
    """Create mock response for request get"""
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

    return MockResponse(response_json_data, response_status_code)


class TestDataLoader(TestCase):

    KRAKEN_OHLC_URL = 'https://api.kraken.com/0/public/OHLC'
    TEST_START_DATE = 1628809200  # 13/Aug/2021
    DATA_INTERVALS = 1440
    BITCOIN_USD = 'BTCUSD'
    NON_EXISTING_SYMBOL = 'NON_EXISTING'
    NON_EXISTING_INTERVAL = 1516585615181552
    NON_EXISTING_SINCE = 1518416515000000000

    @property
    def correct_request_params(self):
        return {
            'pair': self.BITCOIN_USD,
            'interval': 1440,
            'since': self.TEST_START_DATE
        }

    def test_convert_unix_to_date(self):
        """Test convert unix timestamp to a date that can be easier to read"""
        unix_time = 1634008620
        date = convert_unix_to_date(unix_time)
        self.assertEqual(date, '12/10/2021')

    def test_kraken_content_fetcher_returns_json_response(self):
        """fetch method returns a json object when correct parameters are
        provided"""
        kraken_fetcher = KrakenContentFetcher(self.KRAKEN_OHLC_URL,
                                              self.correct_request_params)
        response = kraken_fetcher.fetch()
        self.assertIsInstance(response, Mapping)

    def test_kraken_content_fetcher_raises_HTTPError(self):
        """Fetch method raises error when response status code is not ok"""
        mocked_response = mocked_requests_get({'error': 'error'}, 500)
        with patch('requests.get', return_value=mocked_response):
            kraken_fetcher = KrakenContentFetcher(self.KRAKEN_OHLC_URL,
                                                  self.correct_request_params)
            with self.assertRaises(HTTPError):
                kraken_fetcher.fetch()



