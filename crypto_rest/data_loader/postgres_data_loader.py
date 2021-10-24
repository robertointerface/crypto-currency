"""load crypto data into Postgres sql database"""
import logging
from collections.abc import Iterator
from requests.exceptions import HTTPError
from rest_framework.serializers import ValidationError
from crypto_data.models import KrakenSymbols
from crypto_data.serializers import KrakenOHLCSerializer
from data_loader.kraken_data_loader import KrakenContentFetcher, KrakenResponseExtractor
from data_loader.response_extractor import ResponseExtractor
from data_loader.errors import ExtractorErrorResponse, NonRelatedResponseError


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
    """
    Fetch data from a given instance, the instance must follow interface as
    ABC class ContentResourceFetcher at resource_content_abs.
    """
    try:
        return fetcher.fetch()
    except HTTPError as e:
        logger.error(f'HTTPError because {e.args}')
        raise ExtractorErrorResponse from e
    except AttributeError as e:
        raise ExtractorErrorResponse from e

# improve this method in the future to not use the same serializer
# KrakenOHLCSerializer, use different serializer depending on the ocasssion
# this could be done by creating a serializer with a factory method or similar.
def save_OHLC_data_on_database(data_iterator: Iterator, related_symbol: str):
    """Iterate over a collection of dicts that contain the necessary parameters
    to create a KrakenOHLCSerializer and save it without raising a validation
    exception
    @args:
        - data_iterator: instance with __iter__ or __getitem__ implemented, to
        comply with iterator protocol.
        - related_symbol: related symbol to be included on KrakenOHLCSerializer
    @returns:
        - On Success: save all items on on as KrakenOHLCSerializer.
        - On Failure: raise ValidationError.
    """
    for serializer_data in data_iterator:
        serializer_data['symbol'] = related_symbol
        serializer = KrakenOHLCSerializer(data=serializer_data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        except ValidationError as e:
            # log in here validation error and pass
            logger.error(f'Validation error for symbol {related_symbol}'
                         f'{e}')


def load_kraken_data_into_postgres(data_type: str):
    """Provided a data type (OHLC, ), Load data from kraken api of that specific type,
    data is related to all the symbols already saved at KrakenSymbols.
    """
    url = KRAKEN_URLS.get(data_type)
    if url is not None:
        # get all the saved symbols
        # iterate over each one to extract all the data from a specified time.
        kraken_symbols = KrakenSymbols.objects.all()
        for symbol in kraken_symbols:
            # prepare query parameters
            params = {
                'pair': symbol.symbol,
                'since': START_DATE,
                'interval': INCREMENT_STEPS,
            }
            try:
                # create fetcher and try to fetch the data
                fetcher = KrakenContentFetcher(url, params)
                response = fetch_data(fetcher)
                """use a KrakenResponseExtractor with the returned response 
                from kraken to extract data in a format that serializer 
                KrakenOHLCSerializer can use."""
                kraken_extractor = KrakenResponseExtractor(response,
                                                           symbol.symbol)
                response_extractor = ResponseExtractor()
                response_extractor.extract_response(kraken_extractor)
                save_OHLC_data_on_database(response_extractor, symbol.symbol)
            except (ExtractorErrorResponse, NonRelatedResponseError) as e:
                # at this stage the error that provoked this has already
                # been logged into log file, so just print the error and try
                # next symbol
                print(f'ERROR FETCHING DATA FOR  {symbol.symbol} {e}')
