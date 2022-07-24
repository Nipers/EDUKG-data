from itertools import count
from rdflib import Graph
from tqdm import tqdm
ls = ["THMWDICT_A.ttl", "THMWDICT_B.ttl", "THMWDICT_C.ttl", "THMWDICT_D.ttl", "THMWDICT_E.ttl", "THMWDICT_F.ttl", "THMWDICT_G.ttl", 
      "THMWDICT_H.ttl", "THMWDICT_I.ttl", "THMWDICT_J.ttl", "THMWDICT_K.ttl", "THMWDICT_L.ttl", "THMWDICT_M.ttl", "THMWDICT_N.ttl", 
      "THMWDICT_O.ttl", "THMWDICT_P.ttl", "THMWDICT_Q.ttl", "THMWDICT_R.ttl", "THMWDICT_S.ttl", "THMWDICT_T.ttl", "THMWDICT_U.ttl", 
      "THMWDICT_V.ttl", "THMWDICT_W.ttl", "THMWDICT_X.ttl", "THMWDICT_Y.ttl", "THMWDICT_Z.ttl"]
entity_count = 0
ttl_count = 0
for dir in tqdm(ls):
    g = Graph()
    g.parse(dir, format="ttl")
    ttl_count += len(g)
    output = open("toAlign.jsonl", "a", encoding="utf-8")
    for triple in g:
        # print(str(triple[1]))
        if str(triple[1]) == "http://www.w3.org/2000/01/rdf-schema#label":
            ls = {str(triple[0]):str(triple[2])}
            output.write(str(ls) + "\n")
            entity_count += 1
print(entity_count)
print(ttl_count)