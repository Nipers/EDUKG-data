from rdflib import RDF, RDFS, Namespace, Graph, Literal, URIRef

def process():
    g = Graph()
    ID = 0
    UNIPROT = Namespace('http://edukg.org/knowledge/3.0/entity/ext/uniprot#I')
    UNIPROT_CLASS = Namespace('http://edukg.org/knowledge/3.0/ontology/class/ext#C')
    UNIPROT_OBJ_PROP = Namespace('http://edukg.org/knowledge/3.0/ontology/obj_property/ext#P')
    UNIPROT_DATA_PROP = Namespace('http://edukg.org/knowledge/3.0/ontology/data_property/ext#P')
    file = open( "uniprot_sprot.dat", "r")
    f = open("proteins.txt", "w")
    line = file.readline().replace("\n", "")
    interactor = ""
    DT = ""
    GN = ""
    organism = ""
    encodedOn = ""
    recName = ""
    altName = ""
    taxonomicLineage =""
    taxonomy = ""
    OH = ""
    reference = []
    RP = ""
    RX = ""
    RA = ""
    RT = ""
    RL = ""
    RC = ""
    RG = ""
    DR = ""
    PE = ""
    KW = ""
    FT = ""
    SQ = ""
    while line:
        while line != "//\n":
            if line[0:2] == "AC":
                if interactor != "":
                    print("multiple AC!!!!, interactor: " + interactor)
                else:
                    interactor = line[5:len(line) - 1].split(";")[0]
                    f.write(interactor + "\n")
                    
                line = file.readline().replace("\n", "")
                # print("interactor: " + interactor)
                continue
            elif line[0:2] == "DT":
                DT = ""
                while line[0:2] == "DT":
                    DT += line[5:len(line)]
                    DT += " "
                    line = file.readline().replace("\n", "")
                # print("DT: " + DT)
                continue   
            elif line[0:2] == "DE":
                recName = ""
                altName = ""
                while line[0:2] == "DE":
                    if line.find("RecName:") != -1:
                        recName = line.replace("DE   RecName: ", "").replace(";", "")   
                        line = file.readline().replace("\n", "")
                    else:                        
                        altName += line.replace("DE   AltName: ", "").replace(";", "").replace("DE  ", "")
                        altName += " "
                        line = file.readline().replace("\n", "")
                # print("altName:" + altName)
                # print("recName:" + recName)
                continue
            elif line[0:2] == "GN":
                GN = ""
                while line[0:2] == "GN":
                    GN += line[5:len(line)]
                    line = file.readline().replace("\n", "")
                # print("GN: " + GN)
                continue
            elif line[0:2] == "OS":
                organism = line[5: len(line) - 1]
                # print("organsim: " + organism)
                line = file.readline().replace("\n", "")
                continue
            elif line[0:2] == "OC":
                taxonomicLineage = ""
                while line[0:2] == "OC":
                    taxonomicLineage += line[5:len(line)]
                    line = file.readline().replace("\n", "")
                # print("taxonomicLineage: " + taxonomicLineage)
                continue
            elif line[0:2] == "OG":
                encodedOn = ""
                while line[0:2] == "OG":
                    encodedOn += line[5:len(line)]
                    line = file.readline().replace("\n", "")
                # print("taxonomicLineage: " + taxonomicLineage)
                continue
            elif line[0:2] == "OX":
                taxonomy = line[0:len(line)-1].replace("OX   NCBI_TaxID=", "")
                # print("taxonomy: " + taxonomy)
                line = file.readline().replace("\n", "")
                continue
            elif line[0:2] == "OH":
                OH = ""
                while line[0:2] == "OH":
                    OH += line[5:len(line)]
                    OH += " ;"
                    line = file.readline().replace("\n", "")
                # print("OH: " + OH)
                continue
            elif line[0:2] == "RN":
                line = file.readline().replace("\n", "")
                reference = []
                while line[0:2] != "CC":
                    if line[0:2] == "RP":
                        RP = ""
                        while line[0:2] == "RP":
                            RP += line[5:len(line)]
                            line = file.readline().replace("\n", "")
                        # print("RP: " + RP)
                        continue
                    elif line[0:2] == "RX":
                        RX = ""
                        while line[0:2] == "RX":
                            RX += line[5:len(line)]
                            line = file.readline().replace("\n", "")
                        # print("RX: " + RX)
                        continue
                    elif line[0:2] == "RA":
                        RA = ""
                        while line[0:2] == "RA":
                            RA += line[5:len(line) - 1]
                            RA += ", "
                            line = file.readline().replace("\n", "")
                        # print("RA: " + RA)
                        continue
                    elif line[0:2] == "RT":
                        RT = ""
                        while line[0:2] == "RT":
                            RT += line[5:len(line)]
                            RT += ", "
                            line = file.readline().replace("\n", "")
                        # print("RT: " + RT)
                        continue
                    elif line[0:2] == "RL":
                        RL = ""
                        while line[0:2] == "RL":
                            RL += line[5:len(line)]
                            RL += ", "
                            line = file.readline().replace("\n", "")
                        # print("RL: " + RL)
                        continue
                    elif line[0:2] == "RG":
                        RG = ""
                        while line[0:2] == "RG":
                            RG += line[5:len(line) - 1]
                            line = file.readline().replace("\n", "")
                        # print("RG: " + RG)
                        continue                    
                    elif line[0:2] == "RC":
                        RC = ""
                        while line[0:2] == "RC":
                            RC += line[5:len(line) - 1]
                            line = file.readline().replace("\n", "")
                        # print("RG: " + RG)
                        continue
                    elif line[0:2] == "RN" or line[0:2] == "CC":
                        reference.append("RP: " + RP + "RX: " + RX + "RA: " + RA + "RT: " + RT + "RL: " + RL + "RG: " + RG + "RC: " + RC)
                        if line[0:2] == "RN":
                            line = file.readline().replace("\n", "")
                    else:
                        print(line)
                        break
                continue
            elif line[0:2] == "CC":
                while line[0:2] == "CC":
                    line = file.readline().replace("\n", "")
                    continue
                continue
            elif line[0:2] == "DR":
                DR = ""
                while line[0:2] == "DR":
                    DR += line[5:len(line)]
                    DR += " ;"
                    line = file.readline().replace("\n", "")
                # print("DR: " + DR)
                continue
            elif line[0:2] == "PE":
                PE = ""
                while line[0:2] == "PE":
                    PE += line[5:len(line)]
                    line = file.readline().replace("\n", "")
                # print("PE: " + PE)
                continue
            elif line[0:2] == "KW":
                KW = ""
                while line[0:2] == "KW":
                    KW += line[5:len(line)]
                    line = file.readline().replace("\n", "")
                # print("KW: " + KW)
                continue
            elif line[0:2] == "FT":
                FT = ""
                while line[0:2] == "FT":
                    FT += line[5:len(line)]
                    line = file.readline().replace("\n", "")
                # print("FT: " + FT)
                continue
            elif line[0:2] == "SQ":
                SQ = ""
                while line[0:2] != "//":
                    SQ += line[3: len(line)]
                    line = file.readline().replace("\n", "")
                # print("SQ: " + SQ)
                continue
            elif line[0:2] == "ID":
                line = file.readline().replace("\n", "")
                continue
            else:
                # print(line)
                break
        uri = UNIPROT[str(ID)]
        ID += 1
        g.add(
            (uri,
            RDF.type,
            UNIPROT_CLASS['7'])
        )
        # 1 means protein
        if DT != "":
            g.add(
                (uri,
                UNIPROT_DATA_PROP["30"],
                Literal(DT))
            )
        if recName != "":
            g.add(
                (uri,
                RDFS.label,
                Literal(recName))
            )
        if altName != "":
            g.add(
                (uri,
                UNIPROT_DATA_PROP["31"],
                Literal(altName))
            )
        if GN != "":
            g.add(
                (uri,
                UNIPROT_DATA_PROP["32"],
                Literal(GN))
            )
        if organism != "":
            g.add(
                (uri,
                UNIPROT_DATA_PROP["33"],
                Literal(organism))
            )
        if taxonomicLineage != "":
            g.add(
                (uri,
                UNIPROT_DATA_PROP["34"],
                Literal(taxonomicLineage))
            )
        
        if taxonomy != "":
            g.add(
                (uri,
                UNIPROT_DATA_PROP["35"],
                Literal(taxonomy))
            )
        if OH != "":
            g.add(
                (uri,
                UNIPROT_DATA_PROP["36"],
                Literal(OH))
            )
        if len(reference) != 0:
            g.add(
                (uri,
                UNIPROT_DATA_PROP["37"],
                Literal(str(reference)))
            )
        if DR != "":
            g.add(
                (uri,
                UNIPROT_DATA_PROP["38"],
                Literal(DR))
            )
        if PE != "":
            g.add(
                (uri,
                UNIPROT_DATA_PROP["39"],
                Literal(PE))
            )
        if KW != "":
            g.add(
                (uri,
                UNIPROT_DATA_PROP["40"],
                Literal(KW))
            )
        if FT != "":
            g.add(
                (uri,
                UNIPROT_DATA_PROP["41"],
                Literal(FT))
            )
        if SQ != "":
            g.add(
                (uri,
                UNIPROT_DATA_PROP["42"],
                Literal(SQ))
            )
        if encodedOn != "":
            g.add(
                (uri,
                UNIPROT_DATA_PROP["43"],
                Literal(encodedOn))
            )
        if interactor != "":
            g.add(
                (uri,
                UNIPROT_DATA_PROP["29"],
                Literal(interactor))
            )
        # if x > 10:
        #     break
        interactor = ""
        print(ID)
        if line[0:2] != "//":
            print(interactor)
            print(line)
            break
        line = file.readline().replace("\n", "")
    
    g.bind('edukg_ins_biology', 'http://edukg.org/knowledge/3.0/instance/biology#')
    g.bind('edukg_prop_biology', 'http://edukg.org/knowledge/3.0/property/biology#')
    g.bind('edukg_cls_biology', 'http://edukg.org/knowledge/3.0/class/biology#')
    print("ttl数量为 " + str(len(g)))
    with open('uniprot.ttl', 'w') as f:
        f.write(g.serialize(format='ttl'))

process()
# 565928