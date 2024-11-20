from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.blog, name='blog'),
    path('<slug:blog_slug>/', views.blog_detail,name="blog_detail")
   
]