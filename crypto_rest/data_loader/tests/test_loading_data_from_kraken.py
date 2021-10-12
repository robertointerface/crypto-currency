"""
Tests for module kraken_data_loader, test loading data from kraken website
and save it on SQL database using models on app crypto_data
"""
from django.test import TestCase
from data_loader.kraken_data_loader import convert_unix_to_date


class TestDataLoader(TestCase):


    def test_convert_unix_to_date(self):
        """Test convert unix timestamp to a date that can be easier to read"""
        unix_time = 1634008620
        date = convert_unix_to_date(unix_time)
        self.assertEqual(date, '12/10/2021')

