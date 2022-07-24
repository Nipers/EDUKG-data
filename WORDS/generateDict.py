import csv
import json
from nltk.corpus import wordnet as wn
# words = {}
# file = open("六级词汇表.csv", "r", encoding="utf-8")
# cr = csv.reader(file)
# for row in cr:
#     if len(row) != 2:
#         print(row)    
#     if words.get(row[0]) != None:
#         print(row[0])
#     words[row[0]] = row[1]
# file.close()

# file = open("四六级单词.txt", "r", encoding="utf-8")
# cr = csv.reader(file, delimiter="\t")
# for row in cr:
#     if len(row) != 3:
#         print(row)    
#     if words.get(row[0]) != None:
#         continue
#     words[row[0]] = row[1]
# print(len(words))
# file.close()
# file = open("dict.json", "w", encoding="utf-8")
# json.dump(words, file)
# file.close()
file = open("dict.json", "r", encoding="utf-8")
words = json.load(file)
print(len(words))
wordToLemma = {}
for i in words:
    print(wn.synset(i))
    break