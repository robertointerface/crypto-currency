from rest_framework import serializers
from crypto_data.models import KrakenSymbols, KrakenOHLC


class KrakenSymbolSerializer(serializers.HyperlinkedModelSerializer):
    related_OHLC = serializers.HyperlinkedRelatedField(many=True,
                                                    read_only=True,
                                                    view_name='krakensymbols-detail')
    class Meta:
        model = KrakenSymbols
        # you could also just define exclude=[pk] but it makes it easier to
        # define all used fields and not having to go to models file to look
        # at it all the time

        fields = ('url',
                  'coin_name',
                  'coin_symbol',
                  'currency',
                  'symbol',
                  'related_OHLC')


class KrakenOHLCSerializer(serializers.HyperlinkedModelSerializer):
    symbol = serializers.SlugRelatedField(
        queryset=KrakenSymbols.objects.all(),
        slug_field='symbol',
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

