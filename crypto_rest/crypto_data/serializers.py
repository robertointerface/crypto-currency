import numbers
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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

    def update(self, instance, validated_data):
        """instance symbol is a combination of coin_symbol and coin_currency
         therefore this field should not be updated directly by the user. We
         could also create our own validation process to discard any calls
         which include symbol but this is a much simpler and readable way"""
        instance.coin_name = validated_data.get('coin_name', instance.coin_name)
        coin_symbol = validated_data.get('coin_symbol', instance.coin_symbol)
        coin_currency = validated_data.get('currency', instance.currency)
        symbol = f'{coin_symbol}{coin_currency}'
        instance.coin_symbol = coin_symbol
        instance.currency = coin_currency
        instance.symbol = symbol
        instance.save()
        return instance


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

