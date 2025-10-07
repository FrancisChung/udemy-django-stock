from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about.html', views.about, name="about"),
    path('home.html', views.home, name="home"),
    path('add_stock.html', views.add_stock, name="add_stock"),
]