from django.shortcuts import render
from django.views.generic import View
from utils.mixin import LoginRequiredMixin
from django_redis import get_redis_connection
from project.models import Projects

# Create your views here.


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'index/index.html')


class WelcomeView(LoginRequiredMixin, View):
    def get(self, request):
        # 获取用户的个人信息
        user = request.user
        # 获取用户的浏览记录
        conn = get_redis_connection('default')
        history_key = 'history_%d'%user.id
        # 获取浏览记录
        project_ids = conn.lrange(history_key, 0 , 9)
        project_li = []
        # 添加浏览记录
        for project_id in project_ids:
            # 这个修复浏览记录BUG，用于修复浏览后删除屏风的情况
            try:
                project = Projects.objects.get(project_id=str(project_id, "utf-8"), is_delete=False)
            except :
                project = None
                continue
            if project:
                project_li.append(project)
        
        # 组织上下文
        context = {
            'project_li':project_li
        }

        return render(request, 'index/welcome.html', context)
