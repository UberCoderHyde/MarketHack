from django.urls import path,include
from django.contrib import admin
from . import views
urlpatterns = [
    path('signup/', views.home, name="home"),
    path('' , views.accountpage, name = "accountpage"),
    path('delete/' , views.delete, name = "delete"),
    path('delete_account/' , views.delete_account, name = "delete_account"),
    path('notAUser/' , views.notAUser, name = "notAUser"),
]
