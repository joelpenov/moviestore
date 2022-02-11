from dataclasses import fields
from rest_framework import serializers
from core import models

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = ("name", "id")
        read_only_fields = ("id",)
    
class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Actor
        fields = ("name", "last_name", "id")
        read_only_fields = ("id",)