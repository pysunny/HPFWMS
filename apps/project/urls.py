from django.contrib import admin
from django.urls import path
from project.views import ProjectListView, ProjectAddView, ProjectDataView, ProjectDeleteView, FavoritesActiveview, PublicActiveView, PublicListView, FavoritesListView

app_name = 'project'
urlpatterns = [
    path('list', ProjectListView.as_view(), name='list'),# 项目列表
    path('add', ProjectAddView.as_view(), name='add'),# 新建项目
    path('data', ProjectDataView.as_view(), name='data'),# 数据接口
    path('delete', ProjectDeleteView.as_view(), name='delete'),# 删除项目 
    path('favoritesactive', FavoritesActiveview.as_view(), name='favoritesactive'),# 收藏激活 
    path('publicactive', PublicActiveView.as_view(), name='publicactive'),# 发布激活 

    path('publiclist', PublicListView.as_view(), name='publiclist'),# 公共项目
    path('favoriteslist', FavoritesListView.as_view(), name='favoriteslist'),# 收藏项目
    
]
