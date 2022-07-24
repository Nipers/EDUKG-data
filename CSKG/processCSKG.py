from binascii import Error
from cProfile import label
from itertools import count
from rdflib import RDF, RDFS, Namespace, Graph, Literal, URIRef
import csv

import sys
csv.field_size_limit(sys.maxsize)

csv.register_dialect('mydialect',delimiter='\t',quoting=csv.QUOTE_ALL)

def process():
    CSKG = Namespace('http://edukg.org/knowledge/3.0/instance/common#CSKG-E')
    CSKG_CLASS = Namespace('http://edukg.org/knowledge/3.0/class/common#CSKG-C')
    CSKG_PROP = Namespace('http://edukg.org/knowledge/3.0/property/common#CSKG-P')
    CLS = Namespace("http://edukg.org/knowledge/3.0/class/common#CSKG-C")
    ctp = {
        "node1" : 1,
        "node2" : 2,
        "relation" : 3,
        "node1_label" : 4,
        "node2_label" : 5,
        "relation_label" : 6,
        "relation_dimension" : 7,
        "source" : 8,
        "sentence" : 9
    }
    ID = 1
    CLS_ID = 1
    g = Graph()
    file = open("./cskg.tsv", "r")
    data_list = csv.reader(file, 'mydialect')
    node = {}
    property = {}
    dataSources = {}
    property_id = 1
    subGraph = Graph()
    count = 1
    for line in data_list:
        # print(count)
        if len(line) != 10:
            continue
        count += 1
        node1 = line[ctp["node1"]]
        node1_label = line[ctp["node1_label"]]
        node2 = line[ctp["node2"]]
        node2_label = line[ctp["node2_label"]]
        relation = line[ctp["relation"]]
        relation_label = line[ctp["relation_label"]]
        source = line[ctp["source"]]
        
        if dataSources.get(source) == None:
            dataSources[source] = CSKG_CLASS[str(CLS_ID)]
            CLS_ID += 1
            subGraph.add(
                (dataSources[source],
                RDFS.label,
                Literal(source))              
            )
        
        if node.get(node1) == None:
            node[node1] = CSKG[str(ID)]
            ID += 1
            g.add(
                (node[node1],
                RDF.type,
                CLS['0'])
            )
            g.add(
                (node[node1],
                RDFS.label,
                Literal(node1_label))
            )
            g.add(
                (node[node1],
                RDF.type,
                dataSources[source])
            )
        if node.get(node2) == None:
            node[node2] = CSKG[str(ID)]
            ID += 1
            g.add(
                (node[node2],
                RDF.type,
                CLS['0'])
            )
            g.add(
                (node[node2],
                RDFS.label,
                Literal(node2_label))
            )
            g.add(
                (node[node2],
                RDF.type,
                dataSources[source])
            )
        if property.get(relation) == None:
            property[relation] = CSKG_PROP[str(property_id)] 
            property_id += 1
            subGraph.add(
                (property[relation],
                RDFS.label,
                Literal(relation_label))                
            )
            
        g.add(
            (node[node1],
            property[relation],
            node[node2])
        )

    g.bind('edukg_ins_common', 'http://edukg.org/knowledge/3.0/instance/common#')
    g.bind('edukg_prop_common', 'http://edukg.org/knowledge/3.0/property/common#')
    g.bind('edukg_cls_common', 'http://edukg.org/knowledge/3.0/class/commom#')
    subGraph.bind('edukg_ins_common', 'http://edukg.org/knowledge/3.0/instance/common#')
    subGraph.bind('edukg_prop_common', 'http://edukg.org/knowledge/3.0/property/common#')
    subGraph.bind('edukg_cls_common', 'http://edukg.org/knowledge/3.0/class/commom#')
    with open("./CSKG.ttl", 'wb') as f:
        f.write(g.serialize(format='ttl'))
    print(ID)
    with open("./subGraph.ttl", 'wb') as f:
        f.write(subGraph.serialize(format='ttl'))
    
    csv.unregister_dialect('mydialect')
    print(len(node))
    print(len(dataSources))
    print(len(property))
process()
    