from django.shortcuts import render
from django.views.generic import View
from standard.models import PanelModels, PartPicModels, PicsModels
from django.http import JsonResponse, HttpResponse
from utils.ComplexEncoder import ComplexEncoder
from django.core.paginator import Paginator
import json

""" 屏风型号 """
# /standard/modelslist 屏风型号
class ModelsListView(View):
    def get(self, request):
        """ 显示页面 """
        return render(request, 'standard/modelslist.html')

# /standard/modelsdata 型号数据
class ModelsDataView(View):
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
            "code": 0,
            "msg": "",
            "count": count,
            "data": data
        }
        # 使用ComplexEncoder格式化jason
        return HttpResponse(json.dumps(context, cls=ComplexEncoder))

# /standard/models 屏风型号操作
class ModelsView(View):
    def get(self, request):
        """ 显示页面 """
        # 接收数据
        model_id = request.GET.get('model_id')
        model = ""
        # 如果接受数据有id,表示是修改模式,返回model
        if model_id:
            model = PanelModels.objects.get(id=model_id)

        return render(request, 'standard/models.html',{'model':model})
        # 如果接受数据没有id ,表示是新建模式,不用返回数据

    def post(self, request):
        """ 添加新项目 """
        # 接收数据
        model_id = request.GET.get('model_id')
        name = request.POST.get('name')
        series = request.POST.get('series')
        desc = request.POST.get('desc')
        top_clearance = request.POST.get('top_clearance')
        top_seal = request.POST.get('top_seal')
        top_mechanism = request.POST.get('top_mechanism')
        basic_material = request.POST.get('basic_material')
        steel_plate = request.POST.get('steel_plate')
        rockwool = request.POST.get('rockwool')
        bottom_clearance = request.POST.get('top_clearance')
        bottom_seal = request.POST.get('top_seal')
        bottom_mechanism = request.POST.get('top_mechanism')
        # 校验数据
        if not all([name, series, top_clearance, basic_material, steel_plate, bottom_clearance, desc]):
            return JsonResponse({'res': 0, 'errmsg': '数据不完整'})
        # 检验已有相同名字
        try:
            panelmodel = PanelModels.objects.get(name=name, basic_material=basic_material, bottom_clearance=bottom_clearance, steel_plate=steel_plate)
        except PanelModels.DoesNotExist:
            # 用户名不存在
            panelmodel = None
            
        if panelmodel:
            return JsonResponse({'res': 1, 'errmsg': '型号已经存在'})
        # 业务处理
        if model_id:
        # 如果model_id有值，就进行更新操作。
            PanelModels.objects.filter(id=model_id).update(
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
            return JsonResponse({'res': 2})

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
        return JsonResponse({'res': 2})
        
        
""" 屏风图元 """
# /standard/picslist 屏风图元
class PicsListView(View):
    def get(self, request):
        """ 显示页面 """
        return render(request, 'standard/picslist.html')

# /standard/picsdata 图元数据
class PicsDataView(View):
    def get(self, request):
        # 获取全部用户的数据
        ret = PicsModels.objects.all()
        # 转化数据
        pics = ret.values()
        # 获取数据数量
        count = ret.count()
        data = list(pics)

        # 在字典内添加四个组件代码
        for pic in data:
            pic['leftsidecode']=PartPicModels.objects.get(id=pic['leftside_id']).svgcode
            pic['middlecode']=PartPicModels.objects.get(id=pic['middle_id']).svgcode
            pic['wheelcode']=PartPicModels.objects.get(id=pic['wheel_id']).svgcode
            pic['rightsidecode']=PartPicModels.objects.get(id=pic['rightside_id']).svgcode

        # 组织上下文
        context = {
            "code": 0,
            "msg": "",
            "count": count,
            "data": data
        }
        # 使用ComplexEncoder格式化jason
        return HttpResponse(json.dumps(context, cls=ComplexEncoder))

# /standard/pics 屏风图元操作
class PicsView(View):
    def get(self, request):
        """ 显示页面 """
        # 接收数据
        pic_id = request.GET.get('pic_id')
        pic = ""
        # 获取各部位
        leftside = PartPicModels.objects.filter(panelpart=0)
        middle = PartPicModels.objects.filter(panelpart=1)
        wheel = PartPicModels.objects.filter(panelpart=2)
        rightside = PartPicModels.objects.filter(panelpart=3)

        # 如果pic_id有值，表示是表示是修改模式,返回pic
        if pic_id:
            pic = PicsModels.objects.get(id=pic_id)

        context = {
            'pic':pic,
            'leftside':leftside,
            'middle':middle,
            'wheel':wheel,
            'rightside':rightside
        }
        
        return render(request, 'standard/pics.html', context)

    def post(self, request):
        """ 添加图元 """
        pic_id = request.POST.get('pic_id')
        name = request.POST.get('picsname')
        paneltype = request.POST.get('paneltype')
        pictype = request.POST.get('pictype')
        wheel_id = request.POST.get('wheel')
        leftside = PartPicModels.objects.get(id=request.POST.get('leftside'))
        middle = PartPicModels.objects.get(id=request.POST.get('middle'))
        wheel = PartPicModels.objects.get(id=wheel_id)
        rightside = PartPicModels.objects.get(id=request.POST.get('rightside'))

        wheeltype = '0'
        if wheel_id == '33':
            wheeltype = '1'

        # 校验数据
        if not all([name, paneltype, wheeltype, pictype, leftside, middle, wheel, rightside]):
            return JsonResponse({'res': 0, 'errmsg': '数据不完整'})

        # 检验是否有相同名字
        try:
            pic = PicsModels.objects.filter(name=name, wheel=wheel)
            # 如果是修改模式，需要排除自己
            if pic_id:
                pic = pic.exclude(id=pic_id)
        except PicsModels.DoesNotExist:
            # 用户名不存在
            pic = None
        if pic:
            return JsonResponse({'res': 1, 'errmsg': '此图元名称已经存在'})
        # 检验是否有结构的屏风图元
        try:
            pic = PicsModels.objects.filter(leftside=leftside, middle=middle, wheel=wheel, rightside=rightside)
            # 如果是修改模式，需要排除自己
            if pic_id:
                pic = pic.exclude(id=pic_id)
        except PicsModels.DoesNotExist:
            # 用户名不存在
            pic = None
        if pic:
            return JsonResponse({'res': 3, 'errmsg': '此图元结构已经存在'})
        
        # 业务处理
        # 如果pic_id有值，表示是修改模式，需要使用更新

        if pic_id:
            PicsModels.objects.filter(id=pic_id).update(
                name=name,
                paneltype=paneltype,
                wheeltype=wheeltype,
                pictype=pictype,
                leftside=leftside,
                middle=middle,
                wheel=wheel,
                rightside=rightside
            )
            # 返回应答
            return JsonResponse({'res': 2})

        # pic_id没有值，表示是新建模式，需要创建
        PicsModels.objects.create(
            name=name,
            paneltype=paneltype,
            wheeltype=wheeltype,
            pictype=pictype,
            leftside=leftside,
            middle=middle,
            wheel=wheel,
            rightside=rightside
        )
        # 返回应答
        return JsonResponse({'res': 2})


""" 屏风组件 """
# /standard/picspartslist 屏风组件
class PicsPartsListView(View):
    def get(self, request):
        """ 显示页面 """
        return render(request, 'standard/picspartslist.html')

# /standard/picspartsdata 组件数据
class PicsPartsDataView(View):
    def get(self, request):
        # 获取页数及数量
        page = request.GET.get('page')
        limit = request.GET.get('limit')
        # 获取全部用户的数据
        ret = PartPicModels.objects.all()

        # 转化数据
        parts = ret.values()

        # 对数据进行分页
        paginator = Paginator(parts, limit)
        # 获取数据数量
        count = paginator.count

        parts = paginator.page(page)
        
        data = list(parts)
        # 组织上下文
        context = {
            "code": 0,
            "msg": "",
            "count": count,
            "data": data
        }
        # 使用ComplexEncoder格式化jason
        return HttpResponse(json.dumps(context, cls=ComplexEncoder))

# /standard/picspartsadd 新建组件
class PicsPartsView(View):
    def get(self, request):
        """ 显示页面 """
        picparts_id = request.GET.get('picparts_id')
        picpart = ""
        # 如果picparts_id有值，表示是修改模式，需要返回picpart
        if picparts_id:
            picpart = PartPicModels.objects.get(id=picparts_id)

        return render(request, 'standard/picsparts.html', {"picpart":picpart})

    def post(self, request):
        """ 添加组件 """
        picparts_id = request.POST.get('picparts_id')
        name = request.POST.get('picspartsname')
        paneltype = request.POST.get('paneltype')
        panelpart = request.POST.get('panelpart')
        svgcode = request.POST.get('svgcode')
        
        # 校验数据
        if not all([name, paneltype, panelpart, svgcode]):
            return JsonResponse({'res': 0, 'errmsg': '数据不完整'})

        # 检验已有相同名字,# 如果修改模式要排除本身
        try:
            picpart = PartPicModels.objects.filter(name=name, panelpart=panelpart)
            if picparts_id:
                picpart = picpart.exclude(id=picparts_id)
        except PartPicModels.DoesNotExist:
            # 用户名不存在
            picpart = None

        if picpart:
            return JsonResponse({'res': 1, 'errmsg': '此基本图元已经存在'})

        if picparts_id:
            # 如果修改模式，进行updata
            PartPicModels.objects.filter(id=picparts_id).update(
            name=name,
            paneltype=paneltype,
            panelpart=panelpart,
            svgcode=svgcode
            )
            return JsonResponse({'res': 2})

        # 业务处理
        picpart = PartPicModels.objects.create(
            name=name,
            paneltype=paneltype,
            panelpart=panelpart,
            svgcode=svgcode
        )
        # 返回应答
        return JsonResponse({'res': 2})


