from django.urls import path, include
from jsonrpc.backend.django import api
from . import views

urlpatterns = [
    path('echo/', views.get_echo, name='echo'),
    path('hello/', views.get_hello, name='hello'),
    path('api/jsonrpc/', include(api.urls), name="jsonrpc"),
]