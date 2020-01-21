from django.shortcuts import render
from django.views.generic import View
from user.models import User
from project.models import Projects, Favorites, PdsVersion
from PDS.models import Panelsets, Panels
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from utils.getData import getData
from django_redis import get_redis_connection
from django.db import transaction
import json

# /project/list 项目列表
class ProjectListView(View):
    def get(self, request):
        """ 显示页面 """
        return render(request, 'project/list.html')

# /project/publiclistlist 公共项目
class PublicListView(View):
    def get(self, request):
        """ 显示页面 """
        return render(request, 'project/publiclist.html')

# /project/favoriteslist 公共项目
class FavoritesListView(View):
    def get(self, request):
        """ 显示页面 """
        return render(request, 'project/favoriteslist.html')

# /project/add 新建项目
class ProjectAddView(View):
    def get(self, request):
        """ 显示页面 """
        # 获取数据 project_id
        project_id = request.GET.get('project_id')
        location_choices = Projects.LOCATION_CHOICES

        # 初始化数据
        project = ""
        if project_id:
            project = Projects.objects.get(project_id=project_id)

        context = {
            'project':project,
            'location_choices':location_choices
        }

        return render(request, 'project/add.html', context)

    def post(self, request):
        """ 添加新项目 """
        # 接收数据
        user = request.user
        project_id = request.POST.get('project_id')
        projectname = request.POST.get('name')
        address = request.POST.get('address')
        projectlocation = request.POST.get('projectlocation')
        location = request.POST.get('location')
        # 校验数据
        # 检验是否已有项目
        try:
            project = Projects.objects.filter(name=projectname)
            # 如果是修改模式，需要排除自己
            if project_id:
                project = project.exclude(project_id=project_id)
        except Projects.DoesNotExist:
            # 用户名不存在
            project = None
        if project:
            return JsonResponse({'res': 1, 'errmsg': '项目已经存在'})

        # 业务处理
        # 如果是修改模式，需要使用更新
        if project_id:
            Projects.objects.filter(project_id=project_id).update(
                name=projectname,
                address=address
            )
                # 返回应答
            return JsonResponse({'res': 2})
        
        # 下面是新建模式
        # 生产项目编号
        project_id = location + str(user.id) + datetime.now().strftime('%Y%m%d%H%M%S')
        # 保存数据到数据库
        project = Projects.objects.create(
            project_id=project_id,
            projectlocation=projectlocation,
            name=projectname,
            user=user,
            address=address
        )

        # 返回应答
        return JsonResponse({'res': 2})

# /project/data 数据接口
class ProjectDataView(View):
    def get(self, request):
        # 获取全部用户的数据
        user = request.user
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        page_name = request.GET.get('page_name')
        # 如果页面名是list，就返回个人地区的项目列表
        if page_name == "list":
            # 获取的区域权限
            location_permiss = eval(user.location_permiss)
            # 获取用户区域的全部项目
            ret = Projects.objects.filter(projectlocation__in=location_permiss, is_delete=False)
        # 如果页面名是publiclist，就返回公开项目的列表
        if page_name == "publiclist":
            ret = Projects.objects.filter(is_public=True, is_delete=False)

        # 如果页面名是favorites，就返回收藏的项目列表
        if page_name == "favoriteslist":
            #获取收藏夹中名字是user的条目
            ret = Favorites.objects.filter(user=user, is_favorites=True).values("project_id")
            ret = Projects.objects.filter(project_id__in=ret)

        # 调用分页的方法 获取数据
        context = getData().getData(ret, page, limit)
        # 获取data
        data = context["data"]
        for tmp in data:
            if not page_name == "publiclist":
                # 初始值为false
                tmp['is_favorites'] = False
                # 获取收藏数据user project
                project = Projects.objects.get(project_id=tmp['project_id'])
                # 在收藏夹模型找，如果有数据就返回ture
                try:
                    favorites = Favorites.objects.filter(user=user, project=project, is_favorites=True)
                except:
                    favorites = None
                if favorites:
                    tmp['is_favorites'] = True
            
            tmp['user'] = User.objects.get(id=tmp['user']).username

        print(context)
        # 使用ComplexEncoder格式化jason
        return HttpResponse(json.dumps(context))

# /project/delete 删除项目
class ProjectDeleteView(View):
    def post(self, request):
        # 获取要删除的项目ID
        project_id = request.POST.get('project_id')
        # 更新数据库
        Projects.objects.filter(project_id=project_id).update(is_delete = True)
        # 返回应答
        return JsonResponse({'res': 2})
        
# /project/publicactive 删除项目
class PublicActiveView(View):
    def post(self, request):
        # 获取要删除的项目ID
        project_id = request.POST.get('project_id')
        is_public = request.POST.get('is_public')
        # 转换数据
        if is_public == "true":
            is_public = True
        else:
            is_public = False
        # 更新数据库
        Projects.objects.filter(project_id=project_id).update(is_public=is_public)
        # 返回应答
        return JsonResponse({'res': 2})

