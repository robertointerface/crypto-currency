"""
Tests for module kraken_data_loader, test loading data from kraken website
and save it on SQL database using models on app crypto_data
"""
from collections.abc import Mapping
from django.test import TestCase
from data_loader.kraken_data_loader import (convert_unix_to_date,
                                            KrakenContentFetcher)


class TestDataLoader(TestCase):

    KRAKEN_OHLC_URL = 'https://api.kraken.com/0/public/OHLC'
    TEST_START_DATE = 1628809200  # 13/Aug/2021
    DATA_INTERVALS = 1440
    BITCOIN_USD = 'BTCUSD'

    def test_convert_unix_to_date(self):
        """Test convert unix timestamp to a date that can be easier to read"""
        unix_time = 1634008620
        date = convert_unix_to_date(unix_time)
        self.assertEqual(date, '12/10/2021')

    def test_kraken_content_fetcher_returns_json_response(self):
        """fetch method returns a json object when correct parameters are
        provided"""
        request_params = {
            'pair': self.BITCOIN_USD,
            'interval': 1440,
            'since': self.TEST_START_DATE
        }
        kraken_fetcher = KrakenContentFetcher(self.KRAKEN_OHLC_URL,
                                              request_params)
        response = kraken_fetcher.fetch()
        self.assertIsInstance(response, Mapping)

