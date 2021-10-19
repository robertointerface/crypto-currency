"""Test serializers and APIViews return correct responses"""
import json
import datetime
import functools
from django.test import TestCase
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.test import APIRequestFactory
from data_loader.postgres_data_loader import load_kraken_data_into_postgres
from data_loader.save_crypto_names import create_kraken_symbols
from crypto_data.models import KrakenSymbols
from crypto_data import views
from crypto_data.custom_pagination import PAGE_SIZE_OHLC, MAX_PAGE_SIZE


SEND_DATA_METHODS = ['post', 'put', 'patch']
GET_DATA_METHODS = ['get', 'options']


def setUpModule():
    """set up the data creation for the test on the module level"""
    create_kraken_symbols('USD')


KRAKEN_SYMBOL_SERIALIZER_FIELDS = ['url',
                                   'coin_name',
                                   'coin_symbol',
                                   'currency',
                                   'symbol',
                                   'related_OHLC']

def get_result_list(result_data):
    """Get result from Rest api call, in case is paginated the result is under
    the key 'results'"""
    if result_data.get('results') is not None:
        return result_data.get('results')
    return result_data

"""
AUTHENTICATE USERS.
No authentication is implemented at the moment but in order to test 
authentication the simplest approach is to use force_authenticate from 
from rest_framework.test, other alternative is to request the token auth
and use it, but there is no point on keep doing this for all the tests if 
you have tested your authentication and know is functioning correctly.

1 - create a fake user
2 - force authenticate the fake user on a view like
    force_authenticate(request, fake_user)
3 - set the user on the request with 
    request.user = fake_user
4 - call the view as always."""

class TestKrakenSymbolsListView(TestCase):
    """Test list and create operation for view KrakenSymbolsList"""
    VALID_CURRENCY = 'USD'

    def setUp(self):
        self.factory = APIRequestFactory()

    def valid_request_arg(func):
        """validate request method is a valid/safe one"""
        @functools.wraps(func)
        def validate(self, *args, **kwargs):
            method, *_ = args
            if method in [*SEND_DATA_METHODS, *GET_DATA_METHODS]:
                return func(self, *args, **kwargs)
            raise AttributeError(
                f'request method {method} is not valid, must be '
                f'post, put, patch, get, options')
        return validate

    @valid_request_arg
    def create_request(self, method, url, **kwargs):
        """Create a REST API request call to be used for testing.
        @args:
            - method: request CRUD method.
            - url: request url
        @Return:
            - on success: APIRequestFactory request ready to be used on a view.
            - on failure: raise corresponding error.
        """
        # if is a method that will send data, the data needs to be JSONIFY
        if method in SEND_DATA_METHODS:
            request_data = kwargs.get('request_data', {})
            request_method = getattr(self.factory, method)
            request = request_method(url,
                                     data=json.dumps(request_data),
                                     content_type='application/json')
        else:
            request_method = getattr(self.factory, method)
            request = request_method(url)
        return request

    def test_view_returns_correct_serializer_fields(self):
        """Test View returns correct fields with get operation"""
        request = self.create_request('get', 'crypto-data/kraken-symbols/')
        view = views.KrakenSymbolsList.as_view()
        response = view(request)
        #print(f'response.dat {json.dumps(response.data)}')
        # get the ordered dict response as view response has not yet been
        # converted to JSON object.
        if response.status_code == status.HTTP_200_OK:
            json_response = get_result_list(response.data)[0]
            self.assertCountEqual(json_response.keys(),
                                  KRAKEN_SYMBOL_SERIALIZER_FIELDS)
        else:
            self.fail(f"response returned {response.status_code}")

    def test_post_request(self):
        """Test post request saves KrakenSymbols"""
        data = {'coin_name': 'Test coin',
                'coin_symbol': 'TC',
                'currency': 'EUR',
                'symbol': 'TCEUR'}
        test_url = 'crypto-data/kraken-symbols/'
        request = self.create_request('post',
                                      test_url,
                                      **{'request_data': data})
        view = views.KrakenSymbolsList.as_view()
        response = view(request)
        if response.status_code == status.HTTP_201_CREATED:
            created_object = get_object_or_404(KrakenSymbols, symbol='TCEUR')
            self.assertIsNotNone(created_object)
        else:
            self.fail(f"response returned {response.status_code}")



