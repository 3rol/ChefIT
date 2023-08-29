from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.home, name="home"),

    path('create-recipe/', views.createRecipe, name="create-recipe"),
    path('update-recipe/<str:pk>/', views.updateRecipe, name="update-recipe"),
    path('delete-recipe/<str:pk>/', views.deleteRecipe, name="delete-recipe"),
]
