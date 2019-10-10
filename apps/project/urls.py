from django.contrib import admin
from django.urls import path
from project.views import ProjectListView, ProjectAddView, ProjectDataView, ProjectDetailsView

app_name = 'project'
urlpatterns = [
    path('list', ProjectListView.as_view(), name='list'),# 项目列表
    path('add', ProjectAddView.as_view(), name='add'),# 新建项目
    path('data', ProjectDataView.as_view(), name='data'),# 数据接口
    path('details', ProjectDetailsView.as_view(), name='details'),# 项目详细
]
