import imp
import json
import jsonlines
import mysql.connector
import scipy as sp
import xlrd
import csv
import ast
import time
import os
from translate import translate
from time import sleep
from datetime import datetime
from xlrd import xldate_as_datetime
import re



db = mysql.connector.connect(
    host="localhost",       # 数据库主机地址
    user="debian-sys-maint",    # 数据库用户名
    passwd="A8XHtsF7BmWUauMw",   # 数据库密码
)
cursor = db.cursor()
cursor.execute("DROP DATABASE IF EXISTS `population_6`;")
cursor.execute("CREATE DATABASE IF NOT EXISTS `population_6`;")

originFields = {  
    "Cls" : -1,
    "Year" : -1,
    "Property" : -1,
    "Value": -1,
    "Unit": -1   
}
indexes = {  
    "Cls" : set(),
    "Property": set()
}
db = mysql.connector.connect(
    host="localhost",       # 数据库主机地址
    user="debian-sys-maint",    # 数据库用户名
    passwd="A8XHtsF7BmWUauMw",   # 数据库密码
    database="population_6"
)
cursor = db.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS `data` \
    (   \
        `ID` INT AUTO_INCREMENT PRIMARY KEY,\
        `Cls` VARCHAR(100) NOT NULL,\
        `Year`  SMALLINT NOT NULL,\
        `Property` VARCHAR(100) NOT NULL,\
        `Value` FLOAT,\
        `Unit` VARCHAR(50),\
        `Source` VARCHAR(50)\
    )ENGINE=InnoDB  DEFAULT CHARSET=utf8 ;")
# print(mycursor)

 
# mycursor.execute("SHOW TABLES")
# for x in mycursor:
#   print(x)
def replace(s):
    s = s.replace(" ", "")
    ls = ["、", "，"]
    # begin = {"一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "_", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."}
    pattern = re.compile(r"[一二三四五六七八九十、\d\.]*")
    # for i in ls:
    #     s = s.replace(i, "_")
    # print(s)
    if len(s) == 0:
        return s
    no = {"-","岁", "小", "川", "年", "人", "代", "元"}
    
    span = re.search(pattern, s).span()
    # print(span)
    if span[1] == len(s) or s[span[1]] in no or span[0] != 0:
        return s
    else:
        return s[span[1]:]
    # while s[0] in begin:
    #     s = s[1:]
    #     if len(s) == 0:
    #         return s
        
    # return s
def loadXLSfile(fileNames, cnt=0):
    begin = time.time()
    year = 2000
    ls = []
    fields = ["Cls", "Year", "Property", "Value", "Unit", "Source"]
    for filename in fileNames:
        print(filename)
        book = xlrd.open_workbook(filename="./population/6/" + filename, formatting_info=True)
        name = book.sheet_names()[0]
        sheet = book.sheet_by_name(name)
        row = sheet.nrows
        column = sheet.ncols
        name = sheet.cell_value(0, 0)
        propertys = []
        b = 0
        for i in range(row):
            xfx = sheet.cell_xf_index(i, 0)
            xf = book.xf_list[xfx]
            if xf.background.pattern_colour_index == 44:
                propertys.append(i)
        b = propertys[-1] + 1
            # print(xf.background.pattern_colour_index)
        columnContent = []
        
        for r in propertys:
            columnContent.append([])
            # DIFF
            before = ""
            for c in range(1, column):
                # print(r)
                # print(c)
                # DIFF
                # before = ""
                if sheet.cell_value(r, c) != "":
                    # print(r, c)
                    # print(sheet.cell_value(r, c))
                    if sheet.cell(r, c).ctype == 3:
                        date =  xldate_as_datetime(sheet.cell_value(r, c), 0)
                        before = date.strftime('%Y/%m/%d')
                    else:
                        before = sheet.cell_value(r, c).replace(" ", "")
                columnContent[r - propertys[0]].append(before)
        columns = {}
        rows = {}
        print(str(propertys))
        for c in range(len(columnContent[0])):
            s = ""
            for r in range(len(columnContent)):
                if columnContent[r][c] != "":
                    s += columnContent[r][c]
                    # DIFF
                    # s += "_"
            # columns[replace(s[:-1])] = c + 1
            columns[replace(s)] = c + 1
        # print(str(columns))
        before = ""
        for r in range(b, row):
            if replace(str(sheet.cell_value(r, 0))) != "":
                if replace(str(sheet.cell_value(r, 0))) == "男":
                    before = "男"
                if replace(str(sheet.cell_value(r, 0))) == "女":
                    before = "女"
                s = replace(str(sheet.cell_value(r, 0))) + before
                if s == "男男" or s == "女女":
                    s = s[:-1]
                s = s.replace(".0", "")
                rows[s] = r
        
        # print(str(rows))
        for key1 in rows.keys():
            for key2 in columns.keys():
                if key2.replace("\n", "") == "":
                    continue
                value = sheet.cell_value(rows[key1], columns[key2])
                if sheet.cell(rows[key1], columns[key2]).ctype < 2:
                    value = 0
                if value == "":
                    value = 0
                unit = "人数"
                if name.find("户数") != -1:
                    unit = "户数"
                if key2.find("性别比") != -1:
                    unit = "比例"
                if key2.find("户数") != -1:
                    unit = "户数"
                ls.append([key1, str(year), key2.replace("\n", ""), value, unit, filename])
    length = len(ls)
    cnt += length
    for item in ls:
        for i in range(len(fields)):
            if fields[i] != "Value" and indexes.get(fields[i]) != None:
                indexes[fields[i]].add(item[i])
    for i in range(int(length / 100000) + 1):
        insertData(ls = ls[i * 100000: min((i + 1) * 100000, length)], fields=fields)
    select()
    end = time.time()
    print("Finish loading {} in {} sec".format(fileNames[0], str(end - begin)))
            

