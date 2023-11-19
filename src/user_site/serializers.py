from rest_framework import serializers
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import *


class CreateSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'

    def validate_url(self, value):
        validator = URLValidator()
        try:
            validator(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e.messages))
        return value

    def validate(self, attrs):
        url = attrs.get('url')
        self.validate_url(value=url)
        return attrs


class TrafficSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficStatic
        fields = '__all__'

