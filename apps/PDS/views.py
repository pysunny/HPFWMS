from django.shortcuts import render
from django.views.generic import View
from project.models import Projects
from PDS.models import Panelsets, Panels
from standard.models import PanelModels, PicsModels
from django.http import JsonResponse, HttpResponse
from utils.getData import getData
import json

# /PDS/panelsetslist 组列表
class PanelsetsListView(View):
    """ 查看组列表视图类 """
    def get(self, request):
        """ 显示页面 """
        # 接收数据
        project_id = request.GET.get('project_id')
        project = Projects.objects.get(project_id=project_id)
        project.location = project.get_projectlocation_display()
        return render(request, 'PDS/panelsetslist.html', {'project':project})

# /PDS/panelsetsdata 组数据
class PanelsetsDataView(View):
    """ 组数据 """
    def get(self, request):
        # 获取全部用户的数据
        # 接收数据
        project_id = request.GET.get('project_id')
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        # 获取数据
        ret = Panelsets.objects.filter(project_id = project_id, is_delete=False)
        # 调用分页的方法 整理数据
        context = getData().getData(ret, page, limit)
        # 添加选项内容
        # 获取data
        data = context["data"]
        for tmp in data:
            model = Panelsets.objects.get(id=tmp['id'])
            tmp['wheel'] = model.get_wheel_display()
            tmp['model'] = PanelModels.objects.get(id=tmp['model']).name

        return HttpResponse(json.dumps(context))

# /PDS/panelsetsadd_setp2 新建屏风
class PanelsetsAddSetp2View(View):
    """ 新建组 """
    def get(self, request):
        """ 显示页面 """
        # 接收数据
        panelset_id = request.GET.get('panelset_id')
        # 获取key
        panelset = Panelsets.objects.get(id=panelset_id)
        # 获取panels数据
        panels = Panels.objects.filter(panelset=panelset, is_delete=False)


        # 组织上下文
        context = {
            'panelset_id':panelset_id,
            'panels':panels,
        }

        return render(request, 'PDS/panelsetsadd_step_2.html', context )

# /PDS/panelsetsadd 新建组
class PanelsetsAddView(View):
    """ 新建组 """
    def get(self, request):
        """ 显示页面 """
        # 接收数据
        project_id = request.GET.get('project_id')
        panelset_id  = request.GET.get('panelset_id')
        # 初始化panelset
        panelset = ""
        splicer_list = ""
        # 如果panelset_id为""，表示是新建模式，否则是修改模式:
        if panelset_id:
            panelset =  Panelsets.objects.get(id=panelset_id)
            project_id = panelset.project.project_id

            # 拆分横驳条
            splicer = panelset.splicer
            if not splicer == "":
                splicer_list = splicer.split(",")

        # 添加wheel 选项内容
        wheel_choices = Panelsets.WHEEL_CHOICES
        face_structure = Panelsets.FACE_STRUCTURE_CHOICES
        sound_test = Panelsets.SOUND_TEST_CHOICES

        # 组织上下文
        context = {
            'project_id':project_id,
            'panelset':panelset,
            'splicer_list':splicer_list,
            'common_splicer':["平门中门","2400","4800","7200"],
            'wheel_choices':wheel_choices,
            'face_structure':face_structure,
            'sound_test':sound_test
        }

        return render(request, 'PDS/panelsetsadd_step_1.html', context)

    def post(self, request):
        """ 添加新组 """
        # 接收数据
        panelset_id = request.POST.get('panelset_id')
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
        splicer = request.POST.get('splicer')

        # 校验数据
        if not all([project, mark, sets, production_time, model, height, width, wheel, sound_test, face_structure, frame_color]):
            return JsonResponse({'res': 0, 'errmsg': '数据不完整'})

        # 检验已有相同名字
        try:
            panelset = Panelsets.objects.filter(mark=mark,project=project)
            # 如果是修改模式，需要排除自己
            if panelset_id:
                panelset = panelset.exclude(id=panelset_id)
        except Panelsets.DoesNotExist:
            # 用户名不存在
            panelset = None
        if panelset:
            return JsonResponse({'res': 1, 'errmsg': '此屏风编号已经存在'})

        
        # 如果panelset_id有值，表示是修改模式，需要使用更新。
        if panelset_id:
            Panelsets.objects.filter(id=panelset_id).update(
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
                frame_color=frame_color,
                splicer=splicer
            )
            # 返回应答
            return JsonResponse({'res': 2, 'panelset_id':panelset_id})

        # 新建模式业务处理
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
            frame_color=frame_color,
            splicer=splicer
        )
        panelset_id = panelset.id
        # 返回应答
        return JsonResponse({'res': 2, 'panelset_id':panelset_id})

