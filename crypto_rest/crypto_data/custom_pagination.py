"""Define pagination"""
from rest_framework.pagination import PageNumberPagination
PAGE_SIZE_OHLC = 10
PAGE_SIZE_SYMBOL = 6
MAX_PAGE_SIZE = 20


class KrakenSymbolsPagination(PageNumberPagination):
    """Pagination for views returning KrakenSymbols"""
    page_size = PAGE_SIZE_SYMBOL
    max_page_size = MAX_PAGE_SIZE
    page_size_query_param = 'page_size'


class KrakenOHLCPagination(PageNumberPagination):
    """Pagination for views returning KrakenOHLC"""
    page_size = PAGE_SIZE_OHLC
    max_page_size = MAX_PAGE_SIZE
    page_size_query_param = 'page_size'
