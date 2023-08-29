from django.forms import ModelForm
from .models import Recipe, Recipe_Type


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
