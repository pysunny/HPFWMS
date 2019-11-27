from django.core.paginator import Paginator
from django.http import JsonResponse
# 这是一个获取数据分页后的数据的函数,返回网页中需要的表格数据
class getData(object):
    def getData(self, ret, page, limit):
        # 对数据分页
        paginator = Paginator(ret, limit)
        # 获取数量
        count = paginator.count
        # 获取对应的页面的数据
        ret_page = paginator.page(page)
        json_list = []

        for tmp in ret_page:
            json_dict = tmp.to_dict()
            json_list.append(json_dict)

        # 返回layui需要的数据格式   
        context = {
            "code": 0,
            "msg": "",
            "count": count,
            "data": json_list
        }
        # 返回
        return context


# 有点复杂暂时取消
# # 这是操作数据库的类
# class perateData(object):
#     # 添加数据到表
#     def addObject(self, model, querydict, key_fields=None, exclude=None):
#         # 获取post全部数据，并生成eval字符
#         tmp_dict = querydict.dict()
#         key_list = tmp_dict.keys()
#         # 初始化eval字符
#         eval_str = ''
#         # 循环tmp_dict，一个由键值组成的元祖的列表
#         for tmp in key_list:
#             # 不要csrfmiddlewaretoken
#             if tmp == "csrfmiddlewaretoken":
#                 continue
#             # 不包含
#             if exclude and tmp in exclude:
#                 continue
#             tmp_str = str(tmp) + "= '" + str(tmp_dict[tmp]) + "',"
#             eval_str += tmp_str
        
#         print(eval_str[:-1])

#         id_name = model().get_id_name()
#         print(id_name)

#         # 以上用于处理关键数据，防止数据重复

#         key_str = ''
#         if not key_fields == None:
#             for tmp in key_fields:
#                 tmp_str = str(tmp) + "= '" + str(tmp_dict[tmp]) + "',"
#                 key_str += tmp_str
#         print(key_str[:-1])

#         try:
#             tmp_model = eval("model.objects.filter(" + key_str[:-1] + ")")
#         except:
#             tmp_model = None
        
#         if tmp_model:
#             return JsonResponse({'res': 0, 'errmsg': '此基本图元已经存在'})

#         # # 创建对象
#         try:
#             eval("model.objects.create(" + eval_str[:-1] + ")")
#             return JsonResponse({'res': 2})
#         except:
#             return  JsonResponse({'res': 1, 'errmsg': '发生错误,创建不成功'})


#     # 这是更新数据库
#     def updateObject(self, model, querydict, key_id, key_fields=None, exclude=None):
#         # 获取post全部数据，并生成eval字符
#         tmp_dict = querydict.dict()
#         key_list = tmp_dict.keys()
#         # 初始化eval字符
#         eval_str = ''
#         # 循环tmp_dict，一个由键值组成的元祖的列表
#         for tmp in key_list:
#             # 不要csrfmiddlewaretoken
#             if tmp == "csrfmiddlewaretoken":
#                 continue
#             # 去除id字符
#             if tmp == key_id:
#                 continue
#             # 不包含
#             if exclude and tmp in exclude:
#                 continue
#             tmp_str = str(tmp) + "= '" + str(tmp_dict[tmp]) + "',"
#             eval_str += tmp_str
        
#         print(eval_str[:-1])

#         # 以上用于处理关键数据，防止数据重复

#         id_name = model().get_id_name()

#         key_str = ''
#         if not key_fields == None:
#             for tmp in key_fields:
#                 tmp_str = str(tmp) + "= '" + str(tmp_dict[tmp]) + "',"
#                 key_str += tmp_str
#         print(key_str[:-1])

#         id = tmp_dict[key_id]
#         try:
#             tmp_model = eval("model.objects.filter(" + key_str[:-1] + ").exclude("+id_name +"="+id+")")
#         except:
#             tmp_model = None
        
#         if tmp_model:
#             return JsonResponse({'res': 0, 'errmsg': '此基本图元已经存在'})

#         # # 创建对象
#         try:
#             eval("model.objects.filter("+id_name+"="+id+").update("+eval_str[:-1]+")")
#             return JsonResponse({'res': 2})
#         except:
#             return  JsonResponse({'res': 1, 'errmsg': '发生错误,创建不成功'})

