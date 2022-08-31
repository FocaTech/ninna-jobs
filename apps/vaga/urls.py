from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('novo', views.novo, name='novo')
]