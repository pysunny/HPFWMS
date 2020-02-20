from django.contrib import admin
from django.urls import path
from PDS.views import  setEditView, panelSelView, workspaceView, setDataView, editPageView, pdsPreviewView, EditPdsVersionView

app_name = 'PDS'
urlpatterns = [
    path('pdspreview', pdsPreviewView.as_view(), name='pdspreview'),# 打印预览
    path('setedit/<set_index>', setEditView.as_view(), name='setedit'),# 编辑，新建屏风细节
    path('panel_sel/<set_index>', panelSelView.as_view(), name='panel_sel'),# 屏风选择
    path('workspace/<set_index>', workspaceView.as_view(), name='workspace'),# 工作区
    path('editpage', editPageView.as_view(), name='editpage'),# 编辑页面

    path('setdata', setDataView.as_view(), name='setdata'),# 组数据

    path('editpdsversion/<project_id>/<pdsversion_id>', EditPdsVersionView.as_view(), name='editpdsversion'),#编辑版本
]
