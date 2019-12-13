from django.shortcuts import render
from django.views.generic import View
from user.models import User
from project.models import Projects, Favorites
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from utils.getData import getData
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
            print(ret)

        # 调用分页的方法 获取数据
        context = getData().getData(ret, page, limit)
        # # 获取data
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



