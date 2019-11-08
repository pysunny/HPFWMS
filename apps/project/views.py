from django.shortcuts import render
from django.views.generic import View
from user.models import User
from project.models import Projects
from django.http import JsonResponse, HttpResponse
from utils.ComplexEncoder import ComplexEncoder
from datetime import datetime
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
        return render(request, 'project/add.html')

    def post(self, request):
        """ 添加新项目 """
        # 接收数据
        user = request.user
        projectname = request.POST.get('projectname')
        address = request.POST.get('address')
        projectlocation = request.POST.get('projectlocation')
        # 校验数据
        # 检验是否已有项目
        try:
            project = Projects.objects.get(name=projectname)
        except Projects.DoesNotExist:
            # 用户名不存在
            project = None
        if project:
            return JsonResponse({'res': 1, 'errmsg': '项目已经存在'})

        # 项目区域字典
        location_dict = {
            '0': 'HPF',
            '1': 'HHKD',
            '2': 'HGZ',
            '3': 'HSH',
            '4': 'HDL'
        }

        # 业务处理
        # 获取项目区域
        location = location_dict[projectlocation]
        # 生产项目编号
        project_id = location + str(user.id) + \
            datetime.now().strftime('%Y%m%d%H%M%S')
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
        # 获取的区域权限
        location_permiss = eval(user.location_permiss)
        # 获取用户区域的全部项目
        ret = Projects.objects.filter(projectlocation__in=location_permiss, is_delete=False)
        # 转化数据
        projects = ret.values()
        # 获取数据数量
        count = ret.count()
        data = list(projects)
        # 修改data数据中user_id变成name
        for datas in data:
            user_id = datas['user_id']
            user = User.objects.get(id=user_id)
            datas['user_id'] = user.username
        # 组织上下文
        context = {
            "code": 0,
            "msg": "",
            "count": count,
            "data": data
        }
        # 使用ComplexEncoder格式化jason
        return HttpResponse(json.dumps(context, cls=ComplexEncoder))

# /project/delete 删除项目
class ProjectDeleteView(View):
    def post(self, request):
        # 获取要删除的项目ID
        project_id = request.POST.get('project_id')
        # 更新数据库
        Projects.objects.filter(project_id=project_id).update(is_delete = True)
        # 返回应答
        return JsonResponse({'res': 2})



