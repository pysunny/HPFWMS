from django.shortcuts import render
from django.views.generic import View
from project.models import Projects
from PDS.models import Panelsets, Panles
from standard.models import PanelModels, PicsModels
from django.http import JsonResponse, HttpResponse
from utils.ComplexEncoder import ComplexEncoder
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
        # 接收数据
        project_id = request.GET.get('project_id')
        ret = Panelsets.objects.filter(project_id = project_id)
        # 转化数据
        panelset = ret.values()
        # 获取数据数量
        count = ret.count()
        data = list(panelset)
        for pic in data:
            pic['model'] = PanelModels.objects.get(id=pic['model_id']).name
        # 组织上下文
        context = {
            "code": 0,
            "msg": "",
            "count": count,
            "data": data
        }
        # 使用ComplexEncoder格式化jason
        return HttpResponse(json.dumps(context, cls=ComplexEncoder))

# /PDS/panelsetsadd 新建屏风组
class PanelsetsAddView(View):
    """ 新建组 """
    def get(self, request):
        """ 显示页面 """
        # 接收数据
        project_id = request.GET.get('id')

        return render(request, 'PDS/panelsetsadd.html', {'project_id':project_id})

    def post(self, request):
        """ 添加新组 """
        # 接收数据
        project = Projects.objects.get(project_id=request.POST.get('project_id'))
        mark = request.POST.get('mark')
        sets = request.POST.get('sets')
        production_time = request.POST.get('production_time')
        model = PanelModels.objects.get(id=request.POST.get('model_id'))
        height = request.POST.get('height')
        width = request.POST.get('width')
        wheel = request.POST.get('wheel')
        sound_test = request.POST.get('sound_test')
        face_structure = request.POST.get('face_structure')
        frame_color = request.POST.get('frame_color')
        panelset_id = request.POST.get('panelset_id')

        if panelset_id:
            return JsonResponse({'res': 3, 'panelset_id':panelset_id})

        # 校验数据
        if not all([project, mark, sets, production_time, model, height, width, wheel, sound_test, face_structure, frame_color]):
            return JsonResponse({'res': 0, 'errmsg': '数据不完整'})

        # 检验已有相同名字
        try:
            panelset = Panelsets.objects.get(mark=mark,project=project)
        except Panelsets.DoesNotExist:
            # 用户名不存在
            panelset = None
        if panelset:
            return JsonResponse({'res': 1, 'errmsg': '此屏风编号已经存在'})

        # 业务处理
        panelset = Panelsets.objects.create(
            project=project,
            mark=mark,
            sets=sets,
            production_time=production_time,
            model=model,
            height=height,
            width=width,
            wheel=wheel,
            sound_test=sound_test,
            face_structure=face_structure,
            frame_color=frame_color
        )

        panelset_id = panelset.id
        # 返回应答
        return JsonResponse({'res': 2, 'panelset_id':panelset_id})

# /PDS/panelsadd 新建屏风组
class PanelsAddView(View):
    """ 新建组 """
    def get(self, request):
        """ 显示页面 """
        # 接收数据
        panelset_id = request.GET.get('id')
        return render(request, 'PDS/panelsadd.html',{'panelset_id':panelset_id})

    def post(self, request):
        """ 添加新组 """
        # 接收数据
        panelset = Panelsets.objects.get(id=request.POST.get('panelset_id'))
        panle_no = request.POST.get('panle_no')
        quantity = request.POST.get('quantity')
        carrier_space = request.POST.get('carrier_space')
        panel_width = request.POST.get('panel_width')
        panel_pic = PicsModels.objects.get(id=request.POST.get('pic_id'))
        
        # 校验数据
        if not all([panelset, panle_no, quantity, carrier_space, panel_width, panel_pic]):
            return JsonResponse({'res': 0, 'errmsg': '数据不完整'})

        panel_type = panel_pic.pictype

        # 业务处理
        panel = Panles.objects.create(
            panelset=panelset,
            panle_no=panle_no,
            quantity=quantity,
            carrier_space=carrier_space,
            panel_width=panel_width,
            panel_pic=panel_pic,
            panel_type=panel_type
        )

        svgcode=panel_pic.leftside.svgcode+panel_pic.middle.svgcode+panel_pic.rightside.svgcode+panel_pic.wheel.svgcode

        context = {
            'res':2,
            'panle_no':panle_no,
            'quantity':quantity,
            'carrier_space':carrier_space,
            'panel_width':panel_width,
            'svgcode':svgcode,
            'panel_type':panel_type
        }

        # 返回应答
        return JsonResponse(context)



# /PDS/panelsdata 屏风数据
class PanelsDataView(View):
    """ 屏风数据 """
    def get(self, request):
        # 获取全部用户的数据
        ret = Panles.objects.all()
        # 转化数据
        panels = ret.values()
        # 获取数据数量
        count = ret.count()
        data = list(panels)
        # 组织上下文
        context = {
            "code": 0,
            "msg": "",
            "count": count,
            "data": data
        }
        # 使用ComplexEncoder格式化jason
        return HttpResponse(json.dumps(context))