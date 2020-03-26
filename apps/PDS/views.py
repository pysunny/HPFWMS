from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse
from project.models import Projects ,PdsVersion
from PDS.models import Panelsets, Panels
from standard.models import PanelModels, PicsModels
from django.http import JsonResponse, HttpResponse
from django_redis import get_redis_connection
from utils.getData import getData
import json
import datetime

# /pds/pdspreview 预览打印页面
class pdsPreviewView(View):
    def get(self, request):
        # 获取用户id
        # 建立空列表
        set_index = request.GET.get('set_index')
        set_index_list = eval('[' + set_index + ']')

        user = request.user
        conn = get_redis_connection('default')
        # 获取redis数据
        workspaceKeyName = 'workspace_%s' % user.id

        # 定义一个空列表
        panelsets = []
        # 遍历添加信息到panelsets
        for tmp in set_index_list:
            # 定义空字典
            panelset = {}
            # 获取第一个数据，也就是project_di
            project_di = conn.lrange(workspaceKeyName, 0, -1)[0]
            project = eval(project_di)
            panelset['project'] = project
            # 从redis数据库获取数据
            workData =  conn.lrange(workspaceKeyName, 0, -1)[int(tmp)]
            # 获取组属性，屏风列表，转化成可用数据
            set_di = eval(workData)
            panel_li = set_di.get('panel_li')
            # 为每个屏风添加svgcode
            for panel in panel_li:
                panel_pic_id = int(panel.get('panel_pic_id'))
                pic = PicsModels.objects.get(id = panel_pic_id)
                # 添加全部组件的代码
                svgcode = "%s%s%s%s%s"% (pic.leftside.svgcode, pic.middle.svgcode, pic.rightside.svgcode, pic.wheel.svgcode, pic.text.svgcode)
                pictype_name = pic.get_pictype_display()
                # 更新字典，添加添加svgcode
                panel.update({'svgcode':svgcode, 'pictype_name':pictype_name})
                
            # 添加型号属性
            model = PanelModels.objects.get(id = set_di['model_id'])
            panelset['model'] =model
            panelset.update(set_di)
            # 添加轮子，隔音600结构等属性
            panelset['wheel_text'] = [v for k,v in Panelsets.WHEEL_CHOICES if k==int(panelset.get('wheel'))][0]
            panelset['sound_test_text'] = [v for k,v in Panelsets.SOUND_TEST_CHOICES if k==int(panelset.get('sound_test'))][0]
            if panelset.get('face_structure'):
                panelset['face_structure_text'] = [v for k,v in Panelsets.FACE_STRUCTURE_CHOICES if k==int(panelset.get('face_structure'))][0]

            panelset['panels'] = panel_li
            panelsets.append(panelset)

        # 组织上下文
        context = {
            'panelsets': panelsets
        }
        # 返回应答
        return render(request, 'PDS/print_PDS.html', context)

#进入屏风编辑准备页面

class setEditView(View):
    def get(self, request, set_index):
        # 返回应答
        # 获取用户id
        user = request.user
        conn = get_redis_connection('default')
        workspaceKeyName = 'workspace_%s' % user.id
        #如果是新建
        if set_index == 'new':
            # 新建一个空数据
            panel_li = []
            set_di = {}
            # 获取第一个数据，也就是project_di
            project_di = conn.lrange(workspaceKeyName, 0, -1)[0]
            project = eval(project_di)
            project_id = project.get("project_id")
            set_di.update({'project_id':project_id,'ipd_qu':0,'panel_li':panel_li})
            # 数据转换成Redis   
            workData = str(set_di)
            conn.rpush(workspaceKeyName, workData)
            set_index = -1

        url = "/PDS/workspace/"+str(set_index)

        return redirect(url)
        
# 这是工作区视图
#/PDS/workspace/set_index
class workspaceView(View):
    def get(self, request, set_index):
        # 获取用户id
        user = request.user
        conn = get_redis_connection('default')
        # 获取redis数据
        workspaceKeyName = 'workspace_%s' % user.id

        # 从redis数据库获取数据
        workData =  conn.lrange(workspaceKeyName, 0, -1)[int(set_index)]

        # Redis数据结构：b"{'panel_li': [], 'set_di': {}}"
        # 修改成{'ipd_qu':0,'panel_li':panel_li}
        # 获取组属性，屏风列表，转化成可用数据
        set_di = eval(workData)
        panel_li = set_di.get('panel_li')
        # stc转换成int
        set_di.update({key:int(value) for key,value in set_di.items() if value and key in ['sound_test', 'model_id', 'lockeyoption_a', 'wheel', 'lockeyoption_b', 'face_structure']})
        # 为每个屏风添加svgcode
        for panel in panel_li:
            panel_pic_id = int(panel.get('panel_pic_id'))
            pic = PicsModels.objects.get(id = panel_pic_id)
            # 添加全部组件的代码
            svgcode = "%s%s%s%s%s"% (pic.leftside.svgcode, pic.middle.svgcode, pic.rightside.svgcode, pic.wheel.svgcode, pic.text.svgcode)
            pictype_name = pic.get_pictype_display()
            # 更新字典，添加添加svgcode
            panel.update({'svgcode':svgcode, 'pictype_name':pictype_name})
        
        # 获取全部的屏风型号数据，并传到前端
        models = PanelModels.objects.all()

        # 获取第一个数据，也就是project_di
        project_di = conn.lrange(workspaceKeyName, 0, -1)[0]
        project = eval(project_di)

        # 组织上下文
        context = {
            'models':models,
            'Panelsets':Panelsets,
            'panel_li':panel_li,
            'panelset':set_di,
            'set_index':set_index,
            'project':project
        }
        return render(request, 'PDS/setedit.html', context)

