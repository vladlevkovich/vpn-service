from django.db import models
from django.db.models import Count
from src.user_profile.models import Profile
from src.oauth.models import CustomUser
import uuid


class Site(models.Model):
    """Інформація про сайт"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=155)
    url = models.URLField()

    def __str__(self):
        return f'{self.url}'


class SiteVist(models.Model):
    """Фіксування відвідування сайта користувачем"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    site = models.ForeignKey(Site, blank=True, null=True, on_delete=models.CASCADE)
    visit_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.site} visited at {self.visit_time}'


class TrafficStatic(models.Model):
    """Щоденна статистика трафіка для сайта"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, blank=True, null=True, on_delete=models.CASCADE)
    path = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    incoming_traffic = models.PositiveBigIntegerField()     # вхідний трафік
    outgoing_traffic = models.PositiveBigIntegerField()     # вихідний трафік

    def __str__(self):
        return f'{self.site} on {self.date}: {self.incoming_traffic} in {self.outgoing_traffic} out'

    def page_visit(self):
        return self.sitevisit_set.values('path').annotate(Count('path'))


# class UserStatistics(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE)
#     page_visit = models.JSONField(default=dict)
#     data_page = models.JSONField(default=dict)
#
#     def __str__(self):
#         return f'{self.user} visit {self.page_visit}'
