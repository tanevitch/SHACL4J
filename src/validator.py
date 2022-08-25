from rdflib import Graph, URIRef, RDFS
from pyshacl import validate
import re

def build_report(txt, data_graph):
        report= "---------------------------\nREPORTE DE ERRORES\n---------------------------\n"
        reporte_errores= txt.split("Constraint Violation")
        del reporte_errores[0]
        for error in reporte_errores:
            requirement= re.search("requirement\\w+", error)
            label= data_graph.value(URIRef("http://www.semanticweb.org/prueba_merge#"+requirement.group(0)), RDFS.label)
            message= re.search('Message: .+', error).group(0) if re.search('Message: .+', error) else ""
            report_text= f"Error en requerimiento '{label}'. {message}"

            report += report_text + '\n'
        
        return report+"---------------------------\nFIN REPORTE\n---------------------------"

def validate_graph():
    data_graph = Graph()
    data_graph.parse("ontology/data_graph.xml")

    shape_graph = Graph()
    shape_graph.parse("ontology/shape_graph.ttl")

    result= validate(data_graph,
        shacl_graph=shape_graph,
        ont_graph=None,
        inference='none',
        abort_on_first=False,
        allow_infos=False,
        allow_warnings=False,
        meta_shacl=False,
        advanced=False,
        js=False,
        debug=False)

    with open('reporte.txt', 'w', encoding="utf-8") as f:
        f.write(build_report(result[2], data_graph))

validate_graph()