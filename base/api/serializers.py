from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from base.models import Recipe
from rest_framework import serializers


class RecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',]
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
