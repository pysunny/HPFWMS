from django.shortcuts import render
from django.views.generic import View
from standard.models import PanelModels, PartPicModels, PicsModels
from django.http import JsonResponse, HttpResponse
# from utils.ComplexEncoder import ComplexEncoder
# from django.core.paginator import Paginator
from utils.getData import getData
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
        # 获取全部数据
        ret = PanelModels.objects.all()
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        # 调用分页的方法 获取数据
        context = getData().getData(ret, page, limit)
        # 返回数据
        return HttpResponse(json.dumps(context, ensure_ascii=False))

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

        model_choices = PanelModels

        context = {
            'model':model,
            'model_choices':model_choices
        }

        # 如果接受数据没有id ,表示是新建模式,不用返回数据
        return render(request, 'standard/models.html', context)

    def post(self, request):
        """ 添加新项目 """
        # 接收数据
        model_id = request.GET.get('model_id')
        name = request.POST.get('name')
        series = request.POST.get('series')
        desc = request.POST.get('desc')
        top_clearance = request.POST.get('top_clearance')
        top_option = request.POST.get('top_option')
        basic_material = request.POST.get('basic_material')
        steel_plate = request.POST.get('steel_plate')
        rockwool = request.POST.get('rockwool')
        bottom_option = request.POST.get('bottom_option')
        bottom_clearance = request.POST.get('bottom_clearance')
        wheel_type = request.POST.get('wheel_type')
        # 校验数据
        if not all([name, series, top_clearance, basic_material, steel_plate, bottom_clearance, desc]):
            return JsonResponse({'res': 0, 'errmsg': '数据不完整'})
        # 检验已有相同名字
        try:
            panelmodel = PanelModels.objects.get(
                name=name, 
                basic_material=basic_material, 
                bottom_clearance=bottom_clearance, 
                top_option=top_option, 
                bottom_option=bottom_option, 
                steel_plate=steel_plate, 
                wheel_type=wheel_type
            )
            if model_id:
                panelmodel = panelmodel.exclude(id=model_id)
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
                top_option=top_option,
                basic_material=basic_material,
                steel_plate=steel_plate,
                rockwool=rockwool,
                bottom_option=bottom_option,
                bottom_clearance=bottom_clearance,
                desc=desc,
                wheel_type=wheel_type
            )
            # 返回应答
            return JsonResponse({'res': 2})

        panelmodel = PanelModels.objects.create(
            name=name,
            series=series,
            top_clearance=top_clearance,
            top_option=top_option,
            basic_material=basic_material,
            steel_plate=steel_plate,
            rockwool=rockwool,
            bottom_clearance=bottom_clearance,
            bottom_option=bottom_option,
            desc=desc,
            wheel_type=wheel_type
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
        # 获取全部数据
        ret = PicsModels.objects.all()
        # 获取页码及页数
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        # 调用分页的方法 获取数据
        context = getData().getData(ret, page, limit)
        # 获取数据中data数据
        data = context["data"]
        # 在字典内添加四个组件代码
        for pic in data:
            pic['leftsidecode']=PartPicModels.objects.get(id=pic['leftside']).svgcode
            pic['middlecode']=PartPicModels.objects.get(id=pic['middle']).svgcode
            pic['wheelcode']=PartPicModels.objects.get(id=pic['wheel']).svgcode
            pic['rightsidecode']=PartPicModels.objects.get(id=pic['rightside']).svgcode
            pic['textcode']=PartPicModels.objects.get(id=pic['text']).svgcode

        return HttpResponse(json.dumps(context, ensure_ascii=False))

# /standard/pics 屏风图元操作
class PicsView(View):
    def get(self, request):
        """ 显示页面 """
        # 接收数据
        pic_id = request.GET.get('pic_id')
        pic = ""
        # 获取各部位
        leftside = PartPicModels.objects.filter(panelpart=0, is_activate=True)
        middle = PartPicModels.objects.filter(panelpart=1, is_activate=True)
        wheel = PartPicModels.objects.filter(panelpart=2, is_activate=True)
        rightside = PartPicModels.objects.filter(panelpart=3, is_activate=True)
        text = PartPicModels.objects.filter(panelpart=4, is_activate=True)

        # 如果pic_id有值，表示是表示是修改模式,返回pic
        if pic_id:
            pic = PicsModels.objects.get(id=pic_id)

        context = {
            'pic':pic,
            'leftside':leftside,
            'middle':middle,
            'wheel':wheel,
            'rightside':rightside,
            'text':text,
            'PicsModels':PicsModels
        }
        
        return render(request, 'standard/pics.html', context)

    def post(self, request):
        """ 添加图元 """
        user = request.user
        pic_id = request.POST.get('pic_id')
        name = request.POST.get('picsname')
        paneltype = request.POST.get('paneltype')
        pictype = request.POST.get('pictype')
        extra_length = request.POST.get('extra_length')
        leftside = PartPicModels.objects.get(id=request.POST.get('leftside'))
        middle = PartPicModels.objects.get(id=request.POST.get('middle'))
        wheel = PartPicModels.objects.get(id=request.POST.get('wheel'))
        rightside = PartPicModels.objects.get(id=request.POST.get('rightside'))
        text = PartPicModels.objects.get(id=request.POST.get('text'))


        # 根据轮子代码定义单向式或者多向式,注意 修改了数据库 可能要更新。
        if request.POST.get('wheel') == '41' or request.POST.get('wheel') == '46':
            wheeltype = "0"
        else:
            wheeltype = "1"

        # 根据文字图层定义pin_mark,注意 修改了数据库 可能要更新。
        if request.POST.get('text') == "47":
            pin_mark = False
        else:
            pin_mark = True

        # 校验数据
        if not all([name, paneltype, wheeltype, pictype, leftside, middle, wheel, rightside, text]):
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
            pic = PicsModels.objects.filter(leftside=leftside, middle=middle, wheel=wheel, rightside=rightside, text=text)
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
                rightside=rightside,
                extra_length = extra_length,
                pin_mark = pin_mark,
                user = user
            )
            # 返回应答
            return JsonResponse({'res': 2})

        # pic_id没有值，表示是新建模式，需要创建
        print('##############')
        PicsModels.objects.create(
            name=name,
            paneltype=paneltype,
            wheeltype=wheeltype,
            pictype=pictype,
            leftside=leftside,
            middle=middle,
            wheel=wheel,
            rightside=rightside,
            extra_length = extra_length,
            pin_mark = pin_mark,
            user = user
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
        # 获取全部的数据
        ret = PartPicModels.objects.all()
        # 获取页数及数量
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        # 调用分页的方法 获取数据
        context = getData().getData(ret, page, limit)

        return HttpResponse(json.dumps(context))

# /standard/picspartsadd 新建组件
class PicsPartsView(View):
    def get(self, request):
        """ 显示页面 """
        picpart_id = request.GET.get('picpart_id')
        picpart = ""
        # 如果picpart_id有值，表示是修改模式，需要返回picpart
        if picpart_id:
            picpart = PartPicModels.objects.get(id=picpart_id)

        # 获取选项元组
        paneltype_choices = PartPicModels.PANEL_TYPE_CHOICES
        picpart_choices = PartPicModels.PIC_PART_CHOICES

        # 组织上下文
        context = {
            "picpart":picpart,
            'paneltype_choices':paneltype_choices,
            'picpart_choices':picpart_choices
        }

        return render(request, 'standard/picsparts.html', context)

    def post(self, request):
        # 获取post数据

        """ 添加组件 """
        user = request.user
        picpart_id = request.POST.get('picpart_id')
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
            if picpart_id:
                picpart = picpart.exclude(id=picpart_id)
        except PartPicModels.DoesNotExist:
            # 用户名不存在
            picpart = None

        if picpart:
            return JsonResponse({'res': 1, 'errmsg': '此基本图元已经存在'})

        if picpart_id:
            # 如果修改模式，进行updata
            PartPicModels.objects.filter(id=picpart_id).update(
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
            svgcode=svgcode,
            is_activate=False,
            creator = user
        )
        # 返回应答
        return JsonResponse({'res': 2})


# 激活组件
class PicsPartsActiceView(View):
    # 这是用于激活组件
    def post(self, request):
        # 获取数据
        user = request.user
        picpart_id = request.POST.get('picpart_id')
        is_activate = request.POST.get('is_activate')
        # 转换数据
        if is_activate == "true":
            is_activate = True
        else:
            is_activate = False
        # 更新数据库
        if user.is_superuser:
            PartPicModels.objects.filter(id=picpart_id).update(is_activate=is_activate)
            # 返回应答
            return JsonResponse({'res': 2})
        else:
            return JsonResponse({'res': 1, 'errmsg':'你没有权限'})
