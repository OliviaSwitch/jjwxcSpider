# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup

def get_all_list(url):
    r = requests.get(url)
    r.encoding = 'GBK'
    soup = BeautifulSoup(r.text,'html.parser')
    table = soup.select("table")
    ser_and_nov_fir = []
    for i in table:
        the_class = i.get("class")
        try:
            if the_class[1] == 'series':
                ser_and_nov_fir.append([0, i])
            elif the_class[1] == 'novel':
                ser_and_nov_fir.append([1, i])
        except:
            pass
    #print(ser_and_nov_fir)
    ser_and_nov_sec = []
    for i in ser_and_nov_fir:
        if not i[0]:
            ser_and_nov_sec.append([0, i[1].get_text(strip=True)])
            #print(i)
        else:
            #i[1]
            a = i[1].select('a')[0]
            novelid = a.get("href")[7:]
            name = a.get_text(strip=True)
            tr = i[1].select('td')[1:]
            dic = {}
            for td in tr:
                td_str = td.get_text(strip=True)
                if td_str[:2] == "类型":
                    type_ = td_str[3:].split("-")
                elif td_str[:2] == "进度":
                    ing = td_str[3:]
                elif td_str[:2] == "字数":
                    num = td_str[3:]
                elif td_str[:2] == "积分":
                    integral = td_str[3:]
                elif td_str[:2] == "收藏":
                    collect = "".join(td_str[3:].split(","))
            dic["novelid"] = novelid
            dic["书名"] = name
            dic["类型"] = type_
            dic["进度"] = ing
            dic["字数"] = int(num)
            dic["积分"] = integral
            dic["收藏"] = int(collect)
            ser_and_nov_sec.append([1, dic])
    #print(ser_and_nov_sec)
    return ser_and_nov_sec

if __name__ == "__main__":
    print("本程序用于获取某个作者的所有作品。")
    #author_id = "38144"
    author_id = input("请输入专栏id:")
    url = "https://m.jjwxc.net/wapauthor/" + author_id
    all_list = get_all_list(url)
    #is_all = int(input("是否需要作者的所有小说id？（需要输入“1”，需要额外筛选的输入“0”）"))
    is_all = 1
    if is_all:
        novelid = []
        for a_id in all_list:
            if a_id[0]:
                novelid.append(a_id[1]['novelid'])
        print(novelid)
    elif not is_all:
        select = input("请输入筛选选项（“作者自分类”、“类型”、“进度”、“字数”、“收藏”中选择输入，如需多个请在中间加入半角逗号“,”）：")
        selects = select.split(",")
        if len(selects) >= 2:
            UorN = input("交集请输入“1”，并集请输入“0”")
        i = 0
        for j in selects:
            eval("select_" + str(i)) = select()
    else:
        print("请输入“0”或“1”。")