# 获取数据，并更新redis数据
    def post(self, request, set_index):
        # 获取前端数据
        postData = request.POST.dict()
        postData.pop('csrfmiddlewaretoken')

        # 如果是submit,不用读取redis
        if postData.get('mod') == 'submit':
            return JsonResponse({'res': 2})
        # 获取用户id

        user = request.user
        conn = get_redis_connection('default')
        # 获取redis数据
        workspaceKeyName = 'workspace_%s' % user.id
        # 从redis数据库获取数据
        workData =  conn.lrange(workspaceKeyName, 0, -1)[int(set_index)]
        # 获取组属性，屏风列表，转化成可用数据
        set_di = eval(workData)
        panel_li = set_di.get('panel_li')
        # 更新数据,如果是更新是panel_li

        if postData.get('mod') == 'addpanel':
            postData.pop('mod')
            # 生成屏风列表字典
            panel_di = {}
            panel_di.update(postData)
            # 添加到panel_li
            panel_li.append(panel_di)
            # 如果有门中门,数量+1
            if int(postData.get('pictype')) == 4 or int(postData.get('pictype')) == 5:
                set_di['ipd_qu'] += 1

        if postData.get('mod') == 'panel_li':
            postData.pop('mod')
            # 获取要修改的字典,index值就是所在数字
            panel_di = panel_li[int(postData.get('index'))]
            postData.pop('index')
            # 添加到panel_li
            panel_di.update(postData)

        if postData.get('mod') == 'remove':
            # 删除index元素
            del panel_li[int(postData.get('index'))]
            # 如果删除门中门,数量-1
            if int(postData.get('pictype')) == 4 or int(postData.get('pictype')) == 5:
                set_di['ipd_qu'] -= 1
                # 如果门中门数量为0,把字典的门中门数据删除
                if int(set_di.get('ipd_qu')) == 0:
                    set_di.update({'lockeyoption_a':'', 'lockeyoption_b':'', 'doorheight':''})
                    for tmp in ['lockeyoption_a', 'lockeyoption_b', 'doorheight']:
                        set_di.pop(tmp)

        if postData.get('mod') == 'move_left':
            #元素向左移
            index = int(postData.get('index'))
            tmp = panel_li[index]
            # 删除index元素
            del panel_li[index]
            # 重新插入
            panel_li.insert(index-1, tmp)

        if postData.get('mod') == 'move_right':
            #元素向右移
            index = int(postData.get('index'))
            tmp = panel_li[index]
            # 删除index元素
            del panel_li[index]
            # 重新插入
            panel_li.insert(index+1, tmp)
            
        if postData.get('mod') == 'set_di':
            # 添加组属性
            postData.pop('mod')

            # 如果下列列表选择了“”，需要删除
            value = list(postData.values())[0]
            if value:
                set_di.update(postData)
            else:
                set_di.pop(list(postData.keys())[0])

        # 数据转换成Redis   
        workData = str(set_di)
        # 写入Redis
        conn.lset(workspaceKeyName, int(set_index), workData)

        return JsonResponse({'res': 2})
        

class panelSelView(View):
    def get(self, request, set_index):
        # 获取paneltype, wheel_type, pictype
        paneltype = request.GET.get('paneltype')
        wheel_type = request.GET.get('wheel_type')
        pictype = request.GET.get('pictype')
        # 计算轮子数量, 多向式是两个，或者 0 ,单向式 是 1 
        wheelquantity = [0,2] if wheel_type == '0' else [1]

        pics = ""
        if not pictype == None:
            # 获取全部屏风图元
            pics = PicsModels.objects.filter(paneltype=paneltype, wheelquantity__in=wheelquantity, pictype=pictype)

        # 组织上下文
        context = {
            'PicsModels':PicsModels,
            'pics':pics,
            'set_index':set_index,
            'paneltype':paneltype,
            'wheel_type':wheel_type,
            'pictype':pictype if pictype == None else int(pictype)
        }
        return render(request, 'PDS/panel_sel.html', context)


