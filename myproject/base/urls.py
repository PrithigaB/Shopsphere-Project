from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('addtocart/<int:pk>/', addtocart, name='addtocart'),
    path('cart/',cart,name='cart'),
    path('increase/<int:id>/', increase_qty, name='increase'),
    path('decrease/<int:id>/', decrease_qty, name='decrease'),
    path('support/', support, name='support'),
    path('know_us/', know_us, name='know_us'),
    
    
]
