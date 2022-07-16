# 爬虫获取sofifa网站球员列表

import requests
from bs4 import BeautifulSoup
import sqlite3

def main():
    #main()函数
    get_players()

def get_players():
    headers = {
       'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Host':'sofifa.com'
    }#定义headers

    con = sqlite3.connect('players.db')
    print('database created')
    cursorObj = con.cursor()
    cursorObj.execute('CREATE TABLE IF NOT EXISTS players(id integer, name TEXT,club TEXT,current_ability integer,potential_ability integer)')
    con.commit()
    print('table created')

    index = 1

    infor_list = [] #初始化一个列表，信息包括当页球员名字信息和所在俱乐部信息
    player_list = [] #初始化一个列表，信息只包括球员名字信息
    club_list = [] #初始化一个列表，信息只包括球员的所在俱乐部信息
    current_ability = [] #初始化一个列表，信息包括球员的现有能力
    potential_ability = [] #初始化一个列表，信息包括球员的潜在能力

    for i in range(0,200):
        print('第'+str(i+1)+'页')
        link = 'https://sofifa.com/players?col=oa&sort=desc&offset=' + str(i*60)#一页有60个球员数据
        r = requests.get(link, headers = headers, verify=False)#利用头部信息访问sofifa

        soup = BeautifulSoup(r.text,"lxml")
        div_list_1 = soup.find_all('div',class_='ellipsis')#这个类包括了球员的姓名和所在俱乐部信息
        for each in div_list_1:
            player_infor = each.text.strip().split('\n')[0]
            infor_list.append(player_infor)#该列表存放球员及所在俱乐部信息
            
        print(infor_list)
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

        for i in range(60):
            cursorObj.execute('INSERT INTO players(id, name,club,current_ability,potential_ability) VALUES(?,?,?,?,?)',(index, player_list[i], club_list[i], current_ability[i], potential_ability[i]))
            con.commit()
            index += 1
        # time.sleep(10)#增加爬虫的时间间隔反反爬虫
        infor_list = []
        player_list = []
        club_list = []
        current_ability = []
        potential_ability = []
    
    con.close()

if __name__ == "__main__":
    main()