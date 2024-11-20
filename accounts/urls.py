from django.urls import path, include
from . import views


urlpatterns = [

    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerDoctor/', views.registerDoctor, name='registerDoctor'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('custDashboard/', views.custDashboard, name='custDashboard'),
    path('doctorDashboard/', views.doctorDashboard, name='doctorDashboard'),
    path('myAccount/', views.myAccount, name='myAccount'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('doctor/', include('doctor.urls')),
]