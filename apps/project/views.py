from django.shortcuts import render
from django.views.generic import View
from project.models import Projects
from django.http import JsonResponse, HttpResponse
from utils.ComplexEncoder import ComplexEncoder
import json

# Create your views here.
# /project/list 项目列表
class ProjectListView(View):
    def get(self, request):
        """ 显示页面 """
        return render(request, 'project/list.html')

#/project/add 新建项目
class ProjectAddView(View):
    def get(self, request):
        """ 显示页面 """
        return render(request, 'project/add.html')

    def post(self, request):
        """ 添加新项目 """
        # 接收数据
        user = request.user
        projectname = request.POST.get('projectname')
        request_time = request.POST.get('request_time')
        print(request_time)
        # 校验数据
        # 检验是否已有项目
        try:
            project = Projects.objects.get(name=projectname)
        except Projects.DoesNotExist:
            # 用户名不存在
            project = None
        if project:
            return JsonResponse({'res':1, 'errmsg':'项目已经存在'})

        # 检验时间是否比今天早
        
        # 业务处理
        project = Projects.objects.create(name=projectname, user=user, request_time=request_time)

        # 返回应答
        return JsonResponse({'res':2})

#/project/data 数据接口
class ProjectDataView(View):
    def get(self, request):
        # 获取全部用户的数据
        ret = Projects.objects.all()
        # 转化数据
        projects = ret.values()
        # 获取数据数量
        count = ret.count()
        data = list(projects)
        # 组织上下文
        context = {
            "code":0,
            "msg":"",
            "count":count,
            "data":data
            }
        # 使用ComplexEncoder格式化jason
        return HttpResponse(json.dumps(context, cls=ComplexEncoder))
    
