from django.urls import path, include
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.doctorDashboard, name="doctor"),
    path('profile/', views.dprofile, name='dprofile'),
 
]