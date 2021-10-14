from rest_framework import serializers
from crypto_data.models import KrakenSymbols


class KrakenSymbolSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = KrakenSymbols
        fields = '__all__'

