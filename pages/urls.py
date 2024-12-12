from django.urls import path

from .views import *

urlpatterns = [
    path('', loginView, name='login'),
    path('login/', processLoginView, name='processLogin'),
    # FIX FOR BROKEN ACCESS CONTROL: Change the following path to path('chat/', chatView, name='chat'). See views.py for details.
    path('chat/<str:username>/', chatView, name='chat'),
    path('send/', sendMessageView, name='send'),
    path('search/', searchView, name='search')
]