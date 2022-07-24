from rdflib import RDF, RDFS, Namespace, Graph, Literal, URIRef
import json
def process():
    ttl_num = 0
    FAOSTAT = Namespace('http://edukg.org/knowledge/3.0/entity/ext/faostat#I')
    FAOSTAT_CLASS = Namespace('http://edukg.org/knowledge/3.0/ontology/class/ext#C')
    FAOSTAT_DATA_PROP = Namespace('http://edukg.org/knowledge/3.0/ontology/data_property/ext#P')
    readfile = [
                'Trade_Crops_Livestock_E_All_Data_(Normalized).csv',# 18528755
                'Trade_DetailedTradeMatrix_E_All_Data_(Normalized).csv',# 39473953
                'Trade_Indices_E_All_Data_(Normalized).csv',# 13787336
                'Value_of_Production_E_All_Data_(Normalized).csv',# 3213519
                'ConsumerPriceIndices_E_All_Data_(Normalized).csv', # 171841
                'Employment_Indicators_E_All_Data_(Normalized).csv',# 38997
                'Exchange_rate_E_All_Data_(Normalized).csv',# 10336
                'Investment_CapitalStock_E_All_Data_(Normalized).csv',# 130579
                'Investment_CountryInvestmentStatisticsProfile_E_All_Data_(Normalized).csv',
                'Investment_CreditAgriculture_E_All_Data_(Normalized).csv',# 65994
                'Investment_ForeignDirectInvestment_E_All_Data_(Normalized).csv',# 28937
                'Investment_GovernmentExpenditure_E_All_Data_(Normalized).csv',# 77430
                'Macro-Statistics_Key_Indicators_E_All_Data_(Normalized).csv']# 660662
    writefile = [
                "Trade_Crops_livestock",
                "Trade_Detailed_Trade_Matrix",
                "Trade_Indices",
                "Value_of_Production",
                "ConsumerPriceIndices", "Employment_Indicators", "Exchange_rate", "Investment_CapitalStock",
                 "Investment_CountryInvestmentStatisticsProfile", "Investment_CreditAgriculture", "Investment_ForeignDirectInvestment",
                 "Investment_GovernmentExpenditure", "Macro-Statistics_Key_Indicators"]
    
    ctp = {
        'Area':44,
        'Year':45,
        'Item':46,
        'Element':47,
        'Unit':48,
        'Value':49,
        'Source':50,
        'Months':51,
        'Indicator':52,
        'Currency':53,
        'Donor':54,
        'Recipient Country':55,
        'Reporter Countries':56,
        'Survey':57,
        'Breakdown Variable':58,
        'Breadown by Sex of the Household Head':59,
        'Measure':60,
        'Purpose':61,
    }
    ID = 1
    for j in range(len(readfile)):
        print(readfile[j])
        file = open(readfile[j], "rb")
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
            g = Graph()
            for line in linels[fileid * 4000000: min(fileid * 4000000 + 4000000, length)]:
                if line[len(line) - 1] == ',':
                    line = line[:len(line) - 1]
                if line[len(line) - 1] == '\"':
                    line = line[:len(line) - 1]
                line = line[1:len(line)]
                ls = line.split("\",\"")
                uri = FAOSTAT[str(ID)]
                ID += 1
                content = ""
                if cti.get("Item") != None:
                    content = ls[cti["Item"]] + ", "
                if cti.get("Element") != None:
                    content += ls[cti["Element"]] + ", "
                if cti.get("Indicator") != None:
                    content += ls[cti["Indicator"]] + ", "
                if cti.get("Currency") != None:
                    content += ls[cti["Currency"]] + ", "
                if cti.get("Survey") != None:
                    content += ls[cti["Survey"]] + ", "
                if cti.get("Measure") != None:
                    content += ls[cti["Measure"]] + ", "
                if cti.get("Purpose") != None:
                    content += ls[cti["Purpose"]] + ", "
                if cti.get("Breakdown Variable") != None:
                    content += ls[cti["Breakdown Variable"]] + ", "
                if cti.get("Breadown by Sex of the Household Head") != None:
                    content += ls[cti["Breadown by Sex of the Household Head"]] + ", "
                time = ls[cti["Year"]]
                if cti.get("Area") != None:
                    label = "{}'s {} in {}".format(ls[cti["Area"]], content, time)
                elif cti.get("Recipient Country") != None:
                    label = "{}'s {} in {}".format(ls[cti["Recipient Country"]], content, time)
                elif cti.get("Reporter Countries") != None:
                    label = "{}'s {} in {}".format(ls[cti["Reporter Countries"]], content, time)
                else:
                    label = "{} in {}".format(content, time)
                    
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
                                FAOSTAT_DATA_PROP[str(ctp[column])],
                                Literal(str(ls[cti[column]]))
                                )
                            )                    
                    except IndexError:
                        continue
                g.add(
                    (
                        uri,
                        RDFS.label,
                        Literal(label)
                    )
                )
                res = False
                while not res:
                    bts = file.readline()
                    try:
                        line = bts.decode("utf-8").replace("\n", "")
                        res = True
                    except UnicodeDecodeError:
                        continue
            g.bind('edukg_ins_politics', 'http://edukg.org/knowledge/3.0/instance/politics#')
            g.bind('edukg_prop_politics', 'http://edukg.org/knowledge/3.0/property/politics#')
            g.bind('edukg_cls_politics', 'http://edukg.org/knowledge/3.0/class/politics#')
            print("Politics/" + writefile[j] + "_" + str(fileid) + ".ttl")
            ttl_num += len(g)
            with open("Politics/" + writefile[j] + "_" + str(fileid) + ".ttl", 'w') as f:
                f.write(g.serialize(format='ttl'))
        print(ID)
    print(ttl_num)             

process()
    