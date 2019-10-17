from django.contrib import admin
from django.urls import path
from user.views import LoginView, RegisterView, EmailActiveView, ActiveView, MemberListView, LogoutView, UserDataView, PermissionListView, PermissionDataView
app_name = 'user'
urlpatterns = [
    path('login', LoginView.as_view(), name='login'),# 登录
    path('register', RegisterView.as_view(), name='register'),# 注册
    path('emailactive/<token>', EmailActiveView.as_view(), name='emailactive'),# 电邮激活
    path('active/<user_id>', ActiveView.as_view(), name='active'),# 用户激活
    path('memberlist', MemberListView.as_view(), name='memberlist'),# 用户管理
    path('permissionList', PermissionListView.as_view(), name='permissionList'),# 用户权限表
    path('logout', LogoutView.as_view(), name='logout'),# 登出
    path('data', UserDataView.as_view(), name='data'),# 用户数据接口
    path('permissiondata', PermissionDataView.as_view(), name='permissiondata'),# 权限表数据接口
]
