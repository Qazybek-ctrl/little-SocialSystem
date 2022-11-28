from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('', homePage, name='home'),
    path('friends', friendsPage, name='friends'),
    path('<slug:profile_slug>/', profilePage, name='profile'),
    path('<slug:profile_slug>/edit/', editPage, name='edit'),
    path('<slug>/friend_action/<operation>', friend_action, name='friend_action')
]
