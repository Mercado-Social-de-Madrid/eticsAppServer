from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view

from currency.models import Entity
from rest_api.serializers import UserSerializer, EntitySerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class EntitiesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly)