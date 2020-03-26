from django.contrib import admin
from django.urls import path
from project.views import ProjectListView, ProjectAddView, ProjectDataView, ProjectDeleteView, FavoritesActiveview, PublicListView, FavoritesListView, ProjectDetailView, saveVersionView, PdsversionDataView, viewPdsView, FavoritesDataView

app_name = 'project'
urlpatterns = [
    path('list', ProjectListView.as_view(), name='list'),# 项目列表
    path('add', ProjectAddView.as_view(), name='add'),# 新建项目
    path('data', ProjectDataView.as_view(), name='data'),# 数据接口
    path('delete', ProjectDeleteView.as_view(), name='delete'),# 删除项目 

    path('favoritesdata', FavoritesDataView.as_view(), name='favoritesdata'),# 收藏数据接口
    path('favoritesactive', FavoritesActiveview.as_view(), name='favoritesactive'),# 收藏激活 

    path('publiclist', PublicListView.as_view(), name='publiclist'),# 公共项目
    path('favoriteslist', FavoritesListView.as_view(), name='favoriteslist'),# 收藏项目

    path('projectdetail/<project_id>', ProjectDetailView.as_view(), name='projectdetail'),# 项目细节
    path('saveversion', saveVersionView.as_view(), name='saveversion'),# 保存版本
    path('pdsversiondata/<project_id>', PdsversionDataView.as_view(), name='pdsversiondata'),# 版本数据

    path('viewpds/<project_id>/<pdsversion_id>', viewPdsView.as_view(), name='viewpds'),# 参看开工纸
    
]
