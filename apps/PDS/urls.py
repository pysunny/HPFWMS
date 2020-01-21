from django.contrib import admin
from django.urls import path
from PDS.views import PanelsetsDataView, PanelsetsListView, PanelsetsDeleteView, PanelsDeleteView, setEditView, panelSelView, workspaceView, setDataView, editPageView, pdsPreviewView, EditPdsVersionView

app_name = 'PDS'
urlpatterns = [
    path('panelsetslist/<project_id>/<pdsversion_id>', PanelsetsListView.as_view(), name='panelsetslist'),# 屏风组列表
    path('panelsetsdata/<project_id>', PanelsetsDataView.as_view(), name='panelsetsdata'),# 数据接口
    # path('panelsetsadd', PanelsetsAddView.as_view(), name='panelsetsadd'),# 新建组
    path('panelsetsdelete', PanelsetsDeleteView.as_view(), name='panelsetsdelete'),# 删除组
    # path('panelsetsaddsetp2', PanelsetsAddSetp2View.as_view(), name='panelsetsaddsetp2'),# 新建组
    # path('panelsadd', PanelsAddView.as_view(), name='panelsadd'),# 新建屏风
    path('panelsdelete', PanelsDeleteView.as_view(), name='panelsdelete'),# 删除屏风
    # path('step3', Step3View.as_view(), name='step3'),# 补充资料
    # path('pdsprint', PrintPdsView.as_view(), name='pdsprint'),# 打印屏风

    path('pdspreview', pdsPreviewView.as_view(), name='pdspreview'),# 打印预览
    path('setedit/<set_index>', setEditView.as_view(), name='setedit'),# 编辑，新建屏风细节
    path('panel_sel/<set_index>', panelSelView.as_view(), name='panel_sel'),# 屏风选择
    path('workspace/<set_index>', workspaceView.as_view(), name='workspace'),# 工作区
    path('editpage', editPageView.as_view(), name='editpage'),# 编辑页面

    path('setdata', setDataView.as_view(), name='setdata'),# 组数据

    path('editpdsversion/<project_id>/<pdsversion_id>', EditPdsVersionView.as_view(), name='editpdsversion'),#编辑版本
]
