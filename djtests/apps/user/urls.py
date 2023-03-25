from django.urls import path
from apps.user import views

urlpatterns = [
    # path('', views.index),
    path('login/', views.login),
    path('logout/', views.logout),
    path('register/', views.register, name = "register"),
    path('admin/', views.admin),

    path('userList/', views.userList),
    path('userSearch/', views.searchUser),
    path('admin/delUser/', views.delUser),
    path('admin/updataUser/', views.adminUpdataUser),
    path('admin/adminManage/', views.adminManage),
    path('islog/', views.islog),
    path('userCenter/', views.userCenter),
    # path('add/', views.add)
    path('userInfo/', views.userInfo),
    path('updataUser/', views.updataUser),
    path('toActive/', views.toActive),
    path('userConfirm/', views.userConfirm),
    path('delConfirm/', views.delConfirm),

    path('commentsList/', views.commentsList),
    path('delComment/', views.delComment),
    
]