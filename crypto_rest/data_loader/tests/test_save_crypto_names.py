from django.test import TestCase
from crypto_data.models import KrakenSymbols
from data_loader.save_crypto_names import (create_kraken_symbols,
                                           COINS_TO_CREATE)


class TestCreateKrakenSymbols(TestCase):
    """Test method create_kraken_symbols"""


    def test_instances_are_saved(self):
        """Test instances are saved on database when correct fields are
        provided.
        """
        currency = 'USD'
        create_kraken_symbols(currency)
        saved_symbols = (KrakenSymbols.objects
                         .filter(currency=currency)
                         .count())
        self.assertEqual(len(COINS_TO_CREATE), saved_symbols)

    def test_instances_are_not_saved(self):
        currency = 'NON_EXISTING_CURRENCY'
        create_kraken_symbols(currency)
        saved_symbols = (
            KrakenSymbols.objects.filter(currency=currency).count())
        self.assertEqual(0, saved_symbols)