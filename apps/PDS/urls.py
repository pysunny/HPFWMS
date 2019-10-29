from django.contrib import admin
from django.urls import path
from PDS.views import PanelsetsDataView, PanelsetsListView, PanelsetsAddView, PanelsAddView, PanelsDataView, PanelsetsAddSetp2View

app_name = 'PDS'
urlpatterns = [
    path('panelsetslist', PanelsetsListView.as_view(), name='panelsetslist'),# 屏风组列表
    path('panelsetsdata', PanelsetsDataView.as_view(), name='panelsetsdata'),# 数据接口
    path('panelsetsadd', PanelsetsAddView.as_view(), name='panelsetsadd'),# 新建组
    path('panelsetsaddsetp2', PanelsetsAddSetp2View.as_view(), name='panelsetsaddsetp2'),# 新建组

    path('panelsdata', PanelsDataView.as_view(), name='panelsdata'),# 数据屏风
    path('panelsadd', PanelsAddView.as_view(), name='panelsadd'),# 新建屏风
]
