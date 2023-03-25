from django.urls import path
from apps.login import views
from django.urls import include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('captcha/', include('captcha.urls')),		#验证码
	path('confirm/', views.user_confirm),
	path('uploadimg/',views.upload_image),
	path('nav/', views.nav),

	path('search/',views.search),
	path('loadAvatar/', views.loadAvatar),

	path('my_notifications/', views.my_notifications),

	path('updataPwd/', views.updataPwd),
	path('toSend_pwdEmail/', views.toSend_pwdEmail),
	path('forget_confirm/', views.forget_confirm),
	path('toPwdPage/', views.up_pwd_page),

	path('about/', views.about),
]