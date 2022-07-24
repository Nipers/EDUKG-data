from binascii import Error
from cProfile import label
from fileinput import filename
from itertools import count
from rdflib import RDF, RDFS, Namespace, Graph, Literal, URIRef
import csv

def prefix(s1, s2):
    return s1[:len(s2) + s1.find(s2)]

def process():
    Country2020 = Namespace('http://edukg.org/knowledge/3.0/instance/geo#Country2020-E')
    Country2020_CLASS = Namespace('http://edukg.org/knowledge/3.0/class/geo#Country2020-C')
    Country2020_PROP = Namespace('http://edukg.org/knowledge/3.0/property/geo#Country2020-P')
    CLS = Namespace("http://edukg.org/knowledge/3.0/class/geo#main-C")
    # CLS_ID = 2
    ctp = {}
    # ctp['CLS'] = 1
    # 省1，市2，县3，乡镇4，村5
    ctp['Code'] = 1
    ctp['lng_84'] = 2
    ctp["lat_84"] = 3
    ctp["Belonger"] = 4
    ctp["cityOrCountry"] = 5
    ID = 1
    addresses = [{}, {}, {}, {}]
    
    # ID = 5876917
    # classes[1] = []
    g = Graph()
    filename = "./2020年中国行政村级区划代码及经纬度/2020年村级及以上各级行政区区划代码及经纬度.csv"
    with open(filename, 'r') as csv_file:  
        all_lines = csv.reader(csv_file) 
        i = 0 
        for one_line in all_lines:  
            if i == 0:
                i += 1
                continue
            address = one_line[10]
            
            province = prefix(address, one_line[0])
            provinceCode = one_line[2][0:2] + "0000000000"
            city = prefix(address, one_line[1])
            cityCode = one_line[2]
            county = prefix(address, one_line[3])
            countyCode = one_line[4]
            town = prefix(address, one_line[5])
            townCode = one_line[6]
            country = prefix(address, one_line[7])
            countryCode = one_line[8]
            cityOrCountry = one_line[9]
            lng_84 = one_line[11]
            lat_84 = one_line[12]
            locs = [province, city, county, town, country]
            codes = [provinceCode, cityCode, countyCode, townCode, countryCode]
            for i in range(len(locs)):
                uri = None
                if i == 4 or addresses[i].get(locs[i]) == None:
                    uri = Country2020[str(ID)]
                    ID += 1
                    print(ID)
                    if i != 4:
                        addresses[i][locs[i]] = uri
                    g.add(
                        (uri,
                        RDF.type,
                        CLS['0'])
                    )
                    g.add(
                        (uri,
                        RDF.type,
                        Country2020_CLASS[str(i + 1)])
                    )
                    g.add(
                        (
                            uri,
                            Country2020_PROP["1"],
                            Literal(codes[i])
                        )
                    )
                    g.add(
                        (
                            uri,
                            RDFS.label,
                            Literal(locs[i])
                        )
                    )
                    if i != 0:                        
                        g.add(
                            (
                                uri,
                                Country2020_PROP["4"],
                                addresses[i - 1][locs[i - 1]]
                            )
                        )
                    if i == 4:
                        g.add(
                            (uri,
                            Country2020_PROP["2"],
                            Literal(lng_84))
                        )
                        g.add(
                            (uri,
                            Country2020_PROP["3"],
                            Literal(lat_84))
                        )
                        g.add(
                            (uri,
                            Country2020_PROP["5"],
                            Literal(cityOrCountry))
                        )                        
            # break
    
        
        g.bind('edukg_ins_geo', 'http://edukg.org/knowledge/3.0/instance/geo#')
        g.bind('edukg_prop_geo', 'http://edukg.org/knowledge/3.0/property/geo#')
        g.bind('edukg_cls_geo', 'http://edukg.org/knowledge/3.0/class/geo#')
        with open("Country2020.ttl", 'wb') as f:
        # with open("Politics/" + writefile[j], 'wb') as f:
            f.write(g.serialize(format='ttl'))
         
process()
    