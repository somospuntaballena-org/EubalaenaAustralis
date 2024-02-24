# ¿Dónde Firmar?

Este repositorio permite generar la lista de localidades para firmar la declaración de Punta Ballena como Área Natural Protegida. Utiliza la información proveniente del mapa interactivo que se puede encontrar en https://somospuntaballena.org/

## Instrucciones de uso

Este proyecto require [Python](https://www.python.org/downloads/).

Una vez instalado Python, ejecutar el siguiente comando para generar la lista de locales para firmar en distintos formatos de salida: CSV, Markdown, HTML y PDF. También se genera un archivo KML con los datos actuales del mapa:

```python
% python3 extract_kml_info.py
...
# Ejemplo de salida:
File saved successfully to firmas_2024_02_23_19h_25m_55s.kml
DataFrame saved to output/firmas_2024_02_23_19h_25m_55s.csv
HTML table saved to output/firmas_2024_02_23_19h_25m_55s.html
HTML table saved to firmas_2024_02_23_19h_25m_55s.html
Markdown saved to output/firmas_2024_02_23_19h_25m_55s.md
Markdown saved to firmas_2024_02_23_19h_25m_55s.md
PDF generated: output/firmas_2024_02_23_19h_25m_55s.pdf
PDF saved to output/firmas_2024_02_23_19h_25m_55s.pdf
```

El script también se puede correr en el REPL de Python haciendo

```python
exec(open("extract_kml_info.py").read())
```

---

Este proyecto se ha beneficiado de ejemplos de código y sugerencias proporcionadas a través de interacciones con la IA de OpenAI ChatGPT 4. Ver https://chat.openai.com/
