from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path('login/', loginPage, name='login'),
    path('register/', registerPage, name='register'),
    path('forgotPass/', forgotPassPage, name='forgotPass'),
    path('logout/', logOut, name='logout')
]
