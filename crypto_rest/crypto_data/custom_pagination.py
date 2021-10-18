from rest_framework.pagination import PageNumberPagination
PAGE_SIZE_OHLC = 10
PAGE_SIZE_SYMBOL = 6


class KrakenSymbolsPagination(PageNumberPagination):
    page_size = PAGE_SIZE_SYMBOL


class KrakenOHLCPagination(PageNumberPagination):
    page_size = PAGE_SIZE_OHLC

