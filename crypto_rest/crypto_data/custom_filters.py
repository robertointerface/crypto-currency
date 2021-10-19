"""Define Filters to be used on generic views"""
from django_filters import rest_framework as filters
from django_filters import NumberFilter
from .models import KrakenOHLC


class KrakenOHLCFilter(filters.FilterSet):
    """Filter for model KrakenOHLC
    - min_open: Minimum value for open, return any value above min_open
    - min_low: minimum value for low, return any value above min_low.
    - max_high: maximum value for high, return any value below.
    - max_close: maximum value for close, return any value below.
    """
    min_open = NumberFilter(field_name='open', lookup_expr='gte')
    min_low = NumberFilter(field_name='low', lookup_expr='gte')
    max_high = NumberFilter(field_name='high', lookup_expr='lte')
    max_close = NumberFilter(field_name='close', lookup_expr='lte')

    class Meta:
        model = KrakenOHLC
        fields = (
            'symbol',
        )
