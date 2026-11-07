# Comparación: grafo de conocimiento frente a LLM sin datos

## Método

Se hicieron las 8 preguntas de `consultas.py` a dos modelos de lenguaje respondiendo de memoria, sin acceso a internet ni a los datos del proyecto: **Claude Haiku** y **Claude Sonnet** (7 de noviembre de 2026). Ambos recibieron el mismo mensaje, con los nombres y los ISIN de los tres ETFs, y la indicación de contar Alphabet como una sola empresa. Sus respuestas completas están en el anexo.

La referencia es el grafo (`grafo.ttl`), construido con las 10 principales posiciones publicadas entre el 11 y el 30 de septiembre de 2026.

Criterio: **✓** correcto · **≈** parcialmente correcto · **✗** incorrecto · **—** no puede responder

## Resultados pregunta a pregunta

| # | Pregunta | Grafo | Haiku | Sonnet |


| 1 | Empresas en más de un ETF | 9: NVIDIA, Apple, Microsoft, Alphabet, Amazon, Broadcom, Meta, Micron, Tesla | ✗ 10; añade Berkshire y JPMorgan, olvida Micron | ≈ 9, pero con JPMorgan en lugar de Micron |
| 2 | Empresas compartidas por par | World–S&P: 9; pares con Europe: 0 | ✗ World–S&P: 10 | ✓ 9 / 0 / 0 |
| 3 | Posiciones por sector | World y S&P: IT 5, Consumo discr. 2, Comunicación 2. Europe: Salud 3, IT 2, Financiero 2, Consumo básico 1, Energía 1, Industria 1 | ✗ IT 4, inventa 2 financieras; Europe con Salud 4 y sin Industria | ✗ IT 4, inventa financieras y Salud en World; Europe con Salud 4 |
| 4 | Tecnológicas estadounidenses | World y S&P: Apple, Broadcom, Microsoft, Micron, NVIDIA | ≈ olvida Micron | ≈ olvida Micron |
| 5 | Empresas y países distintos | 19 empresas, 6 países | ✗ 20 y 7 (incluye Francia y Dinamarca, olvida España) | ≈ 21 empresas; 6 países, pero con Dinamarca en vez de España |
| 6 | Empresas no estadounidenses | 10, todas en Europe; incluye Siemens (DE) y Banco Santander (ES) | ≈ incluye Novo Nordisk y LVMH; olvida Siemens y Santander | ≈ incluye Novo Nordisk; olvida Santander |
| 7 | Exposición a NVIDIA | World y S&P 500 | ✓ | ✓ |
| 8 | Fecha y fuente de los datos | Fecha exacta y URL de cada ETF | — «aprox. 2025», sin fuente | — «probablemente 2025», sin fuente |

## Marcador

| Correctas | Parciales | Incorrectas | Sin respuesta |

| Grafo | 8 | 0 | 0 | 0 |
| Claude Haiku | 1 | 2 | 4 | 1 |
| Claude Sonnet | 2 | 4 | 1 | 1 |

## Conclusiones

1. **Los errores del LLM son plausibles, no absurdos.** Berkshire, JPMorgan, Eli Lilly o Novo Nordisk estuvieron en esos top 10 en algún momento. El modelo no inventa al azar: recuerda una foto antigua y la presenta como actual. Eso hace el error más difícil de detectar.
2. **El fallo se propaga.** Un solo dato desactualizado (no saber que Micron ha subido al top 10) arruina a la vez las respuestas 1, 3, 4 y 5. En el grafo, cada respuesta se deriva de los mismos hechos verificados.
3. **El LLM es honesto sobre su incertidumbre, pero esa honestidad no sirve para actuar.** Ambos avisan de que sus datos pueden estar desactualizados, pero no pueden decir *cuáles*. El grafo responde con fecha y URL exactas: cada afirmación se puede comprobar.
4. **Un modelo más grande mejora, pero no resuelve el problema.** Sonnet acierta más que Haiku, pero ninguno acierta las preguntas que dependen de la composición exacta. No es una cuestión de tamaño del modelo, sino de anclaje a los datos.
5. **Donde la pregunta es estable, el LLM acierta** (pregunta 7: NVIDIA lleva tiempo en cabeza). Su punto débil es lo que cambia con el tiempo, que es justo lo que importa a un inversor.

