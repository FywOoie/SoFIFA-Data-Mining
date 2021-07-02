import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json

def main():
    #main()函数
    get_players()


def get_players():
    headers = {
       'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Host':'sofifa.com'
    }#定义headers

    infor_list = []#初始化一个列表，信息包括球员名字信息和所在俱乐部信息
    player_list = []#初始化一个列表，信息只包括球员名字信息
    club_list = []#初始化一个列表，信息只包括球员的所在俱乐部信息
    current_ability = []#初始化一个列表，信息包括球员的现有能力
    potential_ability = []#初始化一个列表，信息包括球员的潜在能力
    path_name = ".\\sofifa1.xlsx"#保存数据路径

    for i in range(0,1):
        link = 'https://sofifa.com/?col=oa&sort=desc&offset=' + str(i*60)#一页有60个球员数据
        r = requests.get(link, headers = headers, timeout = 10)#利用头部信息访问sofifa

        soup = BeautifulSoup(r.text,"lxml")
        div_list_1 = soup.find_all('div',class_='bp3-text-overflow-ellipsis')#这个类包括了球员的姓名和所在俱乐部信息
        for each in div_list_1:
            player_infor = each.text.strip()
            infor_list.append(player_infor)#该列表存放球员及所在俱乐部信息
            
        player_list = infor_list[::2]#只保存原列表奇数索引信息作为球员名字信息，因为偶数元素为前一奇数元素对应球员的所在俱乐部信息
        club_list = infor_list[1::2]#只保存原列表偶数索引信息作为球员所在俱乐部信息
    
        div_list_2 = soup.find_all('td',class_='col col-oa col-sort')#这个类包括了球员的姓名和所在俱乐部
        for each in div_list_2:
            ca = each.text.strip()
            current_ability.append(ca)#球员现有能力列表

        div_list_3 = soup.find_all('td',class_='col col-pt')#这个类包括了球员的姓名和所在俱乐部
        for each in div_list_3:
            pa = each.text.strip()
            potential_ability.append(pa)#球员潜在能力列表

        infor = zip(player_list,club_list,current_ability,potential_ability)#将获取的列表打包
        save_players(infor,path_name)#将爬取数据保存到相应文件夹
        time.sleep(10)#增加爬虫的时间间隔反反爬虫
        
    return infor

def save_players(list,path_name):
    dataframe = pd.DataFrame(list,columns=['Name','Club','Current Ability','Potential Ability'])
    dataframe.to_excel(path_name,index=False)#将list保存到excel中

if __name__ == "__main__":
    main()