from django.contrib import admin
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('signup/', views.signup_view, name = "Signup"),
    path('login/', views.loginUser, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
]