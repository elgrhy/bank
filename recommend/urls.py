from django.urls import path
from . import views

#url configration
urlpatterns = [
    path('index/', views.home, name='home'),
]