from rest_framework import serializers
from crypto_data.models import KrakenSymbols, KrakenOHLC


class KrakenSymbolSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = KrakenSymbols
        fields = '__all__'


class KrakenOHLCSerializer(serializers.HyperlinkedModelSerializer):
    symbol = serializers.SlugRelatedField(
        queryset=KrakenSymbols.objects.all(),
        slug_field='symbol'
    )

    class Meta:
        model = KrakenOHLC
        fields = ('url',
                  'open',
                  'high',
                  'low',
                  'close',
                  'symbol',
                  'date')

