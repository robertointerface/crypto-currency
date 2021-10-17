from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from crypto_data.models import KrakenOHLC, KrakenSymbols
from crypto_data.serializers import (KrakenSymbolSerializer,
                                     KrakenOHLCSerializer)


class KrakenSymbolsList(generics.ListCreateAPIView):
    queryset = KrakenSymbols.objects.all()
    serializer_class = KrakenSymbolSerializer
    name = 'krakensymbol-list' # need to describe name to find hyperlink


class KrakenSymbolsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = KrakenSymbols.objects.all()
    serializer_class = KrakenSymbolSerializer
    name = 'krakensymbols-detail'

