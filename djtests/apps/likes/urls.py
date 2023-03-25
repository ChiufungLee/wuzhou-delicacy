from django.urls import path
from apps.likes import views

urlpatterns = [
    # path('', views.index),
    # path('addArticle/', views.addArticle),
    # path('atvtlist/', views.atvtlist),
    path('uplike/', views.uplike),
    path('upcollect/', views.upcollect),
    path('myCollect/', views.myCollect),
    path('delCollect/', views.delCollect),
    
]