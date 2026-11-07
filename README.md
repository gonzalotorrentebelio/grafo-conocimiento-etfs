# IA-Semantica

Qué es la IA Neurosimbólica?

La IA reurosimbólica combina dos enfoques. La parte **neuronal** (los modelos
de lenguaje como ChatGPT) aprende patrons estádistcos a partir de enormes 
cantidades de texto: manja muy bin el lenguaje, pero responde por 
probabilidad y puede inventarse datos ("alucinar").

La parte **simbólica** representa el conocimento de forma explícita en un 
grafo. Cada dato se guarda como una tripleta sujeto-predicado-objeto (por
ejemplo, <<MSCI World contiene Apple>>), y al juntar muchas tripletas se 
forma una red de entidades conectadas. Una ontología define qué tipos de 
cosas existen y cómo se relacionan, lo que permite a la máquina deducir 
conocimiento nuevo. El grafo se consulta con el lenguaje SPARQL.

Al combinarlas, el modelo de lenguaje aporta la conversación y el grafo
aporta los hechos: cada respuesta se puede verificar y rastrear hasta su fuente.