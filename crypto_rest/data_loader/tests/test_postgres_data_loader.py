from django.test import TestCase
from unittest.mock import patch, Mock
from requests.exceptions import HTTPError
from data_loader.save_crypto_names import create_kraken_symbols
from data_loader.postgres_data_loader import load_kraken_data_into_postgres
from data_loader.kraken_data_loader import KrakenContentFetcher
from data_loader.response_extractor import ResponseExtractor

class TestLoadkrakenData(TestCase):
    """test method load_kraken_data_into_postgres"""
    call_arguments = []

    def setUp(self) -> None:
        """initalize KrakenSymbols."""
        create_kraken_symbols('USD')

    def tearDown(self) -> None:
        self.call_arguments = []

    def save_params(self, url, params):
        self.call_arguments.append((url, params))

    @patch('data_loader.kraken_data_loader.KrakenContentFetcher.fetch')
    def test_KrakenContentFetcher_is_called_several_times(self, mock_fetcher):
        """test instance of type KrakenContentFetcher is called the right
        amount of times"""
        load_kraken_data_into_postgres('OHLC')
        self.assertEqual(mock_fetcher.call_count, 6)


    def test_KrakenContentFetcher_init_is_called_with_right_arguments(self):
        """test KrakenContentFetcher __init__ is initialized with correct
        arguments when being called from method load_kraken_data_into_postgres
        """
        # Mock __init__
        KrakenContentFetcher.__init__ = Mock()
        KrakenContentFetcher.__init__.return_value = None
        # set side_effect to be able to save arguments for later inspection
        KrakenContentFetcher.__init__.side_effect = self.save_params
        # need to mock fetch method, otherwise error will raise as error uses
        # parameters that were not set on the mocked __init__
        KrakenContentFetcher.fetch = Mock()
        # need to mock ResponseExtractor.extract_response to avoid processing
        # this unnecessary part.
        ResponseExtractor.extract_response = Mock()
        load_kraken_data_into_postgres('OHLC')
        for args in self.call_arguments:
            url, params = args
            self.assertEqual(url, 'https://api.kraken.com/0/public/OHLC')

    def test_HTTError_logs_message_into_file(self):
        """test when HTTPError raised on a request when fetching kraken data
        it logs an error message on a file"""
        KrakenContentFetcher.fetch = Mock()
        KrakenContentFetcher.fetch.side_effect = HTTPError
        with self.assertLogs('data_loader.postgres_data_loader'):
            load_kraken_data_into_postgres('OHLC')
