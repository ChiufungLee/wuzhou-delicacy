from django.urls import path
from apps.article import views

urlpatterns = [
    # path('', views.index),
    path('addArticle/', views.addArticle),
    path('atc_detail/', views.article_detail),
    path('listArticle/', views.listArticle),
    path('settop/', views.settop),
    path('editArticle/', views.editArticle),
    path('delArticle/', views.delArticle),
    path('searchArticle/', views.searchArticle),
    # path('articleList/', views.articleList),
    path('foodNews/', views.foodNews),

    path('addTravels/', views.addTravels),
    path('updateTravel/', views.updateTravel),
     path('delTravel/', views.delTravel),
    
    path('cateArticle/', views.cateArticle),
    path('addArticleCate/', views.addArticleCate),
    path('delAtcCategory/', views.delAtcCategory),
    path('updateAtcCategory/', views.updateAtcCategory),

    path('atcListZixun/', views.article_zixun),
    path('atcListRizhi/', views.article_rizhi),

    path('myTravels/', views.myTravels),

    path('uploadimg/', views.uploadimg),
]