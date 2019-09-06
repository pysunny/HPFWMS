from django.contrib import admin
from django.urls import path
from user.views import LoginView, RegisterView, EmailActiveView, ActiveView, MemberListView, LogoutView, UserDataView
app_name = 'user'
urlpatterns = [
    path('login', LoginView.as_view(), name='login'),# 登录
    path('register', RegisterView.as_view(), name='register'),# 注册
    path('emailactive/<token>', EmailActiveView.as_view(), name='emailactive'),# 电邮激活
    path('active/<user_id>', ActiveView.as_view(), name='active'),# 用户激活
    path('memberlist', MemberListView.as_view(), name='memberlist'),# 用户管理
    path('logout', LogoutView.as_view(), name='logout'),# 登出
    path('data', UserDataView.as_view(), name='data'),# layui数据接口
]
