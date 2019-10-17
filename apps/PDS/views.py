from django.shortcuts import render
from django.views.generic import View
from project.models import Projects
from PDS.models import Panelsets
from django.http import JsonResponse, HttpResponse
import json

# Create your views here.

# /PDS/panelsetslist 组列表
class PanelsetsListView(View):
    """ 查看组列表视图类 """
    def get(self, request):
        """ 显示页面 """
        # 接收数据
        id = request.GET.get('id')
        project = Projects.objects.get(project_id=id)
        project.location = project.get_projectlocation_display()
        return render(request, 'PDS/panelsetslist.html', {'project':project})

# /PDS/panelsetsdata 屏风组数据
class PanelsetsDataView(View):
    """ 组数据 """
    def get(self, request):
        # 获取全部用户的数据
        ret = Panelsets.objects.all()
        # 转化数据
        panelset = ret.values()
        # 获取数据数量
        count = ret.count()
        data = list(panelset)
        # 组织上下文
        context = {
            "code": 0,
            "msg": "",
            "count": count,
            "data": data
        }
        # 使用ComplexEncoder格式化jason
        return HttpResponse(json.dumps(context))

# /PDS/panelsetsadd 新建屏风组
class PanelsetsAddView(View):
    """ 新建组 """
    def get(self, request):
        """ 显示页面 """
        return render(request, 'PDS/panelsetsadd.html')