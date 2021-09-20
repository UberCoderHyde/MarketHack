from django.urls import path
from . import views
urlpatterns = [
    path('test/', views.test, name="test"),
    path('search/', views.search_address),
    path('', views.home, name="home"),
    path('stock/<str:name>',views.stock),
    path('sectors/', views.sectors, name="sectors"),
    path('trending/', views.trending, name="trending"),
    path('new/', views.news, name="news"),

]
