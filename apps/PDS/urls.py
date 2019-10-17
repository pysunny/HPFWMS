from django.contrib import admin
from django.urls import path
from PDS.views import PanelsetsDataView, PanelsetsListView, PanelsetsAddView

app_name = 'PDS'
urlpatterns = [
    path('panelsetslist', PanelsetsListView.as_view(), name='panelsetslist'),# 屏风组列表
    path('panelsetsdata', PanelsetsDataView.as_view(), name='panelsetsdata'),# 数据接口
    path('panelsetsadd', PanelsetsAddView.as_view(), name='panelsetsadd'),# 新建组
]
