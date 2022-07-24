import json
from tqdm import tqdm
def mkdir():
    ls = []
    for i in range(2016, 2022):
        for j in range(1, 13):
            for k in range(1, 32):
                dir = "./" + "/".join([str(i), str(j), str(k)]) + "/articles"
                try:
                    file = open(dir, "r", encoding="utf-8")
                    ls.append(dir)
                    file.close()
                except OSError:
                    pass
                # print(dir)
                # return
    file = open("./dir.txt", "w", encoding="utf-8")
    for dir in ls:
        file.write(dir + "\n")
    file.close()

def statistic():
    count = 0
    file = open("dir.txt", "r", encoding="utf-8")
    line = file.readline()
    while line:
        article = open(line.strip(), "r", encoding="utf-8")
        a = json.load(article)
        count += a["number"]
        line = file.readline()
    print(count)
    
def link():
    file = open("dict.json", "r", encoding="utf-8")
    words = json.load(file)
    wordToSpan = {}
    file.close()
    file = open("dir.txt", "r", encoding="utf-8")
    dirs = []
    line = file.readline()
    while line:
        dirs.append(line.strip())
        line = file.readline()
    for line in tqdm(dirs):
        print(line.strip())
        article = open(line.strip(), "r", encoding="utf-8")
        a = json.load(article)["articles"]
        index = 0
        removed = set()
        for article in a:
            # print(index)
            doc_count = 0
            content = article["title"] + " " + article["description"] + " " + article["content"]
            # print(content)
            ls = set()
            for word in removed:
                if words.get(word) != None:
                    words.pop(word)
            for item in words.keys():
                ls.add(item)
            # print(ls)
            for word in words.keys():
                if word not in ls:
                    continue
                if content.find(word) != -1:
                    begin = content.find(word)
                    if wordToSpan.get(word) == None:
                        wordToSpan[word] = []
                    if len(wordToSpan[word]) < 100:
                        wordToSpan[word].append((line.strip() + "_" + str(index), begin, begin + len(word)))
                        doc_count += 1
                    else:
                        ls.remove(word)
                        removed.add(word)
                    if doc_count > 9:
                        break
            if doc_count > 9:
                break
            index += 1
        
    file = open("link.json", "w", encoding="utf-8")
    json.dump(wordToSpan, file)
    # print(wordToSpan)
        
                            
if __name__ == "__main__":
    link()

