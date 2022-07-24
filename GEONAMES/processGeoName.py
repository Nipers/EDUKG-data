from binascii import Error
from cProfile import label
from fileinput import filename
from html import entities
from itertools import count
from xml.etree.ElementTree import XML
from rdflib import RDF, RDFS, Namespace, Graph, Literal, URIRef
import re

def prefix(s1, s2):
    return s1[:len(s2) + s1.find(s2)]

class XMLProcessor():
    ctp = {}
    property = 0
    useless = {
        "?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?",
        'rdf:RDF xmlns:cc="http://creativecommons.org/ns#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:foaf="http://xmlns.com/foaf/0.1/" xmlns:gn="http://www.geonames.org/ontology#" xmlns:owl="http://www.w3.org/2002/07/owl#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" xmlns:wgs84_pos="http://www.w3.org/2003/01/geo/wgs84_pos#"',
        "gn:locationMap",
        "gn:Feature"
    }
    rule = {
        "rdfs:isDefinedBy" : ["rdfs:", "rdf:resource=\""],
        "gn:featureClass" : ["gn:", "rdf:resource=\""],
        "gn:featureCode" : ["gn:", "rdf:resource=\""],
        "gn:parentFeature" : ["gn:", 'rdf:resource="https://sws.geonames.org/'],
        "gn:parentCountry" : ["gn:", 'rdf:resource="https://sws.geonames.org/'],
        "gn:parentAMD1" : ["gn:", 'rdf:resource="https://sws.geonames.org/'],
        "gn:nearbyFeatures": ["gn:", "rdf:resource=\""],        
    }
    def process(self, xmlstr:str):
        result = {}
        splited = xmlstr.split("<")
        ls = [] 
        for i in splited:
            temp = i.split(">")
            # for j in temp:
            ls.append([])
            for j in temp:
                if j != "" and len(j.strip()) != 0:                    
                    ls[-1].append(j)
            if len(ls[-1]) == 0:
                ls.pop(-1)            
            elif ls[-1][0][0] == '/' and len(ls[-1]) == 1:
                ls.pop(-1)
        for item in ls:
            if len(item) == 1:
                # print(item)
                s = item[0]
                if s[-1] == "/":
                    s = s[:-1]
                if s in self.useless:
                    continue
                temp = s.split(" ")
                if len(temp) != 2:
                    print(s)
                    continue
                if temp[0] in self.useless:
                    continue
                elif self.rule.get(temp[0]) != None:
                    key = temp[0].replace(self.rule[temp[0]][0], "")
                    value = temp[1].replace(self.rule[temp[0]][1], "").replace("\"", "")
                    if value[-1] == "/":
                        value = value[:-1]
                    # print(key, value)
                    if self.ctp.get(key) == None:
                        self.ctp[key] = self.property
                        self.property += 1
                    if key.find("parent") != -1:
                        value = int(value)
                    result[self.ctp[key]] = value
                                
                # break
                        
                    
            elif len(item) == 2:
                # print(item)
                key = item[0].split(" ")[0].replace("gn:", "")
                value = item[1]
                # print(key, value)
                if self.ctp.get(key) == None:
                    self.ctp[key] = self.property
                    self.property += 1
                result[self.ctp[key]] = value
            else:
                print(item)
                # continue
        # print(self.ctp)
        return result
            

def process():
    geoNames = Namespace('http://edukg.org/knowledge/3.0/instance/geo#geoNames-E')
    geoNames_CLASS = Namespace('http://edukg.org/knowledge/3.0/class/geo#geoNames-C')
    geoNames_PROP = Namespace('http://edukg.org/knowledge/3.0/property/geo#geoNames-P')
    CLS = Namespace("http://edukg.org/knowledge/3.0/class/geo#main-C")
    # CLS_ID = 2
    ctp = {}
    # ID = 1
    xmlProcessor = XMLProcessor()
    # ID = 5876917
    # classes[1] = []
    g = Graph()
    filename = "./all-geonames-rdf.txt"
    file = open(filename, 'r')
    line = file.readline()  
    ls = []
    entity_count = 0
    while line:   
        entity_count += 1
        line = file.readline()  
        line = file.readline()  
        # entity_id = int(line.split("/")[-2])
        # # print(entity_id)
        # ls.append(entity_id)
        # line = file.readline()
        # uri = geoNames[str(entity_id)]
        # g.add(
        #     (uri,
        #     RDF.type,
        #     CLS['0']
        #     )
        # )
        # g.add(
        #     (uri,
        #     RDF.type,
        #     geoNames_CLASS['0']
        #     )
        # )
        # res = xmlProcessor.process(line.replace("\n", "").replace("        ", ""))
        # for key in res:
        #     if type(res[key]) == type("1"):
        #         if key != 1:
        #             g.add(
        #                 (uri,
        #                 geoNames_PROP[str(key)],
        #                 Literal(res[key])
        #                 )
        #             )    
        #         else:
        #             g.add(
        #                 (uri,
        #                 RDFS.label,
        #                 Literal(res[key])
        #                 )
        #             )                
        #     else:
        #         g.add(
        #             (uri,
        #             geoNames_PROP[str(key)],
        #             geoNames[str(res[key])]
        #             )
        #         )
        # line = file.readline()
         
                
        # break
    # with open("geoNames.ttl", 'wb') as f:
    #     f.write(g.serialize(format='ttl'))
    print(entity_count)
    g = Graph()
    g.parse("geoNames.ttl", format="ttl")
    print(len(g))
    
         
process()
    