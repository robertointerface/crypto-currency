"""
Tests for module kraken_data_loader, test loading data from kraken website
and save it on SQL database using models on app crypto_data
"""
from decimal import *
from collections.abc import Mapping
from unittest.mock import patch, Mock
from django.test import TestCase
from data_loader.kraken_data_loader import (convert_unix_to_date,
                                            KrakenContentFetcher,
                                            KrakenResponseExtractor)
from data_loader.response_extractor import ResponseExtractor
from data_loader.errors import ExtractorErrorResponse
from requests.exceptions import HTTPError, ConnectionError


def mocked_requests_get(response_json_data, response_status_code):
    """Create mock response for request get"""
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

    return MockResponse(response_json_data, response_status_code)


class TestKrakenContentFetcher(TestCase):

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
        self.assertEqual(date, '2021-10-12')

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



class TestKrakenResponseExtractor(TestCase):

    ERROR_RESPONSE = {"error":["EQuery:Unknown asset pair"]}
    VALID_RESPONSE = {"error":[],"result":{"SOLUSD":[
        [1632441600,"149.92","151.30","126.60","139.24","138.06","254005.29576624",19338],
        [1632528000,"139.19","144.00","133.71","136.07","138.33","122860.44860293",8251],
        [1632614400,"135.81","140.67","125.00","135.71","133.44","177607.42934785",11195],
        [1632700800,"135.36","148.83","133.88","136.30","142.28","209945.47932869",14631],
        [1632787200,"136.24","139.32","128.22","132.21","133.37","164573.56774161",9392],
        [1632873600,"132.19","139.95","131.29","135.25","136.19","122735.50872704",8938],
        [1632960000,"135.24","142.85","134.15","141.30","138.86","116648.69998585",9085],
        [1633046400,"141.31","165.00","138.32","161.87","150.95","322541.17130002",19514],
        [1633132800,"161.60","175.37","156.35","169.00","166.56","160603.12555594",14110],
        [1633219200,"168.99","177.69","165.67","172.92","172.71","128501.53929616",12524],
        [1633305600,"172.84","172.94","162.00","167.18","168.59","129669.97631581",11723],
        [1633392000,"167.19","170.00","160.14","164.69","165.56","129902.62731322",9081],
        [1633478400,"164.75","165.39","150.45","154.09","157.43","188699.99243639",14830],
        [1633564800,"153.90","161.44","150.57","154.34","156.25","106171.25961946",10337],
        [1633651200,"154.55","168.81","152.60","158.75","162.65","117734.13738350",11224],
        [1633737600,"158.75","161.38","154.41","156.84","157.87","54741.75239893",6004],
        [1633824000,"156.87","158.37","146.04","147.76","152.47","62884.80911174",7140],
        [1633910400,"147.54","153.87","140.50","144.94","146.85","106788.06518712",8080],
        [1633996800,"144.87","153.28","137.82","152.44","146.11","132484.34003752",12210],
        [1634083200,"152.20","155.50","144.49","146.90","147.97","61114.61817370",5135]
    ],
        "last":1633996800}}
    VALID_RESPONSE_SYMBOL = "SOLUSD"

    def test_is_error_response(self):
        """Test method is_error_response returns True when there is an error
        in the response and false when not"""
        tests_inputs = [
            (self.ERROR_RESPONSE, self.assertTrue),
            (self.VALID_RESPONSE, self.assertFalse),
        ]
        for test in tests_inputs:
            response, expected_result = test
            kraken_extractor = KrakenResponseExtractor(response,
                                                       self.VALID_RESPONSE_SYMBOL)
            expected_result(kraken_extractor.is_error_response())

    def test_set_response_sequence(self):
        """test method set_response_sequence gets response sequence when the
         returned response has the same symbol as the requested one"""
        kraken_extractor = KrakenResponseExtractor(self.VALID_RESPONSE,
                                                   self.VALID_RESPONSE_SYMBOL)
        kraken_extractor.set_response_sequence()
        # iterate over kraken_extractor to obtain a list
        extracted_sequence = list(i for i in kraken_extractor)
        self.assertTrue(len(extracted_sequence) > 0)

    def test_create_serializer_input(self):
        """Test method create_serializer_input returns correct output in dict
        format with correct keys and values."""
        open, high, low, close = ["149.92", "151.30", "126.60", "139.24"]
        OHLC_response = [1632441600,
                         open,
                         high,
                         low,
                         close,
                         "138.06",
                         "254005.29576624",
                         19338]
        kraken_extractor = KrakenResponseExtractor(self.VALID_RESPONSE,
                                                   self.VALID_RESPONSE_SYMBOL)
        serialize_response = kraken_extractor.create_serializer_input(OHLC_response)
        self.assertAlmostEquals(serialize_response.get('open'),
                                round(float(open), 2),
                                delta=0.01)
        self.assertAlmostEquals(serialize_response.get('high'),
                                round(float(high), 2),
                                delta=0.01)

    def test_IndexError_logs_correct_error(self):
        """test logs when IndexError raises on method
        create_serializer_input"""
        open, high, low, close = ["149.92", "151.30", "126.60", "139.24"]
        OHLC_response = [1632441600,
                         open]
        with self.assertLogs('data_loader.kraken_data_loader') as cm:
            kraken_extractor = KrakenResponseExtractor(self.VALID_RESPONSE,
                                                       self.VALID_RESPONSE_SYMBOL)
            serialize_response = kraken_extractor.create_serializer_input(
                OHLC_response)

    def test_set_response_first_result_date(self):
        """Test """
        with self.assertLogs('data_loader.kraken_data_loader') as cm:
            kraken_extractor = KrakenResponseExtractor(self.VALID_RESPONSE,
                                                       self.VALID_RESPONSE_SYMBOL)
            kraken_extractor.set_response_sequence()
            kraken_extractor.set_response_first_result_date()
            self.assertEqual(cm.output[0],
                             'INFO:data_loader.kraken_data_loader:First date '
                             'for SOLUSD is 2021-09-24')