# /PDS/panelsetsdelete 删除组
class PanelsetsDeleteView(View):
    def post(self, request):
        # 获取要删除的组ID
        panelset_id = request.POST.get('panelset_id')
        # 更新数据库
        Panelsets.objects.filter(id=panelset_id).update(is_delete=True)
        # 返回应答
        return JsonResponse({'res': 2})

# /PDS/panelsadd 新建屏风
class PanelsAddView(View):
    """ 新建组 """
    def get(self, request):
        """ 显示页面 """
        # 接收数据
        panelset_id = request.GET.get('panelset_id')
        panel_id = request.GET.get('panel_id')
        panel = ""
        # 如果panel_id有值，表示是修改模式
        if panel_id:
            panel = Panels.objects.get(id=panel_id)
            panelset_id = panel.panelset.id
        # 组织上下文
        context = {
            'panelset_id':panelset_id,
            'panel':panel
        }

        return render(request, 'PDS/panelsadd.html', context)

    def post(self, request):
        """ 添加屏风 """
        # 接收数据
        panelset = Panelsets.objects.get(id=request.POST.get('panelset_id'))
        panle_no = request.POST.get('panle_no')
        quantity = request.POST.get('quantity')
        carrier_space = request.POST.get('carrier_space')
        panel_width = request.POST.get('panel_width')
        panel_pic = PicsModels.objects.get(id=request.POST.get('pic_id'))
        panel_id = request.POST.get('panel_id')
        
        # 校验数据
        if not all([panelset, panle_no, quantity, carrier_space, panel_width, panel_pic]):
            return JsonResponse({'res': 0, 'errmsg': '数据不完整'})

        panel_type = panel_pic.pictype


        # 如果panel_id有值，表示是修改模式
        if panel_id:
            # 业务处理
            Panels.objects.filter(id=panel_id).update(
                panelset=panelset,
                panle_no=panle_no,
                quantity=quantity,
                carrier_space=carrier_space,
                panel_width=panel_width,
                panel_pic=panel_pic,
                panel_type=panel_type
            )

            # 返回应答
            return JsonResponse({'res': 2})
        # 业务处理
        Panels.objects.create(
            panelset=panelset,
            panle_no=panle_no,
            quantity=quantity,
            carrier_space=carrier_space,
            panel_width=panel_width,
            panel_pic=panel_pic,
            panel_type=panel_type
        )

        # 返回应答
        return JsonResponse({'res': 2})

# /PDS/panelsdelete 删除屏风
class PanelsDeleteView(View):
    def post(self, request):
        # 获取要删除的屏风ID
        panel_id = request.POST.get('panel_id')
        # 更新数据库
        Panels.objects.filter(id=panel_id).update(is_delete=True)
        # 返回应答
        return JsonResponse({'res': 2})


#/pds/pdsprint 打印PDS页面
class PrintPdsView(View):
    def get(self, request):
        #显示页面
        # 获取屏风组ID
        panelset_id = request.GET.get('panelset_id')
        # 获取屏风组
        panelset = Panelsets.objects.get(id=panelset_id)
        # 获取所在项目
        project = panelset.project
        # 获取全部屏风
        panels = Panels.objects.filter(panelset=panelset, is_delete=False)
        # 组织上下文
        context = {
            'project':project,
            'panelset':panelset,
            'panels':panels
        }
        # 返回应答
        return render(request, 'PDS/print_PDS.html', context)