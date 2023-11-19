from django.contrib import admin
from .models import *


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name')


@admin.register(SiteVist)
class SiteVisitAdmin(admin.ModelAdmin):
    list_display = ('id', 'site')


@admin.register(TrafficStatic)
class TrafficStatic(admin.ModelAdmin):
    list_display = ('id', 'site', 'incoming_traffic', 'outgoing_traffic')

