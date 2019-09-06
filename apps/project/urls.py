from django.contrib import admin
from django.urls import path
from project.views import ListView, AddView, ProjectDataView

app_name = 'project'
urlpatterns = [
    path('list', ListView.as_view(), name='list'),# 项目列表
    path('add', AddView.as_view(), name='add'),# 新建项目
    path('data', ProjectDataView.as_view(), name='data'),# 新建项目
]
