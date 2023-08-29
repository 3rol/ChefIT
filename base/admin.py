from django.contrib import admin

# Register your models here.

from .models import Recipe, Recipe_Type, Comment

admin.site.register(Recipe)
admin.site.register(Recipe_Type)
admin.site.register(Comment)
