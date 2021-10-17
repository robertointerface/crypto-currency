import json
from django.test import TestCase
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate
from data_loader.save_crypto_names import create_kraken_symbols
from crypto_data.serializers import KrakenSymbolSerializer
from crypto_data.models import KrakenSymbols
from crypto_data import views


class TestKrakenSymbolsListView(TestCase):
    """Test list and create operation for view KrakenSymbolsList"""
    VALID_CURRENCY = 'USD'
    KrakenSymbolSerializer_fields = ['url',
                                     'coin_name',
                                     'coin_symbol',
                                     'currency',
                                     'symbol',
                                     'related_OHLC']
    @classmethod
    def setUpClass(cls):
        """Create kraken symbols in data base in order to test serializer"""
        create_kraken_symbols(cls.VALID_CURRENCY)

    def setUp(self):
        self.factory = APIRequestFactory()

    @classmethod
    def tearDownClass(cls):
        # no need to do anything as content is not really saved in database
        # still need to define class to avoid error.
        pass

    def test_view_returns_correct_serializer_fields(self):
        """Test View returns correct fields with get operation"""
        request = self.factory.get('crypto-data/kraken-symbols/',
                                   content_type='application/json')
        view = views.KrakenSymbolsList.as_view()
        response = view(request)
        # get the ordered dict response as view response has not yet been
        # converted to JSON object.
        if response.status_code == status.HTTP_200_OK:
            json_response = response.data[0]
            self.assertCountEqual(json_response.keys(),
                                  self.KrakenSymbolSerializer_fields)
        else:
            self.fail(f"response returned {response.status_code}")

