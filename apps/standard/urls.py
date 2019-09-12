from django.contrib import admin
from django.urls import path
from standard.views import StandardListView, StandardDataView, StandardAddView

app_name = 'standard'
urlpatterns = [
    path('list', StandardListView.as_view(), name='list'),# 屏风型号
    path('data', StandardDataView.as_view(), name='data'),# 数据接口
    path('add', StandardAddView.as_view(), name='add'),# 添加型号
]
