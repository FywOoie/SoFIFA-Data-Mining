from elasticsearch import Elasticsearch

es = Elasticsearch()#调用elasticsearch，需要后台有elasticsearch环境

f = open(".\\sofifa.txt","r")#打开生成的json格式的球员文档
for i in range(1,10):
    f.readline()#第一行对应“{”
    name='{'+f.readline().strip(',\n')+'}'#第二行字符串对应球员名字
    body=eval(name)#将球员名字行转化为字典键值对格式
    f.readline()#第三行对应俱乐部信息
    f.readline()#第四行对应现有能力
    f.readline()#第五行对应潜在能力
    f.readline()#第六行对应“}”
    es.index(index="abc",doc_type='Player',id=i,body=body)#建立索引
f.close()

#利用match_phrase完全匹配搜索
bb1={
    "query" : {
               "match_phrase" : {"Name" : "J. Oblak" }#寻找球员Oblak
                }
    }
search_result = es.search(index="abc", body=bb1)#调用search函数
#规范化输出格式
search_list = []
for item in search_result['hits']['hits']:
    #print(item['_source']['title'])
    search_list.append(item['_source']['Name'])
print(search_list)