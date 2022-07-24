from rdflib import RDF, RDFS, Namespace, Graph, Literal
import json

from tqdm import tqdm
file = open("dir.txt", "r", encoding="utf-8")
g = Graph()
ID = 1
NYTIMES = Namespace('http://edukg.org/knowledge/3.0/instance#ext-E')
NYTIMES_CLASS = Namespace('http://edukg.org/knowledge/3.0/ontology/class#ext-C')
NYTIMES_PROP = Namespace('http://edukg.org/knowledge/3.0/ontology/property#ext-P')
ctp = {
    'title':44,
    'published_date':45,
    'authors':46,
    'description':47,
    'section':48,
    'content':49,
    'link':50,
}
for line in tqdm(file):
    dir = line.strip()
    a = open(dir, "r", encoding="utf-8")
    articles = json.load(a)
    index = 0
    for article in articles["articles"]:
        label = dir + "_" + str(index)               
        index += 1
        uri = NYTIMES[str(ID)]
        ID += 1
        g.add(
            (
            (uri,
            RDF.type,
            NYTIMES_CLASS['1'])
            )
        )         
        g.add(
            (
                uri,
                RDFS.label,
                Literal(label)
            )
        )             
        for property in article:
            if property not in ctp:
                print(property)
                continue
            g.add(
                (
                    uri,
                    NYTIMES_PROP[str(ctp[property])],
                    Literal(str(article[property]))
                )
            )  
    # break
print("ttl数量为 " + str(len(g)))
print("实体数量为 " + str(ID))
with open('nytimes.ttl', 'wb') as f:
    f.write(g.serialize(format='ttl'))
    
