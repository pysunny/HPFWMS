from django.contrib import admin
from django.urls import path
from standard.views import ModelsListView, ModelsDataView, ModelsAddView, PicsListView, PicsPartsListView, PicsPartsDataView, PicsPartsAddView, PicsPartsEditView, PicsDataView, PicsAddView, PicsEditView, ModelsEditView

app_name = 'standard'
urlpatterns = [
    path('modelslist', ModelsListView.as_view(), name='modelslist'),# 屏风型号
    path('modelsdata', ModelsDataView.as_view(), name='modelsdata'),# 数据接口
    path('modelsadd', ModelsAddView.as_view(), name='modelsadd'),# 添加型号
    path('modelsedir', ModelsEditView.as_view(), name='modelsedit'),# 编辑型号

    path('picspartslist', PicsPartsListView.as_view(), name='picspartslist'),# 图元组件
    path('picspartsdata', PicsPartsDataView.as_view(), name='picspartsdata'),# 组件数据接口
    path('picspartsadd', PicsPartsAddView.as_view(), name='picspartsadd'),# 添加组件
    path('picspartsedit', PicsPartsEditView.as_view(), name='picspartsedit'),# 编辑组件

    path('picslist', PicsListView.as_view(), name='picslist'),# 屏风图元
    path('picsdata', PicsDataView.as_view(), name='picsdata'),# 图元数据接口
    path('picsadd', PicsAddView.as_view(), name='picsadd'),# 添加组件
    path('picsedit', PicsEditView.as_view(), name='picsedit'),# 编辑组件
]
