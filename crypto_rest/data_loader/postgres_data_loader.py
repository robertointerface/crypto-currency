"""load crypto data into Postgres sql database"""
from crypto_data.models import (KrakenSymbols,
                                KrakenOHLC)
from .kraken_data_loader import KrakenContentFetcher, KrakenResponseExtractor


START_DATE = 1570834800  # 12/oct/2019 00:00:00
END_DATE = 1633993200  # 12/oct/2021 00:00:00
INCREMENT_STEPS = 1440  # 60 minutes * 24 hours, increments by day
KRAKEN_URLS = {
    'OHLC': 'https://api.kraken.com/0/public/OHLC'
}


def load_kraken_data_into_postgres(data_type: str):
    url = KRAKEN_URLS.get(data_type)
    if url is not None:
        # get all the saved symbols
        # iterate over
        kraken_symbols = KrakenSymbols.objects.all()
        for symbol in kraken_symbols:
            params = {
                'pair': symbol.symbol,
                'since': START_DATE,
                'interval': INCREMENT_STEPS,
            }
            fetcher = KrakenContentFetcher(url, params)
            response = fetcher.fetch()
            kraken_extractor = KrakenResponseExtractor(response, symbol.symbol)

            # initialize KrakenResponseExtractor with response and symbol.symbol
            # initalize ResponseExtractor
            # call extract_response
            #iterate and push to method to serialize and save
    pass


