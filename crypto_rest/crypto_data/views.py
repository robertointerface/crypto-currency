from rest_framework import generics
from django_filters import rest_framework as d_filter
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .custom_filters import KrakenOHLCFilter
from crypto_data.models import KrakenOHLC, KrakenSymbols
from crypto_data.serializers import (KrakenSymbolSerializer,
                                     KrakenOHLCSerializer)
from .custom_pagination import KrakenSymbolsPagination, KrakenOHLCPagination

"""
All the above could be also implemented using APIView as method/class
but this tends to create a lot of repetitive code. Generic Views are more 
consistent and easier to read and they provide all the functionality for all
CRUD operations, use APIViews if extra functionality is required like 
connecting to storage, creating csv files...
"""


class KrakenSymbolsList(generics.ListCreateAPIView):
    """List and Create KrakenSymbols"""
    queryset = KrakenSymbols.objects.all()
    serializer_class = KrakenSymbolSerializer
    name = 'krakensymbol-list' # need to describe name to find hyperlink
    pagination_class = KrakenSymbolsPagination


class KrakenSymbolsDetail(generics.RetrieveUpdateDestroyAPIView):
    """get single, put, patch, delete KrakenSymbols"""
    queryset = KrakenSymbols.objects.all()
    serializer_class = KrakenSymbolSerializer
    name = 'krakensymbols-detail'


class KrakenOHLCList(generics.ListCreateAPIView):
    """List and created KrakenOHLC"""
    queryset = KrakenOHLC.objects.all()
    serializer_class = KrakenOHLCSerializer
    name = 'Krakenohlc-list'
    pagination_class = KrakenOHLCPagination
    filter_backends = (d_filter.DjangoFilterBackend,
                       filters.SearchFilter )
    filterset_class = KrakenOHLCFilter
    search_fields = ('^symbol__symbol', )


class KrakenOHLCDetail(generics.RetrieveUpdateDestroyAPIView):
    """Get single, put, patch, delete KrakenOHLC"""
    queryset = KrakenOHLC.objects.all()
    serializer_class = KrakenOHLCSerializer
    name = 'krakenohlc-detail'


class APIRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'kraken-symbols': reverse(KrakenSymbolsList.name, request=request),
            'kraken-ohlc': reverse(KrakenOHLCList.name, request=request)
        })






