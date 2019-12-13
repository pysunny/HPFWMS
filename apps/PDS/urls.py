from django.contrib import admin
from django.urls import path
from PDS.views import PanelsetsDataView, PanelsetsListView, PanelsetsAddView, PanelsAddView, PanelsetsAddSetp2View, PanelsetsDeleteView, PanelsDeleteView, PrintPdsView, Step3View

app_name = 'PDS'
urlpatterns = [
    path('panelsetslist', PanelsetsListView.as_view(), name='panelsetslist'),# 屏风组列表
    path('panelsetsdata', PanelsetsDataView.as_view(), name='panelsetsdata'),# 数据接口
    path('panelsetsadd', PanelsetsAddView.as_view(), name='panelsetsadd'),# 新建组
    path('panelsetsdelete', PanelsetsDeleteView.as_view(), name='panelsetsdelete'),# 删除组
    path('panelsetsaddsetp2', PanelsetsAddSetp2View.as_view(), name='panelsetsaddsetp2'),# 新建组
    path('panelsadd', PanelsAddView.as_view(), name='panelsadd'),# 新建屏风
    path('panelsdelete', PanelsDeleteView.as_view(), name='panelsdelete'),# 删除屏风
    path('step3', Step3View.as_view(), name='step3'),# 补充资料
    path('pdsprint', PrintPdsView.as_view(), name='pdsprint'),# 删除屏风
]
