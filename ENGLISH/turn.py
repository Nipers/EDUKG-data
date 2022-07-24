
#from win32com.client import Dispatch
from rdflib import RDF, RDFS, Namespace, Graph, Literal, URIRef
import os
import time
from tqdm import tqdm

g=Graph()
THMWDICT=Namespace('http://edukg.org/knowledge/3.0/instance/english#thmwdict-E')
THMWDICT_CLASS=Namespace('http://edukg.org/knowledge/3.0/class/english#thmwdict-C')
CLS=Namespace('http://edukg.org/knowledge/3.0/class/English#main-C')
THMWDICT_PROP=Namespace('http://edukg.org/knowledge/3.0/property/english#thmwdict-P')
ID=1
PATH = 'txt_files/THMWDict/'
list_dir = os.listdir(PATH)
print(list_dir)
# print(list_dir[0])
for dir in list_dir:
    Filelist=[]
    rootDir = PATH + dir
    for root,dirs,files in os.walk(rootDir):
        for file in files:
            file_name = os.path.join(root,file)
            Filelist.append(file_name)
    for file in tqdm(Filelist):
        f_s = time.time()
        if os.path.getsize(file)==0:
            continue
        source=open(file,encoding='utf-8')
        sentences=[]
        for line in source:
            sentences.append(line.strip())    
        sentences.pop()
        entity=sentences[0]
        i=0
        l=len(sentences)
        
        f_r = time.time()
        if l<3:
            continue
        
        prop = []
        flag = 0   
        while i < l:
            if sentences[i]==entity:
                uri=THMWDICT[str(ID)]
                pos=sentences[i+1]
                ls = ["noun","verb", "adjective", "interjection", "plural noun", "conjunction", "adverb", "preposition", "pronoun", ""]
                for j in range(len(ls)):
                    if pos.startswith(ls[j]):
                        g.add(
                            (uri,
                            RDF.type,
                            THMWDICT_CLASS[str(i + j)])
                        )
                        g.add(
                            (uri,
                            RDF.type,
                            CLS['0'])
                        )
                        g.add(
                            (uri,
                            RDFS.label,
                            Literal(entity))
                        )
                        if pos != "":
                            a = pos
                        else:
                            a = "others"
                        g.add(
                            (uri,
                            THMWDICT_PROP["1"],
                            Literal(a))
                        )
                ID+=1                     
                sentences=sentences[i+2:len(sentences)]
                l=len(sentences)
                i=0
                flag=1
                continue
            ls = ["Synonyms & Antonyms of", "Synonyms & Near Synonyms for", "Synonyms for", "Words Related to", "Phrases Synonymous with","Near Antonyms for", "Antonyms for"]
            
            for index in range(len(ls)):
                if sentences[i].startswith(ls[index]):
                    flag = index + 1
                    i += 1
                    continue
            prop.append(sentences[i])
            if '' in prop:
                prop.remove('')
            if len(prop)>0:
                st=prop.pop()
                g.add(
                    (uri,
                    THMWDICT_PROP[str(flag)],
                    Literal(st))
                )
            i+=1
    g.bind('edukg_ins_english', 'http://edukg.org/knowledge/3.0/instance/english#')
    g.bind('edukg_prop_english', 'http://edukg.org/knowledge/3.0/property/english#')
    g.bind('edukg_cls_english', 'http://edukg.org/knowledge/3.0/class/english#')   
    with open('THMWDICT_' + dir[-1] +'.ttl','w') as f:
        f.write(g.serialize(format='ttl'))
print(ID)
