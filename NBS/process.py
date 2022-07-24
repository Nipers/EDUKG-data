from rdflib import RDF, RDFS, Namespace, Graph, Literal, URIRef
import os 
import csv
from tqdm import tqdm
def process():
    ttl_num = 0
    FAOSTAT = Namespace('http://edukg.org/knowledge/3.0/instance#ext-E')
    FAOSTAT_CLASS = Namespace('http://edukg.org/knowledge/3.0/ontology/class#ext-C')
    FAOSTAT_PROP = Namespace('http://edukg.org/knowledge/3.0/ontology/property#ext-P')

    g = os.walk("/home/lxy/NBS/data") 

    source = []
    for path,dir_list,file_list in g:  
        for file_name in file_list:
            source.append(os.path.join(path, file_name))
    print(len(source))
    print(source[0])
    prop = 62
    ctp = {}
    lines = 0
    for s in tqdm(source):
        file = open(s, "r", encoding="utf-8")
        rows = csv.reader(file)
        for row in rows:
            for c in row:
                if c not in ctp:
                    ctp[c] = prop
                    prop += 1
            break
    # file = open("property.txt", "w", encoding="utf-8")
    # for key in ctp:
    #     file.write(key +": " + str(ctp[key]) + "\n")
    # file.close()
    # print(lines)
    # ID = 2856441
    ID = 1 #Indicators_from_Household_Surveys_E_All_Data_    
    g = Graph()
    for j in tqdm(range(len(source))):
        # print(source[j])
        file = open(source[j], "rb")
        bts = file.readline()
        line = bts.decode("utf-8").replace("\n", "")
        columns = line.split(',')
        # print(columns)
        bts = file.readline()
        linels = []
        line = bts.decode("utf-8").replace("\n", "")
        while line:
            linels.append(line)
            res = False
            while not res:
                bts = file.readline()
                try:
                    line = bts.decode("utf-8").replace("\n", "")
                    res = True
                except UnicodeDecodeError:
                    continue  
        cti = {}
        for i in range(len(columns)):
            if columns[i] in ctp:
                cti[columns[i]] = i
        length = len(linels)
        for fileid in range(int(length / 4000000) + 1):
            for line in linels[fileid * 4000000: min(fileid * 4000000 + 4000000, length)]:
                # print(line)
                if line[len(line) - 1] == ',':
                    line = line[:len(line) - 1]
                if line[len(line) - 1] == '\"':
                    line = line[:len(line) - 1]
                ls = line.split(",")
                uri = FAOSTAT[str(ID)]
                ID += 1
                    
                g.add(
                    (uri,
                    RDF.type,
                    FAOSTAT_CLASS['8'])
                )
                for column in cti:
                    try: 
                        if len(str(ls[cti[column]])) > 0:
                            g.add(
                                (uri,
                                FAOSTAT_PROP[str(ctp[column])],
                                Literal(str(ls[cti[column]]))
                                )
                            )                    
                    except IndexError:
                        continue
                res = False
                while not res:
                    bts = file.readline()
                    try:
                        line = bts.decode("utf-8").replace("\n", "")
                        res = True
                    except UnicodeDecodeError:
                        continue        
    g.bind('edukg_ins_geo', 'http://edukg.org/knowledge/3.0/instance/geo#')
    g.bind('edukg_prop_geo', 'http://edukg.org/knowledge/3.0/property/geo#')
    g.bind('edukg_cls_geo', 'http://edukg.org/knowledge/3.0/class/geo#')
    print("NBS.ttl")
    ttl_num += len(g)
    with open("NBS.ttl", 'w') as f:
        f.write(g.serialize(format='ttl'))
    print(ID)  
    print(ttl_num)              

process()
    