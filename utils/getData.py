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


