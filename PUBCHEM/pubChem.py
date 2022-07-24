import os
import re
import json


ROOT1_DES = '/home/lxy/chemistry/pubChem/descriptor/compound/'
ROOT1_COM = '/home/lxy/chemistry/pubChem/compound/general/'
ROOT2_DES = '/home/lxy/chemistry/pubChem/descriptor/compound/'
ROOT2_COM = '/home/lxy/chemistry/pubChem/compound/general/'

if __name__ == '__main__':
    files_com = os.listdir(ROOT2_COM)
    files_des = os.listdir(ROOT2_DES)

    lineCount = 0
    entCount = 0
    prop_idxs = 8
    properties = {}

    for file in files_com:
        print('parsing file {}...'.format(file))
        print('current triple numbers: {}'.format(lineCount))
        if file.startswith('pc_compound2component'):
            f = open(f'{ROOT1_COM}{file}', 'r')
            tar_f = open(f'./compound/{file}', 'w')
            tar_f.write('@prefix compound:	<http://edukg.org/knowledge/3.0/entity/ext/pubChem/compound#> .\n')
            tar_f.write('@prefix descriptor:	<http://edukg.org/knowledge/3.0/entity/ext/pubChem/descriptor#> .\n')
            tar_f.write('@prefix eduox:	<http://edukg.org/knowledge/3.0/ontology/obj_property/ext#> .\n')
            line = f.readline()
            while line:
                if not line.startswith('@'):
                    line = line.replace('sio:CHEMINF_000480', 'eduox:P7')
                    tar_f.write(line)
                    lineCount += 1
                    entCount = max(int(re.search(r'(?<!CID)[0-9]\S*', line).group(0)), entCount)

                line = f.readline()

            f.close()
            tar_f.close()

        if file.startswith('pc_compound2descriptor'):
            f = open(f'{ROOT2_COM}{file}', 'r')
            tar_f = open(f'./compound/{file}', 'w')
            # j = json.dumps(properties)
            # with open('./pubChemProp.json', 'w') as js_file:
            #     json.dump(j, js_file)
            line = f.readline()
            while line:
                if line.startswith('@prefix'):
                    if line.startswith('@prefix compound'):
                        line = line.replace(
                            'http://rdf.ncbi.nlm.nih.gov/pubchem/compound/',
                            'http://edukg.org/knowledge/3.0/entity/ext/pubChem/compound#'
                        )
                        tar_f.write(line)

                    elif line.startswith('@prefix descriptor'):
                        line = line.replace(
                            'http://rdf.ncbi.nlm.nih.gov/pubchem/descriptor/',
                            'http://edukg.org/knowledge/3.0/entity/ext/pubChem/descriptor#'
                        )
                        tar_f.write(line)

                    elif line.startswith('@prefix sio'):
                        line = line.replace(
                            'sio:	<http://semanticscience.org/resource/>',
                            'eduox:	<http://edukg.org/knowledge/3.0/ontology/obj_property/ext#>'
                        )
                        tar_f.write(line)
                else:
                    lineCount += 1
                    if line.find("sio") != -1:
                        if re.search(r'sio:CHEMINF_\d*', line) != None:
                            pred = re.search(r'sio:CHEMINF_\d*', line).group(0)
                            if pred not in properties.keys():
                                properties[pred] = f'P{prop_idxs}'
                                prop_idxs += 1
                            line = line.replace(pred, properties[pred])
                        elif line.find("sio:has-attribute") == -1:
                            print(line)
                        else:
                            line = line.replace("sio:has-attribute", "P10000000")
                    tar_f.write(line)
                line = f.readline()

            f.close()
            tar_f.close()

    for file in files_des:
        print('parsing file {}...'.format(file))
        print('current triple numbers: {}'.format(lineCount))
        j = json.dumps(properties)
        with open('./pubChemProp.json', 'w') as js_file:
            json.dump(j, js_file)
        if 'type' in file:
            f = open(f'{ROOT2_DES}{file}', 'r')
            tar_f = open(f'./descriptor/{file}', 'w')
            tar_f.write('@prefix rdf:	<http://www.w3.org/1999/02/22-rdf-syntax-ns#> .')
            tar_f.write('@prefix descriptor:	<http://edukg.org/knowledge/3.0/entity/ext/pubChem/descriptor#> .\n')
            tar_f.write('@prefix eduox:	<http://edukg.org/knowledge/3.0/ontology/obj_property/ext#> .\n')
            line = f.readline()
            while line:
                if not line.startswith('@prefix'):
                    pred = re.search(r'sio:CHEMINF_\d*', line).group(0)
                    if pred not in properties.keys():
                        properties[pred] = f'P{prop_idxs}'
                        prop_idxs += 1
                    line = line.replace(pred, properties[pred])
                    tar_f.write(line)
                    lineCount += 1
                line = f.readline()

            f.close()
            tar_f.close()

        else:
            f = open(f'{ROOT1_DES}{file}', 'r')
            line = f.readline()
            while line:
                lineCount += 1
                line = f.readline()

            f.close()

    print(lineCount, entCount)


