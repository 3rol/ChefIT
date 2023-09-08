from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import viewsets
from base.models import Recipe
from .serializers import RecipeSerializer
from base.api.serializers import RegisterSerializer
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/recipes',
        'GET /api/recipes/:id'
    ]
    return Response(routes)


@api_view(['POST'])
def getRoutes(request):
    routes = [

        'POST /api/recipes',

    ]
    return Response(routes)


# @api_view(['GET'])
# def getRecipes(request):
#     recipes = Recipe.objects.all()
#     serializer = RecipeSerializer(recipes, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def getRecipe(request, pk):
#     recipe = Recipe.objects.get(id=pk)
#     serializer = RecipeSerializer(recipe, many=False)
#     return Response(serializer.data)


# Use this decorator to disable CSRF protection for testing purposes.
@csrf_exempt
@api_view(['POST'])
def create_recipe(request):
    if request.method == 'POST':
        # Parse JSON data from the request
        data = JSONParser().parse(request)
        serializer = RecipeSerializer(data=data)

        if serializer.is_valid():
            # Save the new recipe to the database
            serializer.save()
            return JsonResponse(serializer.data, status=201)  # Created
        return JsonResponse(serializer.errors, status=400)  # Bad Request

    return JsonResponse({'message': 'Invalid request method'}, status=405)


# class UserViewSet(viewsets.ModelViewSet):
#     lookup_field = 'name'
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)


class ApiRecipeListView(ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'description']
    filterset_fields = ['name']
