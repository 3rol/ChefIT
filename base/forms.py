from django.forms import ModelForm
from .models import Recipe, Recipe_Type
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
