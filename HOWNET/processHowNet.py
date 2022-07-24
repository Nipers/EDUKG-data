from rdflib import RDF, RDFS, Namespace, Graph, Literal, URIRef

def process():
    file = open("HowNet.txt", "r", encoding="utf-8")
    g = Graph()
    CLS = Namespace("http://edukg.org/knowledge/3.0/class/Chinese#main-C")
    HOWNET = Namespace('http://edukg.org/knowledge/3.0/instance/Chinese#hownet-E')
    HOWNET_CLASS = Namespace('http://edukg.org/knowledge/3.0/class/Chinese#hownet-C')
    HOWNET_PROP = Namespace('http://edukg.org/knowledge/3.0/property/Chinese#hownet-P')
    line = file.readline().replace("\n", "")
    index = 0
    c = ''
    while len(line.strip()) != 0:
        index += 1
        ls = []
        ls.append(line.strip().split("=")[1])
        for i in range(10):            
            line = file.readline()
            ls.append(line.strip().split("=")[1])
        line = file.readline()
        line = file.readline()
        entity_id = int(ls[0])
        if c == '':
            c = ls[6][8]
        
        for i in range(10): 
            ls[i] = ls[i].replace(c, " ")
        uri = HOWNET[str(entity_id)]
        g.add(
            (uri,
            RDF.type,
            HOWNET_CLASS['1'])
        )
        g.add(
            (uri,
            RDF.type,
            CLS['1'])
        )
        for i in range(1, len(ls)):
            if ls[i] != "":
                g.add(
                    (uri,
                    HOWNET_PROP[str(i)],
                    Literal(ls[i]) )
                )
        # if index > 10:
        #     break
        print(index)
    with open('HowNet.ttl', 'w') as f:
        f.write(g.serialize(format='ttl'))

g = Graph()
g.parse("HowNet.ttl", format="ttl")
print(len(g))
