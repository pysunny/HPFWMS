from django.shortcuts import render
from django.views.generic import View
from standard.models import PanelModels
from django.http import JsonResponse, HttpResponse
from utils.ComplexEncoder import ComplexEncoder
import json

# Create your views here.
#/standard/list 屏风型号
class StandardListView(View):
    def get(self, request):
        """ 显示页面 """
        return render(request, 'standard/list.html')
    
#/standard/data 数据接口
class StandardDataView(View):
    def get(self, request):
        # 获取全部用户的数据
        ret = PanelModels.objects.all()
        # 转化数据
        panelmodels = ret.values()
        # 获取数据数量
        count = ret.count()
        data = list(panelmodels)
        # 组织上下文
        context = {
            "code":0,
            "msg":"",
            "count":count,
            "data":data
            }
        # 使用ComplexEncoder格式化jason
        return HttpResponse(json.dumps(context, cls=ComplexEncoder))

#/standard/add 新建型号
class StandardAddView(View):
    def get(self, request):
        """ 显示页面 """
        return render(request, 'standard/add.html')
    
    def post(self, request):
        """ 添加新项目 """
        # 接收数据
        name = request.POST.get('name')
        series = request.POST.get('series')
        top_clearance = request.POST.get('top_clearance')
        top_seal = request.POST.get('top_seal')
        top_mechanism = request.POST.get('top_mechanism')
        basic_material = request.POST.get('basic_material')
        steel_plate = request.POST.get('steel_plate')
        rockwool = request.POST.get('rockwool')
        bottom_clearance = request.POST.get('top_clearance')
        bottom_seal = request.POST.get('top_seal')
        bottom_mechanism = request.POST.get('top_mechanism')
        desc = request.POST.get('desc')
        # 校验数据
        if not all([name, series, top_clearance, basic_material, steel_plate, bottom_clearance, desc]):
            return JsonResponse({'res':0, 'errmsg':'数据不完整'})
        # 检验已有相同名字
        try:
            panelmodel = PanelModels.objects.get(name=name)
        except PanelModels.DoesNotExist:
            # 用户名不存在
            panelmodel = None
        if panelmodel:
            return JsonResponse({'res':1, 'errmsg':'型号已经存在'})
        # 业务处理
        panelmodel = PanelModels.objects.create(
            name=name, 
            series=series, 
            top_clearance=top_clearance, 
            top_seal=top_seal, 
            top_mechanism=top_mechanism, 
            basic_material=basic_material, 
            steel_plate=steel_plate, 
            rockwool=rockwool, 
            bottom_clearance=bottom_clearance, 
            bottom_seal=bottom_seal, 
            bottom_mechanism=bottom_mechanism, 
            desc=desc
            )
        # 返回应答
        return JsonResponse({'res':2})