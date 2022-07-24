import requests
import wget
import os
import urllib 

header = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}

def dfs(baseurl, basedir, depth):
    session = requests.Session()
    page = session.get(baseurl, headers=header)
    text = page.text
    index1 = text.find("Parent Directory</a>")
    index2 = text.find("<hr></pre>")
    l1 = text[index1:index2].split("\n")[1:-1]
    for i in range(len(l1)):
        l1[i] = l1[i].split(' ')[1]
        index1 = l1[i].find(">")
        index2 = l1[i].find("<")
        l1[i] = l1[i][index1 + 1:index2]
        print(l1[i])
    for i in l1:
        cururl = baseurl + i
        curdir = basedir + i
        if i.find("/") == -1:
            if os.path.exists(curdir):
                print(curdir + " exist")
                continue
            try:
                wget.download(cururl, out=curdir)
            except urllib.error.ContentTooShortError:
                wget.download(cururl, out=curdir)
            print()  
            print(cururl + " is downloaded at "+ curdir)
        else:
            # if i == "nbr2d/":
            #     continue
            if i == "nbr3d/":
                continue
            try:
                os.mkdir(curdir, mode=0o777)
                print("create dir   " + curdir)
            except OSError:
                print("dir  " + curdir + " exist")
            dfs(cururl, curdir, depth + 1)

def crawl():
    baseurl = "https://ftp.ncbi.nlm.nih.gov/pubchem/RDF/"
    basedir = "pubChem/"
    dfs(baseurl, basedir, 0)  
                    
        
crawl()