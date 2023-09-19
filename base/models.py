from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Recipe_Type(models.Model):
    name = models.TextField(max_length=200)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, default='', null=True)
    name = models.CharField(max_length=200)
    recipe_type = models.ForeignKey(
        Recipe_Type, on_delete=models.SET_NULL,  null=True)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    recipe_image = models.ImageField(
        null=True, blank=True, upload_to="images/")
    image_url = models.CharField(
        max_length=500, default='/media/images/creamy-tomato-soup-buttery-croutons-hero-02-49b419d00f854db78838a79c8df9a23f.jpg', blank=True)
    is_hardcoded = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body