def loadCSVfile(filename, originfields, cnt):# For FAOSTAT
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
                # if i > 5:
                #     break
            i += 1  
    
    keys = list(fields.keys())
    for item in datas:
        for i in range(len(keys)):
            if keys[i] != "Value" and indexes.get(keys[i]) != None:
                indexes[keys[i]].add(item[i])
    length = len(datas)
    # print(str(fields.keys()))
    # print(item)
    cnt += length
    for i in range(int(length / 100000) + 1):
        insertData(ls = datas[i * 100000: min((i + 1) * 100000, length)], fields=fields, name = table_name)
    link(table_name)
    
    end = time.time()
    print("Finish loading and linking {} in {} sec".format(filename, str(end - begin)))
    return cnt # return indexes

def insertData(ls, fields, name = "data"):
    # print(ls[72114])
    # file = open("insert.txt", "w")
    begin = time.time()
    f = ""
    v = ""
    for key in fields:
        f += key
        f += ", "
        v += "%s, "
    f = f[:-2]
    v = v[:-2]
    # print(f)
    # print(f)
    # print(v)
    sql = "INSERT INTO {} ({}) VALUES ({})".format(name, f, v)
    # print(sql)
    # print(ls)
    # print(sql)
    # for i in ls:
    #     print(i)
    #     cursor.execute(sql, i)
    cursor.executemany(sql, ls)
    db.commit()
    insert_finish = time.time()
    print("{}条记录插入成功, 用时{}秒。".format(str(cursor.rowcount), str(insert_finish - begin)))

def select(order = "SELECT * FROM data", output = "searched.txt"):
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
    print("{}条记录查询成功, 用时{}秒。".format(str(i), str(end - begin)))

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
    for field in fs:
        file = open("./links/{}.jsonl".format(field), "r", encoding="utf-8")
        line = file.readline()
        links = ast.literal_eval(line)
        ls = []
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
                    for item in links[key][0:1]:
                        ls.append((dataid, key, item))
                line = file.readline()
    # file = open("links.txt", "w", encoding="utf-8")
    # for i in ls:
    #     file.write(str(i) + "\n")
    length = len(ls)
    print(length)
    for i in range(int(length / 100000) + 1):
        insertData(ls[i * 100000: min((i + 1) * 100000, length)], f, tablename)
    # select("select * from {}".format(tablename))
    

def main():
    begin = time.time()
    cnt = 0
    # print(len(os.listdir("./csv")))    
    print(len(os.listdir("./population/6")))
    loadXLSfile(os.listdir("./population/6"))
    output = jsonlines.open("indexes.jsonl", "w")
    for key in indexes:
        jsonlines.Writer.write(output, {key: list(indexes[key])})
    output.close()
    print(cnt)
    end = time.time()
    print("Finish population_6 in {} sec".format(str(end - begin)))
    # select()
    return
    
main()
