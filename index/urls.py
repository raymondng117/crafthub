from django.urls import path
from .views import landingpage_view

app_name = 'index'

urlpatterns = [
    # path is a function used to grab the html template for specific url request
    path('', landingpage_view, name='landingpage'),
]
