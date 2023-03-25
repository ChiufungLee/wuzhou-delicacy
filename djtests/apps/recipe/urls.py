from django.urls import path
from apps.recipe import views

urlpatterns = [
    path('listRecipe/', views.listRecipe),
    path('addRecipe/', views.addRecipe),
    path('delRecipe/', views.delRecipe),
    path('updateRecipe/', views.updateRecipe),

    path('adDelRecipe/', views.adDelRecipe),
    path('recipeDetail/', views.recipeDetail),

    path('listCategory/', views.listCategory),
    path('addCategory/', views.addCategory),
    path('delCategory/', views.delCategory),
    path('updateCategory/', views.updateCategory),
    
    path('listTaste/', views.listTaste),
    path('delTaste/', views.delTaste),
    path('addTaste/', views.addTaste),
    path('updateTaste/', views.updateTaste),

    path('testadd/', views.testadd),
    path('listIngres/', views.listIngres),

    path('rcpUcList/', views.rcpUcList),
    path('myRecipes/', views.myRecipes),
    path('myVlogs/', views.myVlogs),

    path('foodvlog/', views.foodvlog),
    path('addVlogs/', views.addVlogs),
    path('vlogDetail/', views.vlogDetail),

]