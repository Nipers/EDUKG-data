import json
import jsonlines
import jieba
file = open("zh-indexes.jsonl", "r", encoding = "utf-8")
output = jsonlines.open("seperated.jsonl", "w")
line = file.readline()
jsonlines.Writer.write(output, json.loads(line))
# print(line)
# dic = literal_eval(line)
# print(dic)
line = file.readline()
jsonlines.Writer.write(output, json.loads(line))
line = file.readline()
dic = json.loads(line)
c = {}
for key in dic:
    s = dic[key]
    ls = list(jieba.cut(s, cut_all= False))
    c[key] = ls
    print(ls)
print(type(c))
jsonlines.Writer.write(output, c)
line = file.readline()
line = file.readline()
line = file.readline()
jsonlines.Writer.write(output, json.loads(line))

