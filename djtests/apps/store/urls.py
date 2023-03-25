from django.urls import path
from apps.store import views

urlpatterns = [
    path('', views.index),
    path('adStoreList/', views.adStoreList),
    path('addStore/', views.addStore),
    path('delStore/', views.delStore),
    path('updateStore/', views.updateStore),
    path('storeDetail/', views.storeDetail),

    path('foodStreet/', views.foodStreet),
    # path('listStores/', views.listStores),
]