from .models import KrakenOHLC
from django_filters import rest_framework as filters
from django_filters import NumberFilter


class KrakenOHLCFilter(filters.FilterSet):
    min_open = NumberFilter(field_name='open', lookup_expr='gte')
    min_low = NumberFilter(field_name='low', lookup_expr='gte')
    max_high = NumberFilter(field_name='high', lookup_expr='lte')
    max_close = NumberFilter(field_name='close', lookup_expr='lte')

    class Meta:
        model = KrakenOHLC
        fields = (
            'symbol',
        )