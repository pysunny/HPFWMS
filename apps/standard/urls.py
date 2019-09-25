from django.contrib import admin
from django.urls import path
from standard.views import ModelsListView, ModelsDataView, ModelsAddView, PicsListView

app_name = 'standard'
urlpatterns = [
    path('modelslist', ModelsListView.as_view(), name='modelslist'),# 屏风型号
    path('picslist', PicsListView.as_view(), name='picslist'),# 屏风图元
    path('modelsdata', ModelsDataView.as_view(), name='modelsdata'),# 数据接口
    path('modelsadd', ModelsAddView.as_view(), name='modelsadd'),# 添加型号
]
