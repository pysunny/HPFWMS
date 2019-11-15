text = "1,4,7,10~20"
panel_no = str(text).split(",")
# print(panel_no)
for i in panel_no:
    if "~" in i:
        print(i)
        tmp = str(i).split("~")
        print(tmp)
        for i1,i2 in tmp:
            # j = range(i1,i2)
            print(i1)
            print(i2)

  
