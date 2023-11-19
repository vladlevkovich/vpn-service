from django.urls import path
from .views import *


urlpatterns = [
    path('', UserProfile.as_view()),
    path('test/', ProfilesList.as_view())
]