class TestResponseExtractor(TestCase):
    VALID_RESPONSE = {"error":[],"result":{"SOLUSD":[
        [1632441600,"149.92","151.30","126.60","139.24","138.06","254005.29576624",19338],
        [1632528000,"139.19","144.00","133.71","136.07","138.33","122860.44860293",8251],
        [1632614400,"135.81","140.67","125.00","135.71","133.44","177607.42934785",11195],
        [1632700800,"135.36","148.83","133.88","136.30","142.28","209945.47932869",14631],
        [1632787200,"136.24","139.32","128.22","132.21","133.37","164573.56774161",9392],
        [1632873600,"132.19","139.95","131.29","135.25","136.19","122735.50872704",8938],
        [1632960000,"135.24","142.85","134.15","141.30","138.86","116648.69998585",9085],
        [1633046400,"141.31","165.00","138.32","161.87","150.95","322541.17130002",19514],
        [1633132800,"161.60","175.37","156.35","169.00","166.56","160603.12555594",14110],
        [1633219200,"168.99","177.69","165.67","172.92","172.71","128501.53929616",12524],
        [1633305600,"172.84","172.94","162.00","167.18","168.59","129669.97631581",11723],
        [1633392000,"167.19","170.00","160.14","164.69","165.56","129902.62731322",9081],
        [1633478400,"164.75","165.39","150.45","154.09","157.43","188699.99243639",14830],
        [1633564800,"153.90","161.44","150.57","154.34","156.25","106171.25961946",10337],
        [1633651200,"154.55","168.81","152.60","158.75","162.65","117734.13738350",11224],
        [1633737600,"158.75","161.38","154.41","156.84","157.87","54741.75239893",6004],
        [1633824000,"156.87","158.37","146.04","147.76","152.47","62884.80911174",7140],
        [1633910400,"147.54","153.87","140.50","144.94","146.85","106788.06518712",8080],
        [1633996800,"144.87","153.28","137.82","152.44","146.11","132484.34003752",12210],
        [1634083200,"152.20","155.50","144.49","146.90","147.97","61114.61817370",5135]
    ],
        "last":1633996800}}
    VALID_RESPONSE_SYMBOL = "SOLUSD"

    @patch('data_loader.kraken_data_loader.KrakenResponseExtractor')
    def test_ExtractorErrorResponse_is_raised(self, kraken_mock):
        """Test if extractor method 'is_error_response' returns True then
         ExtractorErrorResponse is raised"""
        # created mock kraken response extractor
        kraken_response = kraken_mock()
        # set return value for is_error_response to True
        kraken_response.is_error_response.return_value = True
        response_extractor = ResponseExtractor()
        with self.assertRaises(ExtractorErrorResponse):
            response_extractor.extract_response(kraken_response)

    def test_iterator(self):
        """Test ResponseExtractor can be used as an iterator and when iterated
        it iterates over the extractor"""
        kraken_extractor = KrakenResponseExtractor(self.VALID_RESPONSE,
                                                   self.VALID_RESPONSE_SYMBOL)
        response_extractor = ResponseExtractor()
        response_extractor.extract_response(kraken_extractor)
        serialized_result = [i for i in response_extractor]
        print(f'serialized_result {serialized_result}')
        self.assertGreater(len(serialized_result), 0)




