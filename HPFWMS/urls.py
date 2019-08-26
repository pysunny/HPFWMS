from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls', namespace='index')), #主框架
    path('user/', include('user.urls', namespace='user')), #用户
]
