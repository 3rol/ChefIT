from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from base.forms import UserCreationForm
from .models import Recipe, Recipe_Type, Comment
from .forms import RecipeForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from rest_framework.decorators import api_view, permission_classes
from base.api.serializers import *
from rest_framework.permissions import AllowAny
from rest_framework import status

# def loginPage(request):
#     page = 'login'
#     if request.user.is_authenticated:
#         return redirect('home')

#     if request.method == 'POST':
#         username = request.POST.get('username').lower()
#         password = request.POST.get('password')

#         try:
#             user = User.objects.get(username=username)
#         except:
#             messages.error(request, 'User does not exist')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'Username OR Password does not exist')

#     context = {'page': page}
#     return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


@csrf_exempt
def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('home')
        else:
            messages.error(request, 'Error occurred during registration!')
    return render(request, 'base/login_register.html', {'form': form})


# def home(request):
#     q = request.GET.get('q') if request.GET.get('q') != None else ''
#     recipes = Recipe.objects.filter(recipe_type__name__icontains=q)
#     recipe_types = Recipe_Type.objects.all()
#     context = {'recipes': recipes, 'recipe_types': recipe_types}
#     return render(request, 'base/home.html', context)


def recipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    recipe_comment = recipe.comment_set.all().order_by('-created')

    if request.method == 'POST':
        comment = Comment.objects.create(
            user=request.user,
            recipe=recipe,
            body=request.POST.get('body')
        )
        return redirect('recipe', pk=recipe.id)

    context = {'recipe': recipe, 'recipe_comment': recipe_comment}
    return render(request, 'base/recipe.html', context)


@api_view(['POST'])
def createRecipe(request):

    serializer = RecipeSerializer()

    if serializer.is_valid():
        instance = serializer.save()
        instance.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@permission_classes([AllowAny])
def updateRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    form = RecipeForm(instance=recipe)

    if request.user != recipe.user:
        return HttpResponse('You are not the chef!')

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/recipe_creation.html', context)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def deleteRecipe(request, pk):
    try:
        recipe = Recipe.objects.get(id=pk)
    except Recipe.DoesNotExist:
        return Response({'error': 'Recipe not found'}, status=status.HTTP_404_NOT_FOUND)

    recipe.delete()
    return Response({'status': 'Recipe deleted'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def deleteComment(request, pk):
    try:
        comment = Comment.objects.get(id=pk)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    comment.delete()
    return Response({'status': 'Comment deleted'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    page = 'login'
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']

    _, token = AuthToken.objects.create(user)

    return Response({
        'user_info': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        },
        'Bearer': token


    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_data(request):
    user = request.user
    if user and user.is_authenticated:
        return Response({
            'user_info': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        })


@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()
    _, token = AuthToken.objects.create(user)

    return Response({
        'user_info': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        },
        'Bearer': token
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def getRecipes(request):
    name = request.GET.get('name')
    recipes = Recipe.objects.all()

    if name:
        recipes = recipes.filter(name__icontains=name)

    serializer = RecipeSerializer(
        recipes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def getRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    serializer = RecipeSerializer(
        recipe, many=False)
    return Response(serializer.data)


def home(request):
    name = request.GET.get('name')
    recipes = Recipe.objects.all()
    if name:
        recipes = recipes.filter(name__icontains=name)
    context = {
        'form': RecipeForm(),
        'recipe': recipes
    }
    return render(request, 'home.html', context)


@api_view(['GET'])
@permission_classes([AllowAny])
def getCommentsForRecipe(request, pk):
    comments = Comment.objects.filter(recipe=pk)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def postComment(request, pk):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, recipe_id=pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def getRecipeTypes(request):
    recipe_types = Recipe_Type.objects.all()
    serializer = RecipeTypeSerializer(recipe_types, many=True)
    return Response(serializer.data)
