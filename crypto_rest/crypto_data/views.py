from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from crypto_data.models import KrakenOHLC, KrakenSymbols
from crypto_data.serializers import (KrakenSymbolSerializer,
                                     KrakenOHLCSerializer)
from .custom_pagination import KrakenSymbolsPagination, KrakenOHLCPagination

"""All the above could be also implemented using APIView as method/class
but this tends to create a lot of repetitive code. Generic Views are more 
consistent and easier to read and they provide all the functionality for all
CRUD operations, use APIViews if extra functionality is required like 
connecting to storage, creating csv files...
"""


class KrakenSymbolsList(generics.ListCreateAPIView):
    queryset = KrakenSymbols.objects.all()
    serializer_class = KrakenSymbolSerializer
    name = 'krakensymbol-list' # need to describe name to find hyperlink
    pagination_class = KrakenSymbolsPagination

class KrakenSymbolsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = KrakenSymbols.objects.all()
    serializer_class = KrakenSymbolSerializer
    name = 'krakensymbols-detail'


class KrakenOHLCList(generics.ListCreateAPIView):
    queryset = KrakenOHLC.objects.all()
    serializer_class = KrakenOHLCSerializer
    name = 'Krakenohlc-list'
    pagination_class = KrakenOHLCPagination

class KrakenOHLCDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = KrakenOHLC.objects.all()
    serializer_class = KrakenOHLCSerializer
    name = 'krakenohlc-detail'

