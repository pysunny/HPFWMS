from django.contrib import admin
from django.urls import path

app_name = 'PDS'
urlpatterns = [
    path('register', RegistreView.as_view(), name='register'),# 注册
]
