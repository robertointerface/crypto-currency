from django.urls import re_path
from crypto_data import views
app_names = 'crypto_data'

urlpatterns = [
    re_path(r'^kraken-symbols/$',
        views.KrakenSymbolsList.as_view(),
        name=views.KrakenSymbolsList.name
        ),
    re_path(r'^kraken-symbols/(?P<pk>[0-9]+)$',
        views.KrakenSymbolsDetail.as_view(),
        name=views.KrakenSymbolsDetail.name),
    re_path(r'^kraken-ohlc/$',
            views.KrakenOHLCList.as_view(),
            name=views.KrakenOHLCList.name,
            ),
    re_path(r'^kraken-ohlc/(?P<pk>[0-9]+)$',
            views.KrakenOHLCDetail.as_view(),
            name=views.KrakenOHLCDetail.name,
            ),
]