## Limitaciones

- La «verdad» del grafo es tan buena como sus fuentes: agregadores de terceros con fechas distintas, y sectores y países asignados a mano.
- Solo se han probado dos modelos de una misma empresa y una sola formulación de las preguntas.
- Los LLM podrían acertar más si se les dieran los datos (eso sería GraphRAG: el siguiente paso natural del proyecto).

---

## Anexo: respuestas completas de los modelos

### Claude Haiku

1. Las 10 del MSCI World son las mismas que las del S&P 500: NVIDIA, Microsoft, Apple, Alphabet, Amazon, Meta, Broadcom, Tesla, Berkshire Hathaway y JPMorgan Chase. Ninguna de las 10 del Europe aparece en los otros dos.
2. MSCI World y S&P 500: 10. MSCI World y MSCI Europe: 0. S&P 500 y MSCI Europe: 0.
3. World y S&P 500: Tecnología 4, Comunicación 2, Consumo discrecional 2, Financiero 2. Europe: Tecnología 2, Consumo discrecional 1, Financiero 1, Salud 4, Consumo básico 1, Energía 1.
4. Estricto: NVIDIA, Microsoft, Apple y Broadcom, en MSCI World y S&P 500. Ampliando a las grandes tecnológicas: también Alphabet, Meta, Amazon y Tesla. MSCI Europe no tiene ninguna.
5. Empresas distintas: 20. Países: 7 (Estados Unidos, Países Bajos, Alemania, Suiza, Dinamarca, Francia y Reino Unido).
6. ASML (Países Bajos); SAP (Alemania); Nestlé, Novartis y Roche (Suiza); Novo Nordisk (Dinamarca); LVMH (Francia); AstraZeneca, HSBC y Shell (Reino Unido). Todas en MSCI Europe.
7. A través de MSCI World y de S&P 500. No la tienes en MSCI Europe.
8. Los datos proceden de mi conocimiento de entrenamiento; no tengo una fecha exacta ni una fuente citable. Corresponden aproximadamente a la composición de 2025.

### Claude Sonnet

Top 10 usados — World: NVIDIA, Microsoft, Apple, Amazon, Meta, Alphabet, Broadcom, Tesla, JPMorgan, Eli Lilly. S&P 500: NVIDIA, Microsoft, Apple, Amazon, Meta, Alphabet, Broadcom, Tesla, Berkshire Hathaway, JPMorgan. Europe: ASML, SAP, Nestlé, Novartis, Roche, AstraZeneca, HSBC, Shell, Novo Nordisk, Siemens.
1. Nueve empresas están en World y S&P 500: NVIDIA, Microsoft, Apple, Amazon, Meta, Alphabet, Broadcom, Tesla y JPMorgan.
2. World y S&P 500: 9. World y Europe: 0. S&P 500 y Europe: 0.
3. World: Tecnología 4, Comunicación 2, Consumo discrecional 2, Financiero 1, Salud 1. S&P 500: Tecnología 4, Comunicación 2, Consumo discrecional 2, Financiero 2. Europe: Tecnología 2, Financiero 1, Salud 4, Consumo básico 1, Energía 1, Industriales 1.
4. World y S&P 500, con NVIDIA, Microsoft, Apple y Broadcom (Meta y Alphabet son Servicios de comunicación en GICS). Europe no tiene ninguna.
5. Empresas distintas: 21. Países distintos: 6 (EE. UU., Países Bajos, Alemania, Suiza, Reino Unido y Dinamarca).
6. Países Bajos: ASML. Alemania: SAP y Siemens. Suiza: Nestlé, Novartis y Roche. Reino Unido: AstraZeneca, HSBC y Shell. Dinamarca: Novo Nordisk. Todas en MSCI Europe.
7. A través del MSCI World y del S&P 500.
8. No tengo una fecha ni una fuente verificable; son composiciones aproximadas, probablemente de 2025.
