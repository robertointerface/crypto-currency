"""load crypto data into Postgres sql database"""
import logging
from collections.abc import Iterator
from requests.exceptions import HTTPError
from rest_framework.serializers import ValidationError
from crypto_data.models import (KrakenSymbols,
                                KrakenOHLC)
from .kraken_data_loader import KrakenContentFetcher, KrakenResponseExtractor
from .response_extractor import ResponseExtractor
from .errors import ExtractorErrorResponse, NonRelatedResponseError
from crypto_data.serializers import KrakenOHLCSerializer

#START_DATE = 1570834800  # 12/oct/2019 00:00:00
START_DATE = 1627772400
END_DATE = 1633993200  # 12/oct/2021 00:00:00
INCREMENT_STEPS = 1440  # 60 minutes * 24 hours, increments by day
KRAKEN_URLS = {
    'OHLC': 'https://api.kraken.com/0/public/OHLC'
}

logger = logging.getLogger(__name__)
f_handler = logging.FileHandler('logs/kraken_extractor.log',
                                mode='a',
                                encoding='utf-8')
f_handler.setLevel(logging.WARNING)
f_format = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
f_handler.setFormatter(f_format)
f_handler.setLevel(logging.ERROR)
logger.addHandler(f_handler)

c_handler = logging.StreamHandler(__name__)
c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)



def fetch_data(fetcher):
    """Fetch data from a given object"""
    try:
        return fetcher.fetch()
    except HTTPError as e:
        logger.error(f'HTTPError because {e.args}')
        raise ExtractorErrorResponse from e
    except AttributeError as e:
        raise ExtractorErrorResponse from e

def save_OHLC_data_on_database(data_iterator: Iterator, related_symbol):
    for serializer_data in data_iterator:
        #print(f'serializer_data {serializer_data}')
        serializer_data['symbol'] = related_symbol
        serializer = KrakenOHLCSerializer(data=serializer_data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        except ValidationError as e:
            print(f'ValidationError {e}')
            print(f'//////////////////////////')

def load_kraken_data_into_postgres(data_type: str):
    url = KRAKEN_URLS.get(data_type)
    if url is not None:
        # get all the saved symbols
        # iterate over
        kraken_symbols = KrakenSymbols.objects.all()
        for symbol in kraken_symbols:
            print('///////////////////////////////')
            print(f'loading data for {symbol.symbol}')
            params = {
                'pair': symbol.symbol,
                'since': START_DATE,
                'interval': INCREMENT_STEPS,
            }
            try:
                fetcher = KrakenContentFetcher(url, params)
                response = fetch_data(fetcher)
                #print(f'response form { symbol.symbol} {response}')
                kraken_extractor = KrakenResponseExtractor(response,
                                                           symbol.symbol)
                response_extractor = ResponseExtractor()
                response_extractor.extract_response(kraken_extractor)
                #serialized_result = [i for i in response_extractor]
                #print(f'serialized_result {len(serialized_result)}')
                save_OHLC_data_on_database(response_extractor, symbol.symbol)
            except (ExtractorErrorResponse, NonRelatedResponseError) as e:
                # at this stage the error that provoked this has already
                # been logged into log file, so just pass the error and try
                # next symbol
                #logger.warning(f'ExtractorErrorResponse {e}')
                print(f'ERROR FETCHING DATA FOR  {symbol.symbol} {e}')
                pass
