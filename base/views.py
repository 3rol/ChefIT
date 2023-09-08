from django.shortcuts import render, redirect
from django.http import HttpResponse
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
from rest_framework.permissions import IsAuthenticated

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


@login_required(login_url='login')
def createRecipe(request):
    form = RecipeForm()
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/recipe_creation.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
def deleteRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    if request.user != recipe.user:
        return HttpResponse('You are not the chef!')

    if request.method == 'POST':
        recipe.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': recipe})


@login_required(login_url='login')
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.user != comment.user:
        return HttpResponse('You are not allowed to do this!')

    if request.method == 'POST':
        comment.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': comment})


@api_view(['POST'])
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
        'token': token


    })


@api_view(['GET'])
def get_user_data(request):
    user = request.user

    if user.is_authenticated:
        return Response({
            'user_info': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
        })

    return Response({'error': 'Not authenticated'}, status=400)


@api_view(['POST'])
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
        'token': token
    })


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
def getCommentsForRecipe(request, pk):
    comments = Comment.objects.filter(recipe=pk)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postComment(request):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        # Assign the logged-in user to the comment
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
