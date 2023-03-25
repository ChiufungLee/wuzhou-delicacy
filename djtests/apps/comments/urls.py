from django.urls import path
from apps.comments import views

urlpatterns = [
	path('update_comment/',views.update_comment),
    
]