from django.urls import path
from apps.activity import views

urlpatterns = [
    # path('', views.index),
    # path('addArticle/', views.addArticle),
    path('atvtlist/', views.atvtlist),
    path('addActivity/', views.addActivity),
    path('editActivity/', views.editActivity),
    path('delActivity/', views.delActivity),


    path('ActivityManage/', views.ActivityManage),

    path('applyActivity/', views.applyActivity),
    path('applyList/', views.applyList),
    path('myActivity/',views.myActivity),
    path('atvtDetail/', views.atvtDetail),
]