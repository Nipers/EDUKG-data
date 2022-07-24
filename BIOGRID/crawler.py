import requests
def crawl():
    url = "https://thebiogrid.org/"
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }
    # page = requests.Session().get(url, headers=header)
    # text = page.text
    # length = len("meta name=\"description\" content=\"")
    # loc1 = text.find("meta name=\"description\" content=\"")
    # loc2 = text.find("\"", loc1 + length)
    # print(text[loc1 + length:loc2])
    file = open("ID.txt", "r")
    desc = open("desc.txt", "w")
    process = open("process.txt", "w")
    function = open("function.txt", "w")
    component = open("component.txt", "w")
    linkfile = open("linkouts.txt", "w")
    line = file.readline().replace("\n", "")
    print(line)
    i = 0
    session = requests.Session()
    while line:
        page = session.get(url + line + "/", headers=header)
        text = page.text
        length = len("meta name=\"description\" content=\"")
        loc1 = text.find("meta name=\"description\" content=\"")
        loc2 = text.find("\"", loc1 + length)
        desc.write(line + ": " + text[loc1 + length:loc2] + "\n")
        loc1 = text.find("GO Process")
        loc2 = text.find("(", loc1)
        loc3 = text.find(")", loc2)
        num1 = int(text[loc2 + 1: loc3])
        loc1 = text.find("GO Function")
        loc2 = text.find("(", loc1)
        loc3 = text.find(")", loc2)
        num2 = int(text[loc2 + 1: loc3])
        loc1 = text.find("GO Component")
        loc2 = text.find("(", loc1)
        loc3 = text.find(")", loc2)
        num3 = int(text[loc2 + 1: loc3])
        links = []
        if num1 + num2 + num3 != 0:
            loc1 = text.find("http://amigo.geneontology.org/amigo/term/")
            while loc1 != -1:
                loc2 = text.find("\' ", loc1)
                links.append(text[loc1:loc2])
                loc1 = text.find("http://amigo.geneontology.org/amigo/term/", loc2)
        ProcessLink = links[0:num1]
        FunctionLink = links[num1: num1 + num2]
        ComponentLink = links[num1 + num2: num1 + num2 + num3]
        if num1 > 0:
            process.write(line + ": " + str(ProcessLink) + "\n")
        if num2 > 0:
            function.write(line + ": " + str(FunctionLink) + "\n")
        if num3 > 0:
            component.write(line + ": " + str(ComponentLink) + "\n")
        linkouts = []
        loc1 = text.find("linkouts")
        if loc1 != -1:
            loc1 = text.find("href=", loc1)
            loc4 = text.find("<div id=\"download\"")
            while loc1 != -1 and loc1 < loc4:
                loc2 = text.find("\'", loc1)
                loc3 = text.find("\'", loc2 + 1)
                linkouts.append(text[loc2 + 1 : loc3])
                loc1 = text.find("href=", loc1 + 1)
        if len(linkouts) > 0:
            linkfile.write(line + ": " + str(linkouts) + "\n")            
        line = file.readline().replace("\n", "")
        if i % 100 == 0:
            print(i)
        i += 1
        if i > 100:
            break

crawl()