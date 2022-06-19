
from django.contrib import admin
from django.urls import path
from . import views
from .views import RegisterAPI
from knox import views as knox_views
from .views import LoginAPI


urlpatterns = [
    path('', views.index, name='index'),
    path('login/',views.login,name='login'),
    path('welcome/',views.welcome_page,name='welcome'),
    path('data/',views.data,name='alldata'),
    path('loginform/',views.loginform,name='form'),
    path('formdata/',views.form_data,name='form'),
    path('dataform/',views.dataform,name='form'),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]
