from django.shortcuts import render
from django.views.generic import View
from project.models import Projects
from PDS.models import Panelsets, Panels, Ipdinfo
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
        # 需要添加权限，不是自己的区域项目部可以新建，编辑，删除
        # 获取的区域权限
        user = request.user
        location_permiss = eval(user.location_permiss)
        projectlocation = str(project.projectlocation)
        # 初始化
        user.has_permiss = False
        # 如果项目所在区域是用户的权限区域内
        if projectlocation in location_permiss:
            # 获得权限
            user.has_permiss = True
        return render(request, 'PDS/panelsetslist.html', {'project': project})

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
        ret = Panelsets.objects.filter(project_id=project_id, is_delete=False)
        # 调用分页的方法 整理数据
        context = getData().getData(ret, page, limit)
        # 添加选项内容
        # 获取data
        data = context["data"]
        for tmp in data:
            #     model = Panelsets.objects.get(id=tmp['id'])
            #     tmp['wheel'] = model.get_wheel_display()
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
            'panelset_id': panelset_id,
            'panels': panels,
        }

        return render(request, 'PDS/panelsetsadd_step_2.html', context)

# /PDS/panelsetsadd 新建组


class PanelsetsAddView(View):
    """ 新建组 """

    def get(self, request):
        """ 显示页面 """
        # 接收数据
        project_id = request.GET.get('project_id')
        panelset_id = request.GET.get('panelset_id')
        # 初始化panelset
        panelset = ""
        # 如果panelset_id为""，表示是新建模式，否则是修改模式:
        if panelset_id:
            panelset = Panelsets.objects.get(id=panelset_id)
            project_id = panelset.project.project_id

        project_name = Projects.objects.get(project_id=project_id).name

        # 组织上下文
        context = {
            'project_name': project_name,
            'project_id': project_id,
            'panelset': panelset,
            'Panelsets': Panelsets
        }

        return render(request, 'PDS/panelsetsadd_step_1.html', context)

    def post(self, request):
        """ 添加新组 """
        # 接收数据
        panelset_id = request.POST.get('panelset_id')
        project = Projects.objects.get(
            project_id=request.POST.get('project_id'))
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
        location = request.POST.get('location')
        handle_quantity = request.POST.get('handle_quantity')
        decoration_thickness = request.POST.get('decoration_thickness')

        # 校验数据
        if not all([project, mark, sets, production_time, model, height, width, wheel, sound_test, frame_color]):
            return JsonResponse({'res': 0, 'errmsg': '数据不完整'})

        # 检验已有相同名字
        try:
            panelset = Panelsets.objects.filter(
                mark=mark, project=project, is_delete=False)
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
                location=location,
                handle_quantity=handle_quantity,
                decoration_thickness=decoration_thickness,
                splicer=splicer
            )
            # 返回应答
            return JsonResponse({'res': 2, 'panelset_id': panelset_id})

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
            location=location,
            handle_quantity=handle_quantity,
            decoration_thickness=decoration_thickness,
            splicer=splicer
        )
        panelset_id = panelset.id
        # 返回应答
        return JsonResponse({'res': 2, 'panelset_id': panelset_id})

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
        panel = ""
        panelset_id = request.GET.get('panelset_id')
        if panelset_id:
            panelset = Panelsets.objects.get(id=panelset_id)
        panel_id = request.GET.get('panel_id')
        # 如果panel_id有值，表示是修改模式
        if panel_id:
            panel = Panels.objects.get(id=panel_id)
            panelset_id = panel.panelset.id
            panelset = Panelsets.objects.get(id=panelset_id)

            # 轮子数据
            # 获取数据
            carrier = panel.carrier_space
            width = panel.panel_width
            # xx/xxx/xx 双轮非对称 xx/xx 单轮  xxx 双轮 空 无轮
            if "/" in carrier:
                # 如果双轮非对称
                if carrier.count("/") == 2:
                    tmp = carrier.split("/")
                    panel.carrier_left = tmp[0]
                    panel.carrier_middel = tmp[1]
                    panel.carrier_right = tmp[2]

                # 如果单轮
                if carrier.count("/") == 1:
                    tmp = carrier.split("/")
                    panel.carrier_eq_left = tmp[0]
                    panel.carrier_eq_right = tmp[1]

            else:
                panel.carrier_middel = carrier
                panel.carrier_side = (int(width)-int(carrier))/2

        # 组织上下文
        context = {
            'panelset': panelset,
            'panel': panel
        }

        return render(request, 'PDS/panelsadd.html', context)

    def post(self, request):
        """ 添加屏风 """
        # 接收数据
        panelset = Panelsets.objects.get(id=request.POST.get('panelset_id'))
        panle_no = request.POST.get('panle_no')
        quantity = request.POST.get('quantity')
        carrier_space = request.POST.get('carrier')
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