# /project/favorites 验证收藏
class FavoritesActiveview(View):
    def post(self, request):
        user = request.user
        project_id = request.POST.get('project_id')
        is_favorites = request.POST.get('is_favorites')
        # print(project_id + is_favorites)
        project = Projects.objects.get(project_id=project_id)
        # 先判断是否条目，如果没有就想创建
        try:
            favorites = Favorites.objects.filter(user=user, project=project)
        except:
            favorites = None
        if not favorites:
            Favorites.objects.create(user=user, project=project, is_favorites=False)
            favorites = Favorites.objects.filter(user=user, project=project)

        # 根据is_favorites去修改数据库
        if is_favorites == "true":
            favorites.update(is_favorites=True)
        else:
            favorites.update(is_favorites=False)
        return JsonResponse({'res': 2})

#/projectdetail/<project_id> 屏风细节
class ProjectDetailView(View):
    def get(self, request, project_id):
        """ 显示页面 """
        # 接收数据
        # project_id = request.GET.get('project_id')
        project = Projects.objects.get(project_id=project_id)
        return render(request, 'project/projectdetail.html', {'project': project})

#/project/saveversion 保存版本,组,屏风数据
class saveVersionView(View):
    @transaction.atomic
    def post(self, request):
        # 获取Redis数据
        user = request.user
        conn = get_redis_connection('default')
        workspaceKeyName = 'workspace_%s' % user.id
        # 获取第一个数据，也就是project_di
        project_di = conn.lrange(workspaceKeyName, 0, -1)[0]
        project = eval(project_di)
        project_id = project.get("project_id")

        # 查询这个项目最新的版本名称
        try:
            pdsversion = PdsVersion.objects.filter(project=project_id).latest('create_time')
            name = chr(ord(pdsversion.name)+1)
        except :
            name = chr(65)
        # 设置事务保存点
        save_id = transaction.savepoint()
        try:
            # 创建一条新版本
            newversion = PdsVersion.objects.create(project_id=project_id,name=name,user=user)

            # 初始化统计数量
            setsSum = areaSum = lengthSum = lcpSum = bpSum = ipdSum = bspSum = panelSum =0
            
            # 从redis数据库获取数据
            workData =  conn.lrange(workspaceKeyName, 1, -1)
            # 遍历Redis数据,创建组，屏风数据
            for tmp_s in workData:
                # 获取组属性，屏风列表，转化成可用数据
                set_di = eval(tmp_s)
                panel_li = set_di.get('panel_li')
                
                # 添加数据project_id,pdsversion
                set_di.update({'pdsversion':newversion})
                # 删除没有用的数据
                set_di.pop("ipd_qu")
                set_di.pop("panel_li")  

                # 检验是否缺少数据
                data = []
                necessary_li = ['project_id', 'mark', 'sets', 'production_time', 'model_id', 'height', 'width', 'wheel', 'sound_test', 'frame_color', 'splicer', 'pdsversion', 'decoration_thickness', 'handle_quantity']

                for tmp in necessary_li:
                    ret = set_di.get(tmp)
                    # 如果是0，转为文本
                    if ret == 0:
                        ret = str(ret)
                    data.append(ret)


                if not all(data):
                    # 数据不完整，退回mysql节点
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'res':1, 'errmsg':'参数不完整'})

                # 创建一数据set
                panelset = Panelsets.objects.create(**set_di)

                # 计算数据setsSum,lengthSum,areaSum
                setsSum += int(set_di.get('sets'))
                lengthSum += int(set_di.get('width'))/1000
                areaSum += int(set_di.get('width'))*int(set_di.get('height'))/1000000

                # 创建数据panel
                for tmp_p in panel_li:
                    # 遍历计算每种屏风的数量
                    pictype = tmp_p.get('pictype')
                    quantity = int(tmp_p.get('quantity'))
                    if int(pictype) == 1:
                        lcpSum += quantity

                    elif int(pictype) == 4 or pictype == 5:
                        ipdSum += quantity

                    elif int(pictype) == 2:
                        bspSum += quantity 
                    else:
                        bpSum += quantity
                    
                    # 删除没有用的数据
                    tmp_p.pop('pictype')
                    # 添加组属性
                    tmp_p.update({'panelset_id':panelset.id})
                    Panels.objects.create(**tmp_p)

            # 更新version数量
            panelSum = lcpSum+bpSum+ipdSum+bspSum
            newversion.setsSum = setsSum
            newversion.areaSum = areaSum
            newversion.lengthSum = lengthSum
            newversion.panelSum = panelSum
            newversion.lcpSum = lcpSum
            newversion.bpSum = bpSum
            newversion.ipdSum = ipdSum
            newversion.bspSum = bspSum
            newversion.save()

        except :
            # 发生错误，退回节点
            transaction.savepoint_rollback(save_id)
            return JsonResponse({'res': 1,'errmsg':'保存失败，数据有误'})
        
        # 修改项目的新项目标记
        project = Projects.objects.get(project_id=project_id)
        project.is_newversion = False
        project.save()
        # 提交事务
        transaction.savepoint_commit(save_id)
        return JsonResponse({'res': 2})

#/project/pdsversiondata 版本数据
class PdsversionDataView(View):
    def get(self, request, project_id):
        # 获取数据
        ret = PdsVersion.objects.filter(project_id=project_id).order_by('-create_time')
        # 调用分页的方法 获取数据
        context = getData().getData(ret, 1, 99)
        # 获取data
        data = context["data"]
        print(data)
        for tmp in data:
            tmp['user'] = User.objects.get(id=tmp['user']).username
        # 使用ComplexEncoder格式化jason
        return HttpResponse(json.dumps(context))
