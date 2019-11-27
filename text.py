""" 这是一个检验屏风编号，并输出屏风编号列表的类 """

# 获取request
class dataCheck(object):
    def panelNo(self, panel_no):
        panel_no = str(panel_no).split(",")
        # 建立新列表
        text_list = []
        for i in panel_no:
            # 如果有"~",就继续分拆
            try:
                if "~" in i:
                    tmp = (str(i).split("~"))
                    tmp = range(int(tmp[0]), int(tmp[1])+1)
                    # 合拼列表
                    text_list = text_list + list(tmp)
                # 如果就添加到新列表
                else:
                    text_list.append(int(i))
            except :
                return "输入有问题"
        # 把列表进行排序qa
        text_list.sort()
        # 输入结果
        return text_list


a = dataCheck()

panel_no = '1, 3~10, 20 ,12~17 '

print(a.panelNo(panel_no))

# print(list(range(1,10)))