from rdflib import Graph
g = Graph()
g.parse("wordnet.nt", format="nt")
index = 0
file = open("test.ttl", "w", encoding="utf-8")
file.write(g.serialize(format="ttl"))
file.close()
