from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Recipe, Recipe_Type
from .forms import RecipeForm


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    recipes = Recipe.objects.filter(recipe_type__name__icontains=q)
    recipe_types = Recipe_Type.objects.all()
    context = {'recipes': recipes, 'recipe_types': recipe_types}
    return render(request, 'base/home.html', context)


def createRecipe(request):
    form = RecipeForm()
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/recipe_creation.html', context)


def updateRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    form = RecipeForm(instance=recipe)

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/recipe_creation.html', context)


def deleteRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    if request.method == 'POST':
        recipe.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': recipe})
