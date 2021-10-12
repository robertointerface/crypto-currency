"""
Define models to store crypto data
"""
from django.db import models


class KrakenSymbols(models.Model):
    """
    Store the Kraken symbols required to query data from kraken.com.
    The symbol is a combination of the coin symbol and the currency; first
    is the coin symbol and second is the currency symbol i.e BTCUSD, BTC is
    symbol for Bitcoin and USD for US Dollars.
    """
    US_DOLLARS = 'USD'
    BRITISH_POUND = 'GBP'
    EURO = 'EUR'
    JAPAN_YEN = 'JPY'
    CURRENCY_TYPES = [
        (US_DOLLARS, 'US dollar'),
        (BRITISH_POUND, 'British pound'),
        (EURO, 'Euro'),
        (JAPAN_YEN, 'Japanese Yen'),
    ]
    coin_name = models.CharField(max_length=40)
    coin_symbol = models.CharField(max_length=10)
    currency = models.CharField(max_length=3,
                                choices=CURRENCY_TYPES)
    symbol = models.CharField(max_length=13,
                              unique=True)

    def __repr__(self):
        class_name = self.__class__.__name__
        return f'<{class_name} {self.symbol}>'

    def __str__(self):
        return f'{self.coin_name} {self.symbol}'


class KrakenOHLC(models.Model):
    """
    Open-High-low-Close data for an specific kraken symbol (price of coin at
    specific currency) at an specific date.
    - Open: the price at which it opened that date, as Crypto trade 24/7 this is
    midnight.
    - High: the highest price during that date.
    - Low: lowest price during that date.
    - Close: the price at which it close, this is 1 minute before midnight as
    crypto Trade 24/7.
    """
    open = models.DecimalField(max_digits=11,
                               decimal_places=2)
    high = models.DecimalField(max_digits=11,
                               decimal_places=2)
    low = models.DecimalField(max_digits=11,
                              decimal_places=2)
    close = models.DecimalField(max_digits=11,
                                decimal_places=2)
    symbol = models.ForeignKey('crypto_data.KrakenSymbols',
                               related_name='related_OHLC',
                               on_delete=models.CASCADE)
    date = models.DateField()

    def __repr__(self):
        class_name = self.__class__.__name__
        return f'<{class_name} {self.symbol} {self.date}>'

    def __str__(self):
        return f'OHLC for {self.symbol} on {self.date}'
