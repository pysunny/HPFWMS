from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from celery_tasks.tasks import send_email_active_email, send_register_email
from django.conf import settings
from user.models import User, UserPermission
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from utils.ComplexEncoder import ComplexEncoder
from utils.mixin import LoginRequiredMixin
import re
import json

# /user/login 用户登录页面


class LoginView(View):
    def get(self, request):
        """ 显示页面 """
        # 判断是否记得用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        return render(request, 'user/login.html', {'username': username, 'checked': checked})

    def post(self, request):
        """ 登陆校验 """
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        # 校验数据
        if not all([username, password]):
            return render(request, 'user/login.html', {'errmsg': '数据不完整'})
        # 业务处理:登录校验
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户名密码正确
            if user.is_active:
                # 用户已激活
                # 记录用户的登录状态
                login(request, user)
                # 获取登陆之后要跳转的地址，默认返回首页
                next_url = request.GET.get('next', reverse('index:index'))
                # 跳转next_url
                response = redirect(next_url)
                # 判断是否需要记得用户名
                remember = request.POST.get('remember')
                if remember == 'on':
                    # 记得用户名
                    response.set_cookie(
                        'username', username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')
                return response

            else:
                # 用户未激活
                return render(request, 'user/login.html', {'errmsg': '账号未激活'})

        else:
            # 用户名或密码错误
            return render(request, 'user/login.html', {'errmsg': '用户名或者密码错误'})

# /user/register 用户注册页面


class RegisterView(View):
    def get(self, request):
        """ 显示页面 """
        return render(request, 'user/register.html')

    def post(self, request):
        """ 进行注册处理 """
        """ 接收数据 """
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        repassword = request.POST.get('repwd')
        email = request.POST.get('email')
        location = request.POST.get('location')
        allow = request.POST.get('allow')

        """ 检验数据 """
        # 校验是否同意协议
        if allow != 'on':
            return JsonResponse({'res': 1, 'errmsg': '请同意协议'})

        # 进行数据校验
        if not all([username, password, email, location]):
            return JsonResponse({'res': 2, 'errmsg': '数据不完整'})

        # 校验密码组成
        if not re.match(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$', password):
            return JsonResponse({'res': 3, 'errmsg': '密码不符合要求'})

        # 检验密码是否一样
        if password != repassword:
            return JsonResponse({'res': 4, 'errmsg': '两次密码不一样'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return JsonResponse({'res': 5, 'errmsg': '邮箱格式不正确'})

        # 检验是否使用hufcor.com的电邮
        # 测试期间关闭
        # if not email.endswith('hufcor.com'):
            # return JsonResponse({'res':6, 'errmsg':'请使用公司电邮注册'})

        # 检验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            return JsonResponse({'res': 7, 'errmsg': '用户名已经存在'})

        # 检验邮箱是否重复
        try:
            email_add = User.objects.get(email=email)
        except User.DoesNotExist:
            # 电邮不存在
            email_add = None
        if email_add:
            return JsonResponse({'res': 8, 'errmsg': '此邮箱已经存在'})

        """ 业务处理 """
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.location = location
        user.save()

        """ 发送激活邮件 """
        # 加密用户身份信息 生成激活cookie
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'comfirm': user.id}
        token = serializer.dumps(info)
        token = token.decode()

        # 发送激活邮件
        send_email_active_email.delay(email, username, token)

        return JsonResponse({'res': 9})

# /user/email_active 电邮激活


class EmailActiveView(View):
    """ 用户电邮激活 """

    def get(self, request, token):
        """ 进行用户电邮激活 """
        # 进行解密
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取用户id
            user_id = info['comfirm']
            # 激活用户
            user = User.objects.get(id=user_id)
            user.email_activate = 1
            # 获取用户资料 名字及电邮
            username = user.username
            email = user.email
            user.save()

            # 向管理员发送用户激活电邮
            send_register_email.delay(email, username, user_id)

            # 返回应答
            return HttpResponse('<h1>用户激活成功，还需要管理员激活。</h1><a href="http://120.197.59.97:57893/user/login">点击登录</a>', content_type='text/html;charset=utf-8')
        except SignatureExpired as e:
            return HttpResponse('激活邮件已经过期')

# /user/active用户激活


class ActiveView(LoginRequiredMixin, View):
    """ 用户激活 """

    def get(self, request, user_id):
        """ 进行用户激活 """
        # 获取用户id
        user = request.user
        if user.is_superuser:
            user_id = user_id
            # 激活用户
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            # 跳转到登陆页面
            return redirect(reverse('user:login'))
        else:
            return HttpResponse('你没有超级管理员权限')


class MemberListView(View):
    """ 用户管理 """

    def get(self, request):
        return render(request, 'user/memberlist.html')

# /user/logout  登出


class LogoutView(View):
    def get(self, request):
        """ 退出登录 """
        # 清除用户的session信息
        logout(request)
        # 跳转到登陆页
        return redirect(reverse('user:login'))

# /user/data layui数据接口


class UserDataView(View):
    def get(self, request):
        # 获取全部用户的数据
        ret = User.objects.all()
        # 转化数据
        users = ret.values()
        # 获取数据数量
        count = ret.count()
        data = list(users)
        # 组织上下文
        context = {
            "code": 0,
            "msg": "",
            "count": count,
            "data": data
        }
        # 使用ComplexEncoder格式化jason
        return HttpResponse(json.dumps(context, cls=ComplexEncoder))

# /user/permissionlist 用户权限表


class PermissionListView(View):
    """ 用户权限表 """

    def get(self, request):
        return render(request, 'user/permissionlist.html')

# /user/permissiodata 用户权限表数据接口


class PermissionDataView(View):
    def get(self, request):
        # 获取全部用户的数据
        ret = UserPermission.objects.all()
        # 转化数据
        permissions = ret.values()
        # 获取数据数量
        count = ret.count()
        data = list(permissions)
        # 组织上下文
        context = {
            "code": 0,
            "msg": "",
            "count": count,
            "data": data
        }
        # 使用ComplexEncoder格式化jason
        return HttpResponse(json.dumps(context))
