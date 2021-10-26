import datetime
from django.test import TestCase
from data_loader.save_crypto_names import create_kraken_symbols
from data_loader.postgres_data_loader import load_kraken_data_into_postgres
from data_display.load_data import LoadDataFromPostSQl

class TestLoadDataFromPostSQl(TestCase):

    @classmethod
    def setUpClass(cls):
        # load kraken symbols into database to test
        create_kraken_symbols('USD')
        load_kraken_data_into_postgres('OHLC')

    @classmethod
    def tearDownClass(cls):
        return

    def test_load_data_filter_symbol(self):
        """Assert all items loaded belong to the requested symbol"""
        test_instance = LoadDataFromPostSQl('BTCUSD', "2021-08-01")
        test_instance.load_data()
        loaded_data = test_instance.get_response()
        [self.assertEqual(i.symbol.symbol, 'BTCUSD') for i in loaded_data]

    def test_load_data_filter_date(self):
        """Assert all items loaded have a date greater than or equal than
        the requested one"""
        test_instance = LoadDataFromPostSQl('BTCUSD', "2021-08-01")
        test_instance.load_data()
        loaded_data = test_instance.get_response()
        started_date = datetime.date(2021, 8, 1)
        [self.assertGreaterEqual(i.date, started_date)
         for i in loaded_data]

    def test_systemExit_is_raised(self):
        """Assert SystemExit is raised if no data is found"""
        test_instance = LoadDataFromPostSQl('NONVALID', "2021-08-01")
        with self.assertRaises(SystemExit):
            test_instance.load_data()