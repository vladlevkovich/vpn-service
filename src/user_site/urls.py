from django.urls import path
from .views import *

urlpatterns = [
    path('sites/', SitesList.as_view()),
    path('proxy/<uuid:site_id>/', ProxySite.as_view())
]
