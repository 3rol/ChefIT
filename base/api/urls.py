from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('recipes/', views.getRecipes),
    path('recipes/<str:pk>', views.getRecipe)
]
