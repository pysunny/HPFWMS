from django.contrib import admin
from django.urls import path
from index.views import IndexView, WelcomeView

app_name = 'index'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),# 主框架
    path('welcome', WelcomeView.as_view(), name='welcome'),# 欢迎页
]
