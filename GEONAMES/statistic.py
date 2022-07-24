from rdflib import Graph
from tqdm import tqdm
file = open("../index/Country2020.ttl", "r", encoding="utf-8")
entity_num = 0
triple_num = 0
index = 0
for line in tqdm(file):
    if line.find("edukg_ins_geo:Country2020-E") == 0:
        entity_num += 1
    if len(line.strip("\n").strip(" ")) != 0:
        # print(line)
        triple_num += 1
    # index += 1
    # if index > 20:
    #     break
print(entity_num)
print(triple_num)