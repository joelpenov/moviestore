
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication 
from rest_framework.permissions import IsAuthenticated

from core.models import Actor, Tag

from movie import serializers

class MovieBaseViewSet(viewsets.GenericViewSet, 
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    default_order_field = "-name"

    def get_queryset(self):
        return self.query_set.filter(user=self.request.user).order_by(self.default_order_field)

    def perform_create(self, serializer):
        serializer.save(user= self.request.user)

class TagViewSet(MovieBaseViewSet):
    query_set = Tag.objects.all()
    serializer_class = serializers.TagSerializer

class ActorViewSet(MovieBaseViewSet):
    query_set = Actor.objects.all()
    serializer_class = serializers.ActorSerializer
    