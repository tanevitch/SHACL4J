# SHACL4J

SHACL4J es una herramienta que tiene como objetivo servir de soporte para validar requerimientos provenientes de un programa de gestión de proyectos. 

## Estructura
* Data: el dataset con historias exportadas de un proyecto finalizado que utilizó el producto Jira
* Ontology: la ontología a utilizar para conceptualizar todos los elementos necesarios de la Ingeniería de Software que servirán para formalizar los requerimientos extraídos de Jira
* 

## Instalación y ejecución

```sh
git clone https://github.com/tanevitch/SHACL4J.git
python -m venv .env
.env\Script\activate
pip install -r requirements.txt
python run
```

## Contribución
Para la  ontología utilizada se seleccionaron conceptos de SWORE y Requirements Ontology, realizando los alineamientos necesarios para aquellos términos que representan semánticamente lo mismo, y modificaciones menores para reemplazar las clases RO:LevelOfCost y RO:LevelOfRisk por propiedades de datos como las que define SWORE:priority y SWORE:status, quedando como resultado EX:cost y EX:risk, con rango Requirement y dominio una cadena de texto. 

Para el poblado del grafo se toma como entrada la ontología  onto_entrada.owl y el dataset stories.json (que aparece por la conversión de DatasetStories.xlsx a json), realizando el un pequeño procesamiento de datos con Spacy para eliminar caracteres no deseados e identificar que se cumplan ciertos patrones sintácticos.

A partir del grafo output.xml se realiza la verificación de consistencia, completitud y calidad aplicando reglas escritas en lenguaje SHACL, dando como resultado un archivo de texto donde se detallan los errores en caso de existir


## License
[MIT](https://choosealicense.com/licenses/mit/)