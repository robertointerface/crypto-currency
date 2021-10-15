import logging
from django.db import transaction
from rest_framework.serializers import ValidationError
from crypto_data.serializers import KrakenSymbolSerializer



BITCOIN = 'BTC'
ETHERUM = 'ETH'
THETHER_USD = 'USDT'
CARDANO = 'ADA'
RIPPLE = 'XRP'
SOLANA = 'SOL'

COINS_TO_CREATE = [
    ('bitcoin', BITCOIN),
    ('etherum', ETHERUM),
    ('thether usd', THETHER_USD),
    ('cardano', CARDANO),
    ('ripple', RIPPLE),
    ('solana', SOLANA)
]

logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler()
c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)

def get_validation_error(error):
    def create_error_message(error_field, error_messages):
        return f"error at {error_field}, " \
               f"{', '.join([message for message in error_messages])}"

    if error.detail is not None:
        error_messages = [create_error_message(k, v)
                          for k, v in error.detail.items()]
        return '; '.join(error_messages)


def create_kraken_symbols(currency):
    """Create KrakenSymbols instances by providing a currency, each coin on
    COINS_TO_CREATE is combined with the currency and saved."""
    try:
        with transaction.atomic():
            for c in COINS_TO_CREATE:
                coin_name, coin_symbol = c
                symbol_data = {
                    'coin_name': coin_name,
                    'coin_symbol': coin_symbol,
                    'currency': currency,
                    'symbol': f'{coin_symbol}{currency}'
                }
                symbol_ser = KrakenSymbolSerializer(data=symbol_data)
                if symbol_ser.is_valid(raise_exception=True):
                    symbol_ser.save()
    except ValidationError as e:
        validation_errors = get_validation_error(e)
        logger.exception(f"Fields are not valid {validation_errors}")
    except Exception as e:
        logging.exception("Exception occurred")