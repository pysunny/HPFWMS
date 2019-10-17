from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls', namespace='index')), #主框架
    path('user/', include('user.urls', namespace='user')), #用户
    path('project/', include('project.urls', namespace='project')), #项目
    path('standard/', include('standard.urls', namespace='standard')), #标准
    path('PDS/', include('PDS.urls', namespace='PDS')), #开工纸
]
