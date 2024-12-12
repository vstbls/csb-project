from django.urls import path

from .views import *

urlpatterns = [
    path('', loginView, name='login'),
    path('login/', processLoginView, name='processLogin'),
    path('chat/<str:username>/', chatView, name='chat')
]