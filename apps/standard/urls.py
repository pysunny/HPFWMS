from django.contrib import admin
from django.urls import path
from standard.views import ModelsListView, ModelsDataView, ModelsView, PicsListView, PicsPartsListView, PicsPartsDataView, PicsPartsView, PicsDataView, PicsView, PicsPartsActiceView, PicsActiceView, ModelsActiceView
app_name = 'standard'
urlpatterns = [
    path('modelslist', ModelsListView.as_view(), name='modelslist'),# 屏风型号
    path('modelsdata', ModelsDataView.as_view(), name='modelsdata'),# 数据接口
    path('models', ModelsView.as_view(), name='models'),# 添加型号
    path('modelsactice', ModelsActiceView.as_view(), name='modelsactice'),# 激活型号

    path('picspartslist', PicsPartsListView.as_view(), name='picspartslist'),# 图元组件
    path('picspartsdata', PicsPartsDataView.as_view(), name='picspartsdata'),# 组件数据接口
    path('picsparts', PicsPartsView.as_view(), name='picsparts'),# 添加组件
    path('picspartsactice', PicsPartsActiceView.as_view(), name='picspartsactice'),# 激活图元

    path('picslist', PicsListView.as_view(), name='picslist'),# 屏风图元
    path('picsdata', PicsDataView.as_view(), name='picsdata'),# 图元数据接口
    path('pics', PicsView.as_view(), name='pics'),# 添加组件
    path('picsactice', PicsActiceView.as_view(), name='picsactice'),# 激活组件
]
