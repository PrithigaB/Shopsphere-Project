from django.urls import path

from .views import * 

urlpatterns = [
    path('login_/',login_,name='login_'),
    path('register/',register,name='register'),
    path('profile/',profile,name='profile'),
    path('logout_/',logout_,name='logout_'),

    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/', reset_password, name='reset_password'),
    path('update-password/', update_password, name='update_password'),

    path('update_profile/', update_profile, name='update_profile'),

]