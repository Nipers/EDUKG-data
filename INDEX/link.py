from itertools import count
from pyparsing import line
from index.sparql_query import JenaConnector
import ast
import jsonlines
connector = JenaConnector()

def replace():
    file =  open("zh-indexes.jsonl", "r", encoding="utf-8")
    line = file.readline()
    countrys = ast.literal_eval(line)
    f = open("unlinked.txt", "r", encoding="utf-8")
    l = f.readline()
    while l:
        tp = ast.literal_eval(l)
        countrys[tp[0]] = tp[1]
        l = f.readline()
    output = open("replaced.txt", "w", encoding="utf-8")
    output.write(str(countrys))

def link(fields = ["Area", "Year", "Item", "Month", "Currency"]):
    file = open("zh-indexes.jsonl", "r", encoding="utf-8")
    line = file.readline()
    areas = ast.literal_eval(line)
    line = file.readline()
    years = ast.literal_eval(line)
    line = file.readline()
    items = ast.literal_eval(line)
    line = file.readline()
    line = file.readline()
    line = file.readline()
    months = ast.literal_eval(line)
    line = file.readline()
    line = file.readline()
    currencys = ast.literal_eval(line)
    print(len(years))
    source = [areas, years, items, months, currencys]
    result = [{} for i in range(len(fields))]
    count = 0
    unlinked = open("unlinked.txt", "w", encoding="utf-8")
    for i in range(len(source)):
        for key in source[i]:
            result[i][key] = []
            if i == 1:
                source[i][key] += "年"
            if type(source[i][key]) == type("str"):
                ls = source[i][key].split("、")
            else:
                ls = source[i][key]
            for item in ls:
                ret = connector.get_uri_by_name(item)
                if ret != None and ret[1]:
                    for l in ret[0]:
                        result[i][key].append(l)
            if len(result[i][key]) > 0:
                count += 1
            else:            
                for item in ls:
                    ret = connector.get_uri_by_name(item, base="zh", mode = "both")
                    if ret != None and ret[1]:
                        for l in ret[0]:
                            result[i][key].append(l)      
                if len(result[i][key]) > 0:
                    count += 1      
                else:
                    unlinked.write(str((key, source[i][key])) + "\n")
            # break
        output = jsonlines.open("links/{}.jsonl".format(fields[i]), "w")
        jsonlines.Writer.write(output, result[i])
    print(count)
    
link()