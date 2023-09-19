from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from base.models import *
from rest_framework import serializers, validators

from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RecipeTypeSerializer(ModelSerializer):
    class Meta:
        model = Recipe_Type
        fields = '__all__'


class RecipeReadSerializer(ModelSerializer):
    user = UserSerializer()
    recipe_type = RecipeTypeSerializer()

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeWriteSerializer(ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    recipe_type = serializers.PrimaryKeyRelatedField(
        queryset=Recipe_Type.objects.all())

    class Meta:
        model = Recipe
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    recipe = RecipeReadSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), "A user with this Email already exists"

                    )
                ]
            }
        }

    def create(self, validated_data):
        user = User(
            email=validated_data.get('email'),
            username=validated_data.get('username'),

        )
        user.set_password(validated_data.get('password'))
        user.save()

        return user
