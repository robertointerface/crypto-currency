import json
from django.test import TestCase
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate
from data_loader.save_crypto_names import create_kraken_symbols
from crypto_data.models import KrakenSymbols
from crypto_data import views


# set up the data creation for the test on the module level
def setUpModule():
    create_kraken_symbols('USD')


KRAKEN_SYMBOL_SERIALIZER_FIELDS = ['url',
                                   'coin_name',
                                   'coin_symbol',
                                   'currency',
                                   'symbol',
                                   'related_OHLC']

class TestKrakenSymbolsListView(TestCase):
    """Test list and create operation for view KrakenSymbolsList"""
    VALID_CURRENCY = 'USD'

    # @classmethod
    # def setUpClass(cls):
    #     """Create kraken symbols in data base in order to test serializer"""
    #     create_kraken_symbols(cls.VALID_CURRENCY)

    def setUp(self):
        self.factory = APIRequestFactory()

    # @classmethod
    # def tearDownClass(cls):
    #     # no need to do anything as content is not really saved in database
    #     # still need to define class to avoid error.
    #     pass

    def test_view_returns_correct_serializer_fields(self):
        """Test View returns correct fields with get operation"""
        request = self.factory.get('crypto-data/kraken-symbols/',
                                   content_type='application/json')
        view = views.KrakenSymbolsList.as_view()
        response = view(request)
        print(f'response.dat {response.data}')
        # get the ordered dict response as view response has not yet been
        # converted to JSON object.
        if response.status_code == status.HTTP_200_OK:
            json_response = response.data[0]
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
        request = self.factory.post('crypto-data/kraken-symbols/',
                                    json.dumps(data),
                                    content_type='application/json')
        view = views.KrakenSymbolsList.as_view()
        response = view(request)
        if response.status_code == status.HTTP_201_CREATED:
            created_object = get_object_or_404(KrakenSymbols, symbol='TCEUR')
            self.assertIsNotNone(created_object)
        else:
            self.fail(f"response returned {response.status_code}")


class TestKrakenSymbolsDetailView(TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     """Create kraken symbols in data base in order to test serializer"""
    #     create_kraken_symbols(cls.VALID_CURRENCY)

    def setUp(self):
        self.factory = APIRequestFactory()

    # @classmethod
    # def tearDownClass(cls):
    #     # no need to do anything as content is not really saved in database
    #     # still need to define class to avoid error.
    #     pass

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






