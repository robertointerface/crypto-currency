from rest_framework import serializers
from crypto_data.models import KrakenSymbols, KrakenOHLC


class KrakenSymbolSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = KrakenSymbols
        fields = '__all__'


class KrakenOHLCSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = KrakenOHLC
        fields = '__all__'

