from rdflib import Graph
from io import StringIO 
from pyshacl import validate

def validate_graph():
    data_graph = Graph()
    data_graph.parse("ontology/output.xml")

    shape_sobre_requirement = Graph()
    shape_sobre_requirement.parse(StringIO('''
    @prefix dash: <http://datashapes.org/dash#> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix sh: <http://www.w3.org/ns/shacl#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    @prefix ex: <http://example.org/ns#> .
    @prefix swore: <http://ns.softwiki.de/req/2/> .
    @prefix ro: <http://www.semanticweb.org/ontologies/2012/4/test_ontology.owl#> .

    ex:RequirementShape
        a sh:NodeShape ;
        sh:targetClass swore:Requirement ;
        sh:property [
            sh:path ro:hasGoal;
            sh:minCount 1 ;
            sh:message "Cada requerimiento debe estar asociado a al menos una meta"@es ;
        ] ;
        sh:property [
            sh:path ro:isInConflictWith;
            sh:maxCount 0 ;
            sh:message "No debe haber requerimientos conflictivos"@es ;
        ] ;
        sh:property [
            sh:path ro:isMandatory;
            sh:minCount 1 ;
            sh:maxCount 1 ;
            sh:datatype xsd:boolean ;
            sh:message "Para cada requerimiento, se debe definir si es obligatorio o no"@es ;
        ] ;
        sh:sparql [
            a sh:SPARQLConstraint ;
            sh:message "si un requerimiento está bloqueado por otro ese requerimiento no puede estar cerrado si su bloqueante no lo está";
            sh:select 
            """ select $this
                where {
                        $this a <http://ns.softwiki.de/req/2/Requirement> . 
                        $this <http://ns.softwiki.de/req/2/status> ?literal1 .
                        filter(?literal1 in ('closed','cerrado', 'resuelto')) .
                        $this <http://ns.softwiki.de/req/2/requires> ?otroReq .
                        ?otroReq a <http://ns.softwiki.de/req/2/Requirement> .
                        ?otroReq <http://ns.softwiki.de/req/2/status> ?literal .
                        filter(?literal in ('abierto','in progress', 'open')) .
                }
            """;
        ].
    '''))

    shape_sobre_meta = Graph()
    shape_sobre_meta.parse(StringIO('''
    @prefix dash: <http://datashapes.org/dash#> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix sh: <http://www.w3.org/ns/shacl#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    @prefix ex: <http://example.org/ns#> .
    @prefix ro: <http://www.semanticweb.org/ontologies/2012/4/test_ontology.owl#> .


    ex:GoalCountShape
        a sh:NodeShape ;
        sh:targetNode ro:Goal ;
        sh:property [
            sh:path [ sh:inversePath rdf:type ] ;
            sh:minCount 1 ;
            sh:message "Al menos una meta debe ser especificada"@es ;
        ] .
    '''))

    validaciones_goal= validate(data_graph,
        shacl_graph=shape_sobre_meta,
        ont_graph=None,
        inference='none',
        abort_on_first=False,
        allow_infos=False,
        allow_warnings=False,
        meta_shacl=False,
        advanced=False,
        js=False,
        debug=False)

    validacion_requirement= validate(data_graph,
        shacl_graph=shape_sobre_requirement,
        ont_graph=None,
        inference='none',
        abort_on_first=False,
        allow_infos=False,
        allow_warnings=False,
        meta_shacl=False,
        advanced=False,
        js=False,
        debug=False)

    results_text1 = validacion_requirement
    results_text2 = validaciones_goal

    with open('reporte.txt', 'w') as f:
        f.write(results_text1[2])
        f.write(results_text2[2])
        f.write("-------------")

