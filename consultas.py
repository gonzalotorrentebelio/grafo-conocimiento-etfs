#  consultas.py
#  hacer preguntas de inversor al grafo con SPARQL.
#
#  Entrada: grafo.ttl (generado por cargar.py)
#  Ejecutar desde la carpeta del proyecto:  python consultas.py
from rdflib import Graph, Namespace
 
EX = Namespace("http://ejemplo.org/")

#  Cargar el grafo guardado. Ya no hace falta leer el CSV: todo está
#  en grafo.ttl (ontología + datos).

g = Graph()
g.parse("grafo.ttl")

# Prefijos que usarán todas las consultas. Se ponen una vez aquí para
# no repetirlos en cada consulta.
PREFIJOS = {
    "ex": EX,
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
}

def preguntar(titulo, consulta):
    """Ejecuta una consulta SPARQL y muestra el resultado con tabla"""
    resultado = g.query(consulta, initNs=PREFIJOS)
    columnas = [str(v) for v in resultado.vars] # nombres de las variables de SELECT 
    filas = [[str(valor) for valor in fila] for fila in resultado]

    print(f"{titulo}")
    if not filas:
        print("(ningún resultado)")
        return
    # Ancho de cada columna = el texto más largo que contenga
    anchos = [max(len(c), *(len(f[i]) for f in filas)) for i, c in enumerate(columnas)]
    print("  ".join(c.ljust(a) for c, a in zip(columnas, anchos)))
    print("  ".join("-" * a for a in anchos))
    for f in filas:
        print("  ".join(v.ljust(a) for v, a in zip(f, anchos)))

    # ¿Qué empresas están en más de un ETF?
    #  Novedades de SPARQL:
    #    GROUP BY  agrupa las filas por empresa (como en SQL)
    #    HAVING    filtra DESPUÉS de agrupar: solo grupos con más de 1 ETF
    #    ORDER BY  ordena el resultado

preguntar("1. ¿Qué empresas están en más de uno de mis ETFs?", """
    SELECT ?empresa (COUNT(?etf) AS ?num_etfs)
    WHERE {
        ?etf ex:contiene ?e .
        ?e rdfs:label ?empresa .
    }
    GROUP BY ?empresa
    HAVING (COUNT(?etf) > 1)
    ORDER BY ?empresa
""")

preguntar("2. ¿Cuántas empresas comparte cada par de ETFs?", """
    SELECT ?etf_a ?etf_b (COUNT(?empresa) AS ?compartidas)
    WHERE {
        ?a ex:contiene ?empresa ; rdfs:label ?etf_a .
        ?b ex:contiene ?empresa ; rdfs:label ?etf_b .
        FILTER (STR(?a) < STR(?b))
    }
    GROUP BY ?etf_a ?etf_b
    ORDER BY DESC(?compartidas)
""")
 
 
preguntar("3. ¿Cuántas posiciones tiene cada ETF en cada sector?", """
    SELECT ?etf ?sector (COUNT(?e) AS ?posiciones)
    WHERE {
        ?x ex:contiene ?e ; rdfs:label ?etf .
        ?e ex:perteneceA ?s .
        ?s rdfs:label ?sector .
    }
    GROUP BY ?etf ?sector
    ORDER BY ?etf DESC(?posiciones)
""")
 

preguntar("4. ¿Qué ETFs tienen empresas tecnológicas estadounidenses (y cuáles)?", """
    SELECT ?etf (GROUP_CONCAT(?ticker; separator=", ") AS ?empresas)
    WHERE {
        ?x ex:contiene ?e ; rdfs:label ?etf .
        ?e ex:perteneceA ex:InformationTechnology ;
           ex:tieneSedeEn ex:US ;
           ex:ticker ?ticker .
    }
    GROUP BY ?etf
""")
 
 
preguntar("5. ¿En cuántas empresas y países distintos invierten (top 10)?", """
    SELECT (COUNT(DISTINCT ?e) AS ?empresas_distintas)
           (COUNT(DISTINCT ?p) AS ?paises_distintos)
    WHERE {
        ?etf ex:contiene ?e .
        ?e ex:tieneSedeEn ?p .
    }
""")
 
 
preguntar("6. ¿Qué empresas no estadounidenses tengo?", """
    SELECT ?empresa ?pais ?etf
    WHERE {
        ?x ex:contiene ?e ; rdfs:label ?etf .
        ?e rdfs:label ?empresa ;
           ex:tieneSedeEn ?p .
        ?p ex:codigoISO ?pais .
        FILTER (?p != ex:US)
    }
    ORDER BY ?pais ?empresa
""")
 
 

preguntar("7. ¿A través de qué ETFs estoy expuesto a NVIDIA?", """
    SELECT ?etf
    WHERE {
        ?x ex:contiene ex:NVDA ; rdfs:label ?etf .
    }
""")
 
 
preguntar("8. ¿De qué fecha y fuente son los datos de cada ETF?", """
    SELECT ?etf ?fecha ?fuente
    WHERE {
        ?x a ex:ETF ;
           rdfs:label ?etf ;
           ex:fechaDatos ?fecha ;
           ex:fuente ?fuente .
    }
    ORDER BY ?fecha
""")