# /pds/pdsprint 打印PDS页面
class PrintPdsView(View):
    def get(self, request):
        # 显示页面
        # 获取屏风组,传入的是列表
        panelset_id = request.GET.get('panelset_id')
        # 转换成列表
        panelset_id_list = eval('[' + panelset_id + ']')

        # 获取屏风组列表
        panelsets = Panelsets.objects.filter(id__in=panelset_id_list)
        for panelset in panelsets:
            # 获取全部屏风
            panelset.has_ipd = False
            panelset.panels = Panels.objects.filter(panelset=panelset, is_delete=False)
            try:
                ipd = Ipdinfo.objects.get(panelset=panelset, is_delete=False)
                panelset.has_ipd = True
                # 添加属性
                panelset.doorheight = ipd.doorheight
                panelset.keyoption = "Side A:%s / Side B:%s"%(ipd.get_lockeyoption_a_display(), ipd.get_lockeyoption_b_display())
            except :
                panelset.ipd = None
        # 组织上下文
        context = {
            'panelsets': panelsets
        }
        # 返回应答
        return render(request, 'PDS/print_PDS.html', context)


class Step3View(View):
    # 显示页面
    def get(self, request):
        # 返回应答
        panelset_id = request.GET.get('panelset_id')
        # 获取门锁的选择值
        panelset = Panelsets.objects.get(id=panelset_id)

        # 监测panel是否有门中门，如果没有门中门传输fasle
        # 获取全部屏风
        panels = Panels.objects.filter(panelset=panelset, is_delete=False)
        # 初始值
        has_ipd = False
        # 如果有4(uipd),5(lipd),就改变has_ipd
        for tmp in panels:
            if tmp.panel_type == 4 or tmp.panel_type == 5:
                has_ipd = True
                continue

        # 把这边传给panelset，方便在网页隐藏div 
        panelset.has_ipd = has_ipd
        ipd = None
        # 如果有门中门
        if has_ipd:
            try:
                ipd = Ipdinfo.objects.get(panelset=panelset)
            except :
                ipd = None

        # 组织上下文
        context = {
            'Ipdinfo': Ipdinfo,
            'panelset_id': panelset_id,
            'panelset':panelset,
            'ipd':ipd
        }
        return render(request, 'PDS/panelsetsadd_step_3.html', context)


    def post(self, request):
            # 接收数据
            postData = request.POST.dict()
            ipdinfo_id = postData.get('ipdinfo_id')
            doorheight = postData.get('doorheight')
            # 更新需要的字段
            dataupdate_list = ["decoration_text", "note"]
            # 生成字典
            dataupdate = {key: value for key, value in postData.items() if key in dataupdate_list}
            # 添加装饰面说明及备注信息
            Panelsets.objects.filter(id=postData['panelset_id']).update(**dataupdate)
            # 添加门中门信息,没有没有门高，表示没有门中门信息
            if doorheight:
                # # 门中门的需要的key
                dataipd_list = ["lockeroption_a", "lockeroption_b", "doorheight", "panelset_id"]
                data_ipd = {key: value for key,value in postData.items() if key in dataipd_list}
                if ipdinfo_id:
                    Ipdinfo.objects.filter(id=ipdinfo_id).update(**data_ipd)
                    # 返回应答
                    return JsonResponse({'res': 2, 'ipdinfo_id':ipdinfo_id})
                else:
                    ipd = Ipdinfo.objects.create(**data_ipd)
                # 返回应答
                ipdinfo_id = ipd.id
                return JsonResponse({'res': 2, 'ipdinfo_id':ipdinfo_id})
            return JsonResponse({'res': 2})
