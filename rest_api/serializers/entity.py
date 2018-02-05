from django.contrib.auth.models import User
from rest_framework import serializers

from currency.models import Entity


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ('url', 'name', 'email', 'description')