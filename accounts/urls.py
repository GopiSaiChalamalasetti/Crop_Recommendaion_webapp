from django.urls import path
from . import views
urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('home/', views.home, name='home'),
    path('predict/',views.predict_crop,name='predict'),
    
]