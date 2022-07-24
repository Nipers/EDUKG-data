from operator import le
from rdflib import RDF, RDFS, Namespace, Graph, Literal, URIRef
import json
def process():
    ttl_num = 0
    FAOSTAT = Namespace('http://edukg.org/knowledge/3.0/entity/ext/faostat#I')
    FAOSTAT_CLASS = Namespace('http://edukg.org/knowledge/3.0/ontology/class/ext#C')
    FAOSTAT_DATA_PROP = Namespace('http://edukg.org/knowledge/3.0/ontology/data_property/ext#P')
    readfile = [
                'ASTI_Expenditures_E_All_Data_(Normalized).csv',
                'ASTI_Researchers_E_All_Data_(Normalized).csv',
                'CommodityBalances_(non-food)_E_All_Data_(Normalized).csv',
                'Development_Assistance_to_Agriculture_E_All_Data_(Normalized).csv',
                'Emissions_Agriculture_Enteric_Fermentation_E_All_Data_(Normalized).csv',
                'Emissions_Agriculture_Manure_applied_to_soils_E_All_Data_(Normalized).csv',
                'Emissions_Agriculture_Manure_left_on_pasture_E_All_Data_(Normalized).csv',
                'Emissions_Agriculture_Manure_Management_E_All_Data_(Normalized).csv',
                'Emissions_Agriculture_Synthetic_Fertilizers_E_All_Data_(Normalized).csv',
                'Emissions_Totals_E_All_Data_(Normalized).csv',
                'Environment_Emissions_by_Sector_E_All_Data_(Normalized).csv',
                'Environment_Emissions_intensities_E_All_Data_(Normalized).csv',
                'Environment_Fertilizers_E_All_Data_(Normalized).csv',
                'Environment_LivestockManure_E_All_Data_(Normalized).csv',
                'Environment_LivestockPatterns_E_All_Data_(Normalized).csv',
                'Environment_Pesticides_E_All_Data_(Normalized).csv',
                'Environment_Soil_nutrient_budget_E_All_Data_(Normalized).csv',
                'Environment_Transport_E_All_Data_(Normalized).csv',
                'Food_Aid_Shipments_WFP_E_All_Data_(Normalized).csv',
                'Food_Security_Data_E_All_Data_(Normalized).csv',
                'FoodBalanceSheets_E_All_Data_(Normalized).csv',
                'FoodBalanceSheetsHistoric_E_All_Data_(Normalized).csv',
                'Forestry_E_All_Data_(Normalized).csv',
                'Forestry_Trade_Flows_E_All_Data_(Normalized).csv',
                'Indicators_from_Household_Surveys_E_All_Data_(Normalized).csv',
                'Inputs_FertilizersArchive_E_All_Data_(Normalized).csv',
                'Inputs_FertilizersNutrient_E_All_Data_(Normalized).csv',
                'Inputs_FertilizersProduct_E_All_Data_(Normalized).csv',
                'Inputs_Pesticides_Trade_E_All_Data_(Normalized).csv',
                'Inputs_Pesticides_Use_E_All_Data_(Normalized).csv',
                'Investment_Machinery_E_All_Data_(Normalized).csv',
                'Investment_MachineryArchive_E_All_Data_(Normalized).csv',
                'Prices_E_All_Data_(Normalized).csv',
                'PricesArchive_E_All_Data_(Normalized).csv',
                'Production_Indices_E_All_Data_(Normalized).csv',
                'SUA_Crops_Livestock_E_All_Data_(Normalized).csv',                
                "Deflators_E_All_Data_(Normalized).csv", 
                'Emissions_Agriculture_Burning_crop_residues_E_All_Data_(Normalized).csv',
                'Emissions_Agriculture_Crop_Residues_E_All_Data_(Normalized).csv', 
                'Emissions_Agriculture_Energy_E_All_Data_(Normalized).csv',
                'Emissions_Agriculture_Rice_Cultivation_E_All_Data_(Normalized).csv',
                'Emissions_Drained_Organic_Soils_E_All_Data_(Normalized).csv',
                'Emissions_Land_Use_Fires_E_All_Data_(Normalized).csv', 
                'Emissions_Land_Use_Forests_E_All_Data_(Normalized).csv', 
                'Environment_LandCover_E_All_Data_(Normalized).csv',
                'Environment_LandUse_E_All_Data_(Normalized).csv',
                'Environment_Temperature_change_E_All_Data_(Normalized).csv',
                'Inputs_LandUse_E_All_Data_(Normalized).csv',
                'Population_E_All_Data_(Normalized).csv', 
                'Production_Crops_Livestock_E_All_Data_(Normalized).csv' 
                ]
    writefile = [
                "ASTI_Expenditure",
                "ASTI_Researchers",
                "CommodityBalance",
                "Development_Assistance_to_Agriculture",
                "Emission_Agriculture_Enteric_Fermentation",
                "Emission_Agriculture_Manure_applied_to_soils",
                "Emission_Agriculture_Manure_left_on_pasture",
                "Emission_Agriculture_Manure_Management",
                "Emission_Agriculture_Synthetic_Fertilizers",
                "Emissions_Totals",
                "Environment_Emission_by_Sector",
                "Environment_Emission_intensities",
                "Environment_Fertilizers",
                "Environment_livestock_manure",
                "Environment_livestock_Patterns",
                "Environment_Pesticides",
                "Environment_soil_nutrient_budget",
                "Environment_Transport",
                "Food_aid_shipment",
                "Food_security_data",
                "Food_Balance",
                "Food_Balance_sheets_historic",
                "Forestry",
                "Forestry_Trade_Flows",
                "Indicator_from_household_Survey",
                "Inputs_Fertilizers_Archive",
                "Inputs_Fertilizers_Nutrient",
                "Inputs_fertilizers_Product",
                "Inputs_Pesticides_Trade",
                "Inputs_Pesticides_Use",
                "Investment_machinery",
                "Investment_Machinery_Archive",
                "Price",
                "Price_Archive",
                "Production_Indices",
                "SUA_Crops_Livestock",
                "Deflators",
                "Emissions_Agriculture_Burning_crop_residues",
                "Emissions_Agriculture_Crop_Residues", 
                "Emissions_Agriculture_Energy", 
                "Emissions_Agriculture_Rice_Cultivation",
                "Emissions_Drained_Organic_Soils",
                "Emissions_Land_Use_Fires", 
                "Emissions_Land_Use_Forests", 
                "Environment_LandCover",
                "Environment_LandUse", 
                "Environment_Temperature_change",
                "Inputs_LandUse", 
                "Population", 
                "Production_Crops_Livestock"
                ]
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
    # ID = 44159407 #Indicators_from_Household_Surveys_E_All_Data_
    for j in range(len(readfile)):
        print(readfile[j])
        file = open(readfile[j], "rb")
        bts = file.readline()
        line = bts.decode("utf-8").replace("\n", "")
        columns = line.split(',')
        print(columns)
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
                time = ""
                if cti.get("Year") != None:
                    time = ls[cti["Year"]]
                if cti.get("Months") != None:
                    if time != "":
                        time += ", "
                    time += ls[cti["Months"]]
                content = content[:-2]
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
            g.bind('edukg_ins_geo', 'http://edukg.org/knowledge/3.0/instance/geo#')
            g.bind('edukg_prop_geo', 'http://edukg.org/knowledge/3.0/property/geo#')
            g.bind('edukg_cls_geo', 'http://edukg.org/knowledge/3.0/class/geo#')
            print("Geography/" + writefile[j] + "_" + str(fileid) + ".ttl")
            ttl_num += len(g)
            with open("Geography/" + writefile[j] + "_" + str(fileid) + ".ttl", 'w') as f:
                f.write(g.serialize(format='ttl'))
        print(ID)  
        print(ttl_num)              

process()
    