class TestKrakenSymbolsDetailView(TestCase):
    """Test KrakenSymbolsDetail APIView"""
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_get_request(self):
        """Test get request returns correct object"""
        request = self.factory.get('crypto-data/kraken-symbols/1')
        view = views.KrakenSymbolsDetail.as_view()
        response = view(request, pk=1)
        if response.status_code == status.HTTP_200_OK:
            self.assertCountEqual(response.data.keys(),
                                  KRAKEN_SYMBOL_SERIALIZER_FIELDS)

    def test_patch_request(self):
        """Test patch method does not modify symbol even when provided"""
        data_to_patch = {
            'coin_symbol': 'BTCI',
            'symbol': 'TCDD'
        }
        request = self.factory.patch('crypto-data/kraken-symbols/1',
                                     json.dumps(data_to_patch),
                                     content_type='application/json')
        view = views.KrakenSymbolsDetail.as_view()
        response = view(request, pk=1)
        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.data.get('symbol'), 'BTCIUSD')

    def test_put_request(self):
        """Test put requests modifies all fields"""
        data_to_put = {
            'coin_name': 'Etherum 2',
            'coin_symbol': 'ETH2',
            'currency': 'GBP',
        }
        request = self.factory.put('crypto-data/kraken-symbols/2',
                                    json.dumps(data_to_put),
                                    content_type='application/json')
        view = views.KrakenSymbolsDetail.as_view()
        response = view(request, pk=1)
        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.data.get('coin_name'), 'Etherum 2')
            self.assertEqual(response.data.get('coin_symbol'), 'ETH2')
            self.assertEqual(response.data.get('currency'), 'GBP')
            self.assertEqual(response.data.get('symbol'), 'ETH2GBP')


class TestKrakenOHLCListView(TestCase):

    @classmethod
    def setUpClass(cls):
        """Create OHLC objects to be able to test CRUD operations on them"""
        load_kraken_data_into_postgres('OHLC')

    @classmethod
    def tearDownClass(cls):
        # no need to do anything as content is not really saved in database
        # still need to define class to avoid error.
        pass

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_get_request(self):
        """Test get request returns the default page size number of items"""
        request = self.factory.get('crypto-data/kraken-ohlc/',
                                   content_type='application/json')
        view = views.KrakenOHLCList.as_view()
        response = view(request)
        json_response = get_result_list(response.data)

        # assert return response corresponds to page_size
        self.assertEqual(len(json_response), PAGE_SIZE_OHLC)

    def test_get_request_max_page_size(self):
        """Test get request does not return more items than the max set on
        pagination parameter max_page_size"""
        request = self.factory.get('crypto-data/kraken-ohlc/?page_size=30',
                                   content_type='application/json')
        view = views.KrakenOHLCList.as_view()
        response = view(request)
        json_response = get_result_list(response.data)
        self.assertLessEqual(len(json_response), MAX_PAGE_SIZE)

    def greater_than_or_equal(self, x, field):
        def greater_than_or_equal_specified(y):
            return self.assertGreaterEqual(y, x,
                                           f'{y} is not >= {x} for {field}')
        return greater_than_or_equal_specified

    def less_than_or_equal(self, x, field):
        def less_than_or_equal_specified(y):
            return self.assertLessEqual(y, x,
                                        f'{y} is not <= {x} for {field}')
        return less_than_or_equal_specified

    def test_filter_fields(self):
        """Test request will use filter correctly"""
        min_open = 200
        min_low = 70
        max_high = 23
        max_close = 4
        # define test cases
        # you could do this with name tuples to be more pythonic
        test_cases = [
            (
                f'crypto-data/kraken-ohlc/?min_open={min_open}',
                self.greater_than_or_equal(min_open, 'open'),
                'open'
             ),
            (
                f'crypto-data/kraken-ohlc/?min_low={min_low}',
                self.greater_than_or_equal(min_low, 'low'),
                'low'
            ),
            (
                f'crypto-data/kraken-ohlc/?max_high={max_high}',
                self.less_than_or_equal(max_high, 'high'),
                'high'
            ),
            (
                f'crypto-data/kraken-ohlc/?max_close={max_close}',
                self.less_than_or_equal(max_close, 'close'),
                'close'
            )
        ]
        for test in test_cases:
            url, test_func, field = test
            # perform request with provided url
            request = self.factory.get(url)
            view = views.KrakenOHLCList.as_view()
            response = view(request)
            json_response = get_result_list(response.data)
            # first test we have result, otherwise it might give False positive
            self.assertGreater(len(json_response), 0)
            # assert returned items are correct by testing provided function
            [test_func(float(i.get(field))) for i in json_response]

    def test_search_field(self):
        """Test search_fields returns correctly"""
        request = self.factory.get('crypto-data/kraken-ohlc/?search=ETHUSD')
        view = views.KrakenOHLCList.as_view()
        response = view(request)
        json_response = get_result_list(response.data)
        [self.assertEqual(i.get('symbol'), 'ETHUSD') for i in json_response]

    def test_post_request(self):
        """Test post request creates object"""
        post_data = {
            'open': 149.9,
            'high': 151.30,
            'low': 147.95,
            'close': 150.5,
            'symbol': 'BTCUSD',
            'date': datetime.datetime.today().strftime('%Y-%m-%d')
        }
        request = self.factory.post('crypto-data/kraken-ohlc/',
                                   data=json.dumps(post_data),
                                   content_type='application/json')
        view = views.KrakenOHLCList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)






