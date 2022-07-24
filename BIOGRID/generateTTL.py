from rdflib import RDF, RDFS, Namespace, Graph, Literal, URIRef

def generate():
    source = open("BIOGRID-ALL-4.4.203.tab3.txt")
    line = source.readline()
    line = source.readline().replace("\n", "")
    i = 0
    g = Graph()
    nameToID = {}
    s = set()
    ID = 0
    BIOGRID = Namespace('http://edukg.org/knowledge/3.0/entity/ext/biogrid#I')
    BIOGRID_CLASS = Namespace('http://edukg.org/knowledge/3.0/ontology/class/ext#C')
    BIOGRID_OBJ_PROP = Namespace('http://edukg.org/knowledge/3.0/ontology/obj_property/ext#P')
    BIOGRID_DATA_PROP = Namespace('http://edukg.org/knowledge/3.0/ontology/data_property/ext#P')
    while line:
        attlist = line.split("\t")
        InteractionID = attlist[0]
        E_GeneIDA = attlist[1]
        E_GeneIDB = attlist[2]
        BioGRIDIDA = attlist[3]
        BioGRIDIDB = attlist[4]
        SystematicNameA = attlist[5]
        SystematicNameB = attlist[6]      
        OfficialSymbolA = attlist[7]
        OfficialSymbolB = attlist[8]
        SynonymsA = attlist[9]
        SynonymsB = attlist[10]
        SystemName = attlist[11]
        SystemType = attlist[12]
        Author = attlist[13]
        PublicationSource = attlist[14]
        OrganismIDA = attlist[15]
        OrganismIDB = attlist[16]
        InteractionThroughput = attlist[17]
        QuantitativeScore = attlist[18]
        PostTranslationalModification = attlist[19]
        Qualifications = attlist[20]
        Tags = attlist[21]
        SourceDatabase = attlist[22]
        InteractorA = attlist[23].split("|")[0]
        TREMBLAccessionsA = attlist[24]
        REFSEQAccessionsA = attlist[25]
        InteractorB = attlist[26].split("|")[0]
        TREMBLAccessionsB = attlist[27]
        REFSEQAccessionsB = attlist[28]
        OntologyTermIDs = attlist[29]
        OntologyTermNames = attlist[30]
        OntologyTermCategories = attlist[31]
        OntologyTermQualifierIDs = attlist[32]
        OntologyTermQualifierNames = attlist[33]
        OntologyTermTypes = attlist[34]
        OrganismNameA = attlist[35]
        OrganismNameB = attlist[36]
        
        uri1 = BIOGRID[str(ID)]
        ID += 1
        if InteractorA not in nameToID:
            nameToID[InteractorA] = ID
            ID += 1
        if InteractorB not in nameToID:
            nameToID[InteractorB] = ID
            ID += 1
        uri2 = BIOGRID[str(nameToID[InteractorA])]
        uri3 = BIOGRID[str(nameToID[InteractorB])]
        g.add(
            (uri1,
            RDF.type,
            BIOGRID_CLASS['6'])
        )
        # 1 means interaction
        g.add(
            (uri1,
            BIOGRID_OBJ_PROP["1"],
            uri2)
        )
        g.add(
            (uri1,
            BIOGRID_OBJ_PROP["1"],
            uri3)
        )
        g.add(
            (uri1,
            BIOGRID_DATA_PROP["28"],
            Literal(InteractionID))
        )
        if SystemName != "-":
            g.add(
                (uri1,
                BIOGRID_DATA_PROP["6"],
                Literal(SystemName))
            )
        if SystemType != "-":
            g.add(
                (uri1,
                BIOGRID_DATA_PROP["7"],
                Literal(SystemType))
            )
        if Author != "-":
            g.add(
                (uri1,
                BIOGRID_DATA_PROP["8"],
                Literal(Author))
            )
        if PublicationSource != "-":
            g.add(
                (uri1,
                BIOGRID_DATA_PROP["9"],
                Literal(PublicationSource))
            )
        if InteractionThroughput != "-":
            g.add(
                (uri1,
                BIOGRID_DATA_PROP["11"],
                Literal(InteractionThroughput))
            )
        if QuantitativeScore != "-":
            g.add(
                (uri1,
                BIOGRID_DATA_PROP["12"],
                Literal(QuantitativeScore))
            )
        if PostTranslationalModification != "-":
            g.add(
                (uri1,
                BIOGRID_DATA_PROP["13"],
                Literal(PostTranslationalModification))
            )
        if Qualifications != "-":
            g.add(
                (uri1,
                BIOGRID_DATA_PROP["14"],
                Literal(Qualifications))
            )
        if Tags != "-":
            g.add(
                (uri1,
                BIOGRID_DATA_PROP["15"],
                Literal(Tags))
            )
        if SourceDatabase != "-":
            g.add(
                (uri1,
                BIOGRID_DATA_PROP["16"],
                Literal(SourceDatabase))
            )
        if OntologyTermIDs != "-":
            g.add(
                (uri1,
                BIOGRID_DATA_PROP["20"],
                Literal(OntologyTermIDs))
            )
        if OntologyTermNames != "-":
            g.add(
                (uri1,
                BIOGRID_DATA_PROP["21"],
                Literal(OntologyTermNames))
            )
        if OntologyTermCategories != "-":
            g.add(
                (uri1,
                BIOGRID_DATA_PROP["22"],
                Literal(OntologyTermCategories))
            )
        if OntologyTermQualifierIDs != "-":
            g.add(
                (uri1,
                BIOGRID_DATA_PROP["23"],
                Literal(OntologyTermQualifierIDs))
            )
        if OntologyTermQualifierNames != "-":
            g.add(
                (uri1,
                BIOGRID_DATA_PROP["24"],
                Literal(OntologyTermQualifierNames))
            )
        if OntologyTermTypes != "-":
            g.add(
                (uri1,
                BIOGRID_DATA_PROP["25"],
                Literal(OntologyTermTypes))
            )
        
        if InteractorA not in s:
            g.add(
                (uri2,
                RDF.type,
                BIOGRID_CLASS['7'])
            )
            g.add(
                (uri2,
                BIOGRID_DATA_PROP["29"],
                Literal(InteractorA))
            )
            # 2 means protein
            s.add(InteractorA)
            if E_GeneIDA != "-":
                g.add(
                    (uri2,
                    BIOGRID_DATA_PROP["2"],
                    Literal(E_GeneIDA))
                )
            if SystematicNameA != "-":
                g.add(
                    (uri2,
                    BIOGRID_DATA_PROP["3"],
                    Literal(SystematicNameA))
                )
            if OfficialSymbolA != "-":
                g.add(
                    (uri2,
                    BIOGRID_DATA_PROP["4"],
                    Literal(OfficialSymbolA))
                )
            if SynonymsA != "-":
                g.add(
                    (uri2,
                    BIOGRID_DATA_PROP["5"],
                    Literal(SynonymsA))
                )
            if OrganismIDA != "-":
                g.add(
                    (uri2,
                    BIOGRID_DATA_PROP["10"],
                    Literal(OrganismIDA))
                )
            if BioGRIDIDA != "-":
                g.add(
                    (uri2,
                    BIOGRID_DATA_PROP["17"],
                    Literal(BioGRIDIDA))
                )
            if TREMBLAccessionsA != "-":
                g.add(
                    (uri2,
                    BIOGRID_DATA_PROP["18"],
                    Literal(TREMBLAccessionsA))
                )
            if REFSEQAccessionsA != "-":
                g.add(
                    (uri2,
                    BIOGRID_DATA_PROP["19"],
                    Literal(REFSEQAccessionsA))
                )
            if OrganismNameA != "-":
                g.add(
                    (uri2,
                    BIOGRID_DATA_PROP["26"],
                    Literal(OrganismNameA))
                )
        if InteractorB not in s:
            g.add(
                (uri3,
                RDF.type,
                BIOGRID_CLASS['7'])
            )
            
            
            g.add(
                (uri3,
                BIOGRID_DATA_PROP["29"],
                Literal(InteractorB))
            )
            s.add(InteractorB)
            if E_GeneIDB != "-":
                g.add(
                    (uri3,
                    BIOGRID_DATA_PROP["2"],
                    Literal(E_GeneIDB))
                )
            if SystematicNameB != "-":
                g.add(
                    (uri3,
                    BIOGRID_DATA_PROP["3"],
                    Literal(SystematicNameB))
                )
            if OfficialSymbolB != "-":
                g.add(
                    (uri3,
                    BIOGRID_DATA_PROP["4"],
                    Literal(OfficialSymbolB))
                )
            if SynonymsB != "-":
                g.add(
                    (uri3,
                    BIOGRID_DATA_PROP["5"],
                    Literal(SynonymsB))
                )
            if OrganismIDB != "-":
                g.add(
                    (uri3,
                    BIOGRID_DATA_PROP["10"],
                    Literal(OrganismIDB))
                )
            if BioGRIDIDB != "-":
                g.add(
                    (uri3,
                    BIOGRID_DATA_PROP["17"],
                    Literal(BioGRIDIDB))
                )
            if TREMBLAccessionsB != "-":
                g.add(
                    (uri3,
                    BIOGRID_DATA_PROP["18"],
                    Literal(TREMBLAccessionsB))
                )
            if REFSEQAccessionsB != "-":
                g.add(
                    (uri3,
                    BIOGRID_DATA_PROP["19"],
                    Literal(REFSEQAccessionsB))
                )
            if OrganismNameB != "-":
                g.add(
                    (uri3,
                    BIOGRID_DATA_PROP["26"],
                    Literal(OrganismNameB))
                )
        print(i)
        line = source.readline().replace("\n", "")
        i += 1
    f = open("proteins.txt", "w")
    for p in s:
        f.write(p + "\n")
    f.close()
    print("ttl数量为 " + str(len(g)))
    with open('biogrid.ttl', 'w') as f:
        f.write(g.serialize(format='ttl'))
    

generate()
# 2290513