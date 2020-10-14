from django.urls import path
from . import views
from django.conf import settings

from django.contrib.auth import logout

app_name = 'biblio'

urlpatterns = [
    path('logout/', logout , name='logout'),
]