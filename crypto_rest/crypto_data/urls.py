from django.conf.urls import url
from crypto_data import views
app_names = 'crypto_data'

urlpatterns = [
    url(r'kraken-symbols/$',
        views.KrakenSymbolsList.as_view(),
        name=views.KrakenSymbolsList.name
        ),
    url(r'kraken-symbols/(?P<pk>[0-9]+)$',
        views.KrakenSymbolsDetail.as_view(),
        name=views.KrakenSymbolsDetail.name)
]