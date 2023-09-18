from django.urls import path
from . import views
from knox import views as knox_views
from base.api.views import *

urlpatterns = [
    path('login/', views.login_api),
    path('user/', views.get_user_data),
    # path('login/', views.loginPage, name="login"),
    path('logout/', knox_views.LogoutView.as_view()),
    path('logoutall/', knox_views.LogoutAllView.as_view()),
    path('register/', views.register_api, name="register"),
    path('', views.home, name="home"),
    path('recipes/getrecipe/', views.getRecipes),
    path('recipes/getrecipe/<str:pk>', views.getRecipe),
    path('recipes/addrecipe/', views.createRecipe, name='create_recipe'),
    path('recipes/getcomments/<int:pk>/',
         views.getCommentsForRecipe, name='get_comments_for_recipe'),
    path('recipes/postcomment/<str:pk>/',
         views.postComment, name='post_comment'),
    # path('recipe/<str:pk>/', views.recipe, name="recipe"),
    # path('create-recipe/', views.createRecipe, name="create-recipe"),
    path('update-recipe/<str:pk>/', views.updateRecipe, name="update-recipe"),
    path('delete-recipe/<str:pk>/', views.deleteRecipe, name="delete-recipe"),
    path('delete-comment/<str:pk>/', views.deleteComment, name="delete-comment"),

]
