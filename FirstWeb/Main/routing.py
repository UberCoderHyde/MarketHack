from django.urls import re_path
from .consumers import StockConsumer
ws_urlpatterns = [ 
    re_path(r'ws/stock/(?P<stock>\w+)/$',StockConsumer.as_asgi()) 
]