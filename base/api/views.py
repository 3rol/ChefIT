from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import viewsets
from base.models import Recipe
from .serializers import RecipeSerializer
from base.api.serializers import UserSerializer
from rest_framework import permissions


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/recipes',
        'GET /api/recipes/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def getRecipes(request):
    recipes = Recipe.objects.all()
    serializer = RecipeSerializer(recipes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    serializer = RecipeSerializer(recipe, many=False)
    return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
