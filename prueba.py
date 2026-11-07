from rdflib import Graph, Namespace

EX = Namespace("http://ejemplo.org/")
g = Graph()  # creas grafo vacío
g.bind("ex", EX)  # abreviamos http://ejemplo.org/ como "ex:""

g.add((EX.MSCI_World, EX.contiene, EX.Apple))
g.add((EX.SP500, EX.contiene, EX.Apple))
g.add((EX.Apple, EX.perteneceA, EX.Tecnologia))
g.add((EX.Apple, EX.tieneSedeEn, EX.EEUU))

print(g.serialize(format="turtle"))  # convertimos el grafo en memoria de texto

consulta = "SELECT ?sector WHERE { ex:Apple ex:perteneceA ?sector . }"  # las palabras con ? son variablesokay
for fila in g.query(consulta, initNs={"ex": EX}):
    print(fila.sector)