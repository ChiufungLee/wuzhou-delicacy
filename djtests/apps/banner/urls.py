from django.urls import path
from apps.banner import views

urlpatterns = [
    # path('', views.index),
    path('upload_handle/', views.upload_handle),
    path('listCarousel/', views.listCarousel),
    path('uploadCarousel/', views.uploadCarousel),
    path('editBanner/', views.editBanner),
    path('delBanner/', views.delBanner)
]