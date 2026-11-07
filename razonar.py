from rdflib import Graph, Namespace, RDF
from owlrl import DeductiveClosure, RDFS_Semantics

EX = Namespace("http://ejemplo.org/")

# Cargamos la ontología
g = Graph()
g.bind("ex", EX)
g.parse("ontologia.ttl")
print(f"Tripletas de la ontología: {len(g)}")

# Añadimos unos datos de prueba
etf = EX.IE00B4L5Y98   # iShares Core MSCI World (identificado por su ISIN)
apple = EX.AAPL        # Apple (identificada por su ticker)

g.add((etf, EX.contiene, apple))
g.add((apple, EX.perteneceA, EX.InformationTechnology))
g.add((apple, EX.tieneSedeEn, EX.US))
print(f"Tripletas tras añadir los datos: {len(g)}")

# Una consulta ANTES de razonar
consulta_empresas = """
    SELECT ?x WHERE { ?x a ex:Empresa . }
"""
 
def listar(titulo, consulta):
    """Ejecuta una consulta e imprime los resultados de forma legible."""
    filas = list(g.query(consulta, initNs={"ex": EX}))
    print(f"\n{titulo}")
    if not filas:
        print("   (ningún resultado)")
    for fila in filas:
        # g.qname() abrevia la URL completa a la forma ex:AAPL
        print("  ", g.qname(fila.x))
 
listar("Empresas ANTES de razonar:", consulta_empresas)


# Razonar
# DeductiveClosure aplica una y otra vez las reglas de RDFS hasta que
# ya no puede deducir nada nuevo, y añade al grafo lo que deduce.
DeductiveClosure(RDFS_Semantics).expand(g)
print(f"\nTripletas tras razonar: {len(g)}")
# El número sube mucho porque el razonador también añade tripletas
# "obvias" del propio estándar RDFS. Lo importante son las de abajo.

# Hacemos la misma consulta después de razonar
listar("Empresas DESPUÉS de razonar:", consulta_empresas)


# Comprobamos una a una 
print("\nDeducciones del razonador:")
comprobaciones = [
    (apple, EX.Empresa, "AAPL es una Empresa         (por el rango de contiene)"),
    (etf, EX.ETF, "IE00B4L5Y983 es un ETF      (por el dominio de contiene)"),
    (EX.InformationTechnology, EX.Sector, "InformationTechnology es un Sector (por el rango de perteneceA)"),
    (EX.US, EX.Pais, "US es un País                (por el rango de tieneSedeEn)"),
]
for sujeto, clase, explicacion in comprobaciones:
    deducido = (sujeto, RDF.type, clase) in g
    print(f" {'CORRECTO' if deducido else 'INCORRECTO'} {explicacion}")