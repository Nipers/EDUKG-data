import json
import jsonlines
import mysql.connector
import csv
import ast
import time
import os
from translate import translate
from time import sleep



mydb = mysql.connector.connect(
    host="localhost",       # 数据库主机地址
    user="debian-sys-maint",    # 数据库用户名
    passwd="A8XHtsF7BmWUauMw",   # 数据库密码
)
mycursor = mydb.cursor()
mycursor.execute(
    "DROP DATABASE IF EXISTS `mysql`;"
)
mycursor.execute(
    "CREATE DATABASE IF NOT EXISTS `mysql`;"
)

db = mysql.connector.connect(
    host="localhost",       # 数据库主机地址
    user="debian-sys-maint",    # 数据库用户名
    passwd="A8XHtsF7BmWUauMw",   # 数据库密码
    database="mysql"
)
cursor = db.cursor()

originFields = {  
    "Area" : -1,
    "Year" : -1,
    "Item" : -1,
    "Element": -1,
    "Value": -1,
    "Unit": -1,
    "Months": -1,
    "Indicator": -1,
    "Currency": -1        
}
indexes = {  
    "Area" : set(),
    "Year" : set(),
    "Item" : set(),
    "Element": set(),
    "Unit": set(),
    "Months": set(),
    "Indicator": set(),
    "Currency": set()       
}
mydb = mysql.connector.connect(
    host="localhost",       # 数据库主机地址
    user="debian-sys-maint",    # 数据库用户名
    passwd="A8XHtsF7BmWUauMw",   # 数据库密码
    database="mysql"
)
# mycursor = mydb.cursor()
# mycursor.execute(
#     "DROP DATABASE IF EXISTS `mysql`;")
# mycursor.execute(
#     "CREATE TABLE IF NOT EXISTS `data` \
#     (   \
#         `ID` INT AUTO_INCREMENT PRIMARY KEY,\
#         `Area` VARCHAR(100) NOT NULL,\
#         `Year`  SMALLINT NOT NULL,\
#         `Item` VARCHAR(100) ,\
#         `Element` VARCHAR(100),\
#         `Value` FLOAT,\
#         `Unit` VARCHAR(50),\
#         `Months` VARCHAR(20),\
#         `Indicator` VARCHAR(100),\
#         `Currency` VARCHAR(50)\
#     )ENGINE=InnoDB  DEFAULT CHARSET=utf8 ;")
# print(mycursor)

 
# mycursor.execute("SHOW TABLES")
# for x in mycursor:
#   print(x)

def loadCSVfile(filename, originfields, cnt):
    begin = time.time()
    fields = originfields
    # print(filename)
    table_name = filename.replace("./csv/", "").replace("_E_All_Data_(Normalized).csv", "")
    print(table_name)
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `{}` \
        (   \
            `ID` INT AUTO_INCREMENT PRIMARY KEY,\
            `Area` VARCHAR(100) NOT NULL,\
            `Year`  SMALLINT NOT NULL,\
            `Item` VARCHAR(100),\
            `Element` VARCHAR(100),\
            `Value` FLOAT,\
            `Unit` VARCHAR(50),\
            `Months` VARCHAR(20),\
            `Indicator` VARCHAR(100),\
            `Currency` VARCHAR(50)\
        )ENGINE=InnoDB  DEFAULT CHARSET=utf8;".format(table_name))
    datas = []
    with open(filename, 'r') as csv_file:  
        all_lines = csv.reader(csv_file) 
        i = 0 
        for one_line in all_lines:  
            if i == 0:
                first_line = one_line
                for x in range(len(one_line)):
                    if fields.get(one_line[x]) != None: 
                        fields[one_line[x]] = x     
                keys = list(fields.keys())   
                for key in keys:
                    if fields[key] == -1:
                        fields.pop(key)  
            else:
                # print(one_line)
                item = []
                for key in fields:                    
                    if len(one_line[fields[key]]) != 0:
                        item.append(one_line[fields[key]])
                    else:
                        item.append(0)
                datas.append(tuple(item))
            i += 1  
    
    keys = list(fields.keys())
    for item in datas:
        for i in range(len(keys)):
            if keys[i] != "Value" and indexes.get(keys[i]) != None:
                indexes[keys[i]].add(item[i])
    length = len(datas)
    cnt += length
    for i in range(int(length / 100000) + 1):
        insertData(ls = datas[i * 100000: min((i + 1) * 100000, length)], fields=fields, name = table_name)
    link(table_name)
    
    end = time.time()
    print("Finish loading and linking {} in {} sec".format(filename, str(end - begin)))
    return cnt # return indexes

