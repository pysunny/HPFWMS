from django.shortcuts import render
from django.views.generic import View
from user.models import User
from project.models import Projects
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from utils.getData import getData
import json

# /project/list 项目列表
class ProjectListView(View):
    def get(self, request):
        """ 显示页面 """
        return render(request, 'project/list.html')

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
        # 获取的区域权限
        location_permiss = eval(user.location_permiss)
        # 获取用户区域的全部项目
        ret = Projects.objects.filter(projectlocation__in=location_permiss, is_delete=False)
        # 调用分页的方法 获取数据
        context = getData().getData(ret, page, limit)
        # # 获取data
        data = context["data"]
        for tmp in data:
        #     model = Projects.objects.get(project_id=tmp['project_id'])
        #     tmp['projectlocation'] = model.get_projectlocation_display()
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



