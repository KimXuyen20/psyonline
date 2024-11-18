from django.urls import path, include
from . import views


urlpatterns = [

    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerDoctor/', views.registerDoctor, name='registerDoctor'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]