def insertData(ls, fields, name = "data"):
    begin = time.time()
    f = ""
    v = ""
    for key in fields:
        f += key
        f += ", "
        v += "%s, "
    f = f[:-2]
    v = v[:-2]
    sql = "INSERT INTO {} ({}) VALUES ({})".format(name, f, v)
    cursor.executemany(sql, ls)
    db.commit()
    insert_finish = time.time()
    # print("{}条记录插入成功, 用时{}秒。".format(str(mycursor.rowcount), str(insert_finish - begin)))

def select(order = "SELECT * FROM data where id = 42154", output = "searched.txt"):
    begin = time.time()
    i = 0
    cursor.execute(order)
    res = cursor.fetchone()
    file = open(output, "w", encoding="utf-8")
    while res:
        file.write(str(res) + "\n")
        res = cursor.fetchone()
        i += 1
    end = time.time()
    # print("{}条记录查询成功, 用时{}秒。".format(str(i), str(end - begin)))

def translate_label():    
    file = open("indexes.jsonl", "r", encoding="utf-8")
    output = jsonlines.open("zh-indexes.jsonl", "w")
    line = file.readline()
    while line:
        item = json.loads(line)
        key = list(item.keys())[0]
        # print(key)
        s = ""
        print(len(item[key]))
        if len(item[key]) == 0:
            line = file.readline()
            continue
        for x in item[key]:
            s += str(x)
            s += "\n"
        query = s[:-2]
        ls = {}
        res = translate(query=query)['trans_result']
        for i in res:
            ls[i['src']] = i['dst']
        print(len(ls))
        jsonlines.Writer.write(output, ls)
        line = file.readline()
        sleep(1)
    

def link(name = "data"):    # 将某个需要链接的field的数据和对应的链接导入数据库中
    tablename = name + "_links"
    datatolink = {}
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `{}` \
        (   \
            `ID` INT,\
            `label` VARCHAR(100) NOT NULL,\
            `URI` VARCHAR(100) NOT NULL,\
            FOREIGN KEY (ID)\
            REFERENCES {}(ID)\
        )ENGINE=InnoDB  DEFAULT CHARSET=utf8 ;".format(tablename, name))
    links = {}
    
    fs = ["Area", "Currency", "Item", "Months", "Year"]
    ls = []
    for field in fs:
        file = open("./links/{}.jsonl".format(field), "r", encoding="utf-8")
        line = file.readline()
        links = ast.literal_eval(line)
        f = ["ID", "label", "URI"]
        output = "searchresult.txt"
        for key in links:
            select("SELECT ID FROM {} WHERE {} = \"{}\"".format(name, field, key), output)
            # print(field + ": " + key)
            file = open(output, "r", encoding="utf-8")
            line = file.readline()
            if not line:
                continue
            while line:
                dataid = int(line[1:-3])
                if len(links[key]) != 0:
                    for item in links[key][0:min(3, len(links[key]))]:
                        ls.append([dataid, key, item])
                        if dataid not in datatolink:
                            datatolink[dataid] = 0
                        datatolink[dataid] += 1
                line = file.readline()
    # file = open("links.txt", "w", encoding="utf-8")
    # for i in ls:
    #     file.write(str(i) + "\n")
    file = open("datatolink.txt", "a", encoding="utf-8")
    file.write(str(datatolink) + "\n")
    file.close()
    length = len(ls)
    print(length)
    for i in range(int(length / 100000) + 1):
        insertData(ls[i * 100000: min((i + 1) * 100000, length)], f, tablename)
    
    # select("select * from {}".format(tablename))
    

def main():
    begin = time.time()
    cnt = 0
    # print(len(os.listdir("./csv")))
    for i in os.listdir("./csv"):    
        fields = originFields.copy()
        cnt = loadCSVfile(originfields = fields, filename = "./csv/" + i, cnt = cnt)
        # print(originFields)
    output = jsonlines.open("indexes.jsonl", "w")
    for key in indexes:
        jsonlines.Writer.write(output, {key: list(indexes[key])})
    output.close()
    print(cnt)
    end = time.time()
    print("Finish FAOSTAT in {} sec".format(str(end - begin)))
    # select()
    return
    

main()
