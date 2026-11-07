import csv
from rdflib import Graph, Namespace, Literal, RDF, RDFS, XSD
from owlrl import DeductiveClosure, RDFS_Semantics

EX = Namespace("http://ejemplo.org/")

g = Graph()
g.bind("ex", EX)
g.parse("ontologia.ttl")
tripletas_ontologia = len(g)

NOMBRES_PAIS = {
    "US": "Estados Unidos",
    "NL": "Países Bajos",
    "GB": "Reino Unido",
    "CH": "Suiza",
    "DE": "Alemania",
    "ES": "España",

}

def id_sector(nombre_gics):
    """Convierte 'Information Technology en el identificador
    'InformationTechnology' (sin espacios).
    """
    return EX[nombre_gics.replace(" ", "")]

# Leer el CSV fila fila
#  csv.DictReader lee la primera línea como cabecera, y luego entrega
#  cada fila como un diccionario: fila["ticker"], fila["sector"], etc.
#  Es más cómodo y seguro que partir las líneas a mano, porque respeta
#  las comillas y las comas dentro de los nombres.
with open("posiciones.csv", mode="r", encoding="utf-8") as fichero:
    for fila in csv.DictReader(fichero):

        # Identiicadores
        etf = EX[fila["etf_isin"]]          # ej. ex:IE00B4L5Y983
        empresa = EX[fila["ticker"]]        # ej. ex:AAPL
        sector = id_sector(fila["sector"])  # ej. ex:InformationTechnology
        pais = EX[fila["pais"]]             # ej. ex:US

        # El ETF
        g.add((etf, RDF.type, EX.ETF))
        g.add((etf, RDFS.label, Literal(fila["etf_nombre"])))
        g.add((etf, EX.isin, Literal(fila["etf_isin"])))
        g.add((etf, EX.fechaDatos, Literal(fila["fecha_datos"], datatype=XSD.date)))
        g.add((etf, EX.fuente, Literal(fila["fuente"], datatype=XSD.anyURI)))

        # La empresa
        g.add((empresa, RDF.type, EX.Empresa))
        g.add((empresa, RDFS.label, Literal(fila["empresa_nombre"])))
        g.add((empresa, EX.ticker, Literal(fila["ticker"])))

        # El sector y el pais 
        g.add((sector, RDF.type, EX.Sector))
        g.add((sector, RDFS.label, Literal(fila["sector"])))
        g.add((pais, RDF.type, EX.Pais))
        g.add((pais, RDFS.label, Literal(NOMBRES_PAIS[fila["pais"]], lang="es")))
        g.add((pais, EX.codigoISO, Literal(fila["pais"])))

        # Las tres relaciones (las flechas del esquema)
        g.add((etf, EX.contiene, empresa))
        g.add((empresa, EX.perteneceA, sector))
        g.add((empresa, EX.tieneSedeEn, pais))

        # La columna "peso" se lee pero todavía no se guarda: hará falta
        # la clase Posición de la siguiente versión de la ontología. 

print(f"Tripletas de la ontología: {tripletas_ontologia}")
print(f"Tripletas de datos añadidas: {len(g) - tripletas_ontologia}")

# Guardamos el grafo
g.serialize("grafo.ttl", format="turtle")
print("Grafo guardado en grafo.ttl")

# Comrpobaciones rápidas
def contar(clase):
    """Cuántas cosas distintas hay de un tipo."""
    consulta = "SELECT (COUNT(DISTINCT ?x) AS ?n) WHERE { ?x a ?clase . }"
    resultado = g.query(consulta, initBindings={"clase": clase})
    return int(list(resultado)[0].n)

print("\nResumen del grafo:")
for clase in (EX.ETF, EX.Empresa, EX.Sector, EX.Pais):
    print(f"   {g.qname(clase):12} {contar(clase)}")

# Control de calidad con el razonador: si una columna del CSV estuviera
# mal puesta (por ejemplo, un sector en la columna de país), el
# razonador deduciría que algo es a la vez Sector y País. Lo buscamos
# sobre una copia, para no meter las deducciones en el grafo guardado.
copia = Graph()
copia += g
DeductiveClosure(RDFS_Semantics).expand(copia)
 
clases = [EX.ETF, EX.Empresa, EX.Sector, EX.Pais]
problemas = []
for i, a in enumerate(clases):
    for b in clases[i + 1:]:
        for x in copia.subjects(RDF.type, a):
            if (x, RDF.type, b) in copia:
                problemas.append(f"{g.qname(x)} es a la vez {g.qname(a)} y {g.qname(b)}")
 
print("\nControl de calidad:")
if problemas:
    for p in problemas:
        print("   INCORRECTO", p)
else:
    print("   CORRECTO. Ninguna cosa pertenece a dos clases a la vez")