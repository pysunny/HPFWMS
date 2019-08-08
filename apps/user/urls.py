from django.contrib import admin
from django.urls import path

app_name = 'user'
urlpatterns = [
    path('register', RegistreView.as_view(), name='register'),# 注册
]