#PDS/setDate redis组数据
class setDataView(View):
    def get(self, request):
        # 获取用户id
        user = request.user
        conn = get_redis_connection('default')
        workspaceKeyName = 'workspace_%s' % user.id
        data = conn.lrange(workspaceKeyName, 1, -1)
        # 建立空列表,并把数据些人
        json_list = []
        set_index = 1
        for tmp in data:
            set_di = eval(tmp)
            set_di.update({'set_index':set_index})
            json_list.append(set_di)
            set_index += 1

        count = len(json_list)
        # 返回layui需要的数据格式   
        context = {
            "code": 0,
            "msg": "",
            "count": count,
            "data": json_list
        }
        return HttpResponse(json.dumps(context))

#PDS/editpage 编辑页面
class editPageView(View):
    def get(self, request):
        # 获取用户id
        user = request.user
        conn = get_redis_connection('default')
        workspaceKeyName = 'workspace_%s' % user.id
        # 获取第一个数据，也就是project_di
        project_di = conn.lrange(workspaceKeyName, 0, -1)[0]
        project = eval(project_di)
        return render(request, 'PDS/editpage.html', {'project': project})

    # 获取页面的方法，请进行数据库操作 
    def post(self, request):
        set_index = request.POST.get('set_index')
        mod = request.POST.get('mod')
        # 获取用户id
        user = request.user
        conn = get_redis_connection('default')
        workspaceKeyName = 'workspace_%s' % user.id

        # 删除一组
        if mod == "delete":
            data_del = conn.lindex(workspaceKeyName, set_index)
            # 删除值
            conn.lrem(workspaceKeyName, 1, data_del)

        # 复制一组
        if mod == "copy":
            # 获取复制的数据
            workData = conn.lindex(workspaceKeyName, set_index)
            # 获取组属性，屏风列表，转化成可用数据
            set_di = eval(workData)
            # 修改复制数据的mark
            mark = set_di.get('mark')
            new_mark = "%s_copy" % mark
            set_di.update({'mark':new_mark})
            # 重新生成数据
            workData = str(set_di)
            
            # 插入数据
            conn.rpush(workspaceKeyName, workData)

        # 返回应答
        return JsonResponse({'res': 2})

#/PDS/editpdsversion/pdsversion_id 编辑版本
class EditPdsVersionView(View):
    def get(self, request, project_id, pdsversion_id):
        # 获取用户id
        user = request.user
        conn = get_redis_connection('default')
        workspaceKeyName = 'workspace_%s' % user.id
        # 清空Redis原来数据
        conn.delete(workspaceKeyName)
        # 初始化数据,建立空数据
        project = Projects.objects.get(project_id=project_id)
        project_di = project.to_dict()
        project_di.update({'user':project.user.username})
        # 把project_di写入Redis数据库，作为[0]
        conn.rpush(workspaceKeyName, str(project_di))
        # 新建模式
        if pdsversion_id == 'new':
            return redirect(reverse('PDS:editpage'))

        # 获取全部组，屏风数据，并写入Redis数据库,如果是lAST模式，就选择最后版本
        if pdsversion_id == 'last':
            pdsversion = PdsVersion.objects.filter(project=project_id).latest('create_time')
            pdsversion_id = pdsversion.id
        else:
            pdsversion = PdsVersion.objects.get(id=pdsversion_id)

        #编辑模式
        panelsets = Panelsets.objects.filter(pdsversion=pdsversion).values()
        # 获取组数据
        for set_di in panelsets:
            # 修改时间格式
            set_di.update({key:value.strftime('%Y-%m-%d') for key,value in set_di.items() if key =='production_time'})

            panels = list(Panels.objects.filter(panelset=set_di.get('id')).values())
            # 初始化们门数量
            ipd_qu = 0
            for tmp in panels:
                pictype = PicsModels.objects.get(id=tmp.get('panel_pic_id')).pictype
                tmp.update({'pictype':pictype})
                if pictype == 4 or pictype == 5:
                    ipd_qu += 1
                
                # 删除无用字段
                for i in ['id','panelset_id', 'create_time', 'update_time','is_delete']:
                    tmp.pop(i)

            # 删除无用字段
            for i in ['id','pdsversion_id', 'create_time', 'update_time','is_delete']:
                set_di.pop(i)

            # 生成Redis数据
            set_di.update({'panel_li':panels,'ipd_qu':ipd_qu})
            # 数据转换成Redis   
            workData = str(set_di)
            conn.rpush(workspaceKeyName, workData) 

        # 添加浏览记录(查看版本及打印)
        history_key = 'history_%d' % user.id
        # 移除
        conn.lrem(history_key, 0, pdsversion_id)
        # 插入
        conn.lpush(history_key, pdsversion_id)
        # 只保存20条
        conn.ltrim(history_key, 0 ,19)

        return redirect(reverse('PDS:editpage'))
