from rdflib import RDFS, Graph, Literal, RDF, Namespace, URIRef, XSD
import json

from utils.cleaner import Cleaner

CLEANER= Cleaner()

ONTOREQ = Namespace("http://www.semanticweb.org/ontologies/2012/4/test_ontology.owl#")
SWORE= Namespace("http://ns.softwiki.de/req/2/")
EX = Namespace("http://www.semanticweb.org/prueba_merge#")

G = Graph()
G.bind("swore", SWORE)
G.bind("ontoreq", ONTOREQ)
G.bind("ex", EX)
G.parse("ontology/onto_prueba.owl")

def count_individuals_of(uri):
    return len(list(G.triples((None, RDF.type, uri))))

def load_individual(uri: URIRef, class_type: str, literal: str) -> URIRef:
    for s, p, o in G.triples((None, RDFS.label, Literal(literal))):
        return s
    individual= EX[class_type+str(count_individuals_of(uri))]
    G.add((individual, RDF.type, uri))
    G.add((individual, RDFS.label, Literal(literal)))
    return individual


def load_property(uriFrom, prop, uriTo):
    G.add((uriFrom, prop, uriTo))

def load_requirement(requirement: object, clave: str):
    uriRequirement= URIRef(SWORE["Requirement"])
    individual= load_individual(uriRequirement, "requirement", requirement[clave])
    G.add((individual, URIRef(SWORE["priority"]), Literal(requirement["Priority"])))
    G.add((individual, URIRef(SWORE["status"]), Literal(requirement["Status"])))
    G.add((individual, URIRef(EX["risk"]), Literal(requirement["Risk Probability"])))
    G.add((individual, URIRef(EX["cost"]), Literal(requirement["Cost"])))
    if (requirement["Obligatorio"] != None):
        G.add((individual, URIRef(ONTOREQ["isMandatory"]), Literal(requirement["Obligatorio"] == True, datatype=XSD.boolean)))

    return individual

def load_goal(goal: str):
    uriGoal= URIRef(ONTOREQ["Goal"])
    return load_individual(uriGoal, "goal", goal)

def load_project(project: str):
    uriProject= URIRef(SWORE["Project"])
    return load_individual(uriProject, "project", project)
 
def load_stakeholder(stakeholder: str):
    uriStakeholder= URIRef(ONTOREQ["Stakeholder"])
    return load_individual(uriStakeholder, "stakeholder", stakeholder)

def load_developer(developer: str):
    uriDeveloper= URIRef(ONTOREQ["Stakeholder"])
    return load_individual(uriDeveloper, "developer", developer)

def load_story(story: str):
    uriStory= URIRef(ONTOREQ["Story"])
    individual= load_individual(uriStory, "story", story["Key"])
    G.add((individual, URIRef("http://purl.org/dc/terms/description"), Literal(json.dumps(story, ensure_ascii=True))))
    return individual

def load_document(document: str):
    uriDocument= URIRef(SWORE["Document"])
    individual= load_individual(uriDocument, "document", document["Key"])
    G.add((individual, URIRef("http://purl.org/dc/terms/description"), Literal(json.dumps(document, ensure_ascii=True))))
    return individual

def load_obstacle(obstacle: str):
    uriObstacle= URIRef(ONTOREQ["Obstacle"])
    return load_individual(uriObstacle, "obstacle", obstacle)

def load_developedBy(requirement: URIRef, developer: URIRef):
    uriDevelopedBy= URIRef(SWORE["lastContributor"])
    load_property(requirement, uriDevelopedBy, developer)

def load_hasGoal(requirement: URIRef, goal: URIRef):
    uriHasGoal= URIRef(ONTOREQ["hasGoal"])
    load_property(requirement, uriHasGoal, goal)

def load_hasProject(requirement: URIRef, project: URIRef):
    uriHasProject= URIRef(SWORE["hasProject"])
    load_property(requirement, uriHasProject, project)

def load_hasSource(thing: URIRef, source: URIRef):
    uriHasSource= URIRef(SWORE["source"])
    load_property(thing, uriHasSource, source)

def load_describesRequirement(requirement: URIRef, source: URIRef):
    uriDescribesRequirement= ONTOREQ["describesRequirement"]
    load_property(source, uriDescribesRequirement,requirement )

def load_relatedTo(source: URIRef, target: URIRef):
    uriRelatedTo= URIRef(SWORE["relation"])
    load_property(source, uriRelatedTo, target)

def load_refinesTo(source: URIRef, target: URIRef):
    uriRelatedTo= URIRef(ONTOREQ["refinesTo"])
    load_property(source, uriRelatedTo, target)
    

def load_redundantTo(source: URIRef, target: URIRef):
    uriRelatedTo= URIRef(SWORE["isRedundantTo"])
    load_property(source, uriRelatedTo, target)

def load_requires(source: URIRef, target: URIRef):
    uriRelatedTo= URIRef(SWORE["requires"])
    load_property(target, uriRelatedTo, source)

def load_conflicts(source: URIRef, target: URIRef):
    load_property(source, URIRef(ONTOREQ["isInConflictWith"]), target)

def load_hasObstacle(requirement: URIRef, obstacle: URIRef):
    uriHasObstacle= URIRef(ONTOREQ["hasObstacle"])
    load_property(requirement, uriHasObstacle, obstacle)

def link_related_requirements():
    for story, describes_op, req in G.triples((None, ONTOREQ["describesRequirement"], None)):
        texto_story= G.value(story, URIRef("http://purl.org/dc/terms/description"))
        claves_a_buscar= json.loads(texto_story)["Related"]
        claves_a_buscar = [ key.strip() for key in claves_a_buscar.split(",")] if claves_a_buscar  else []
        for clave_a_buscar in claves_a_buscar:
            for otra_story, otro_describes_op, otro_req in G.triples((None, ONTOREQ["describesRequirement"], None)):
                clave_de_otro_req= G.value(otra_story, RDFS.label).value
                if (clave_de_otro_req == clave_a_buscar):
                    load_relatedTo(req, otro_req)

def link_duplicated_requirements():
    for story, describes_op, req in G.triples((None, ONTOREQ["describesRequirement"], None)):
        texto_story= G.value(story, URIRef("http://purl.org/dc/terms/description"))
        claves_a_buscar= json.loads(texto_story)["Duplicates"]
        claves_a_buscar = [ key.strip() for key in claves_a_buscar.split(",")] if claves_a_buscar  else []
        for clave_a_buscar in claves_a_buscar:
            for otra_story, otro_describes_op, otro_req in G.triples((None, ONTOREQ["describesRequirement"], None)):
                clave_de_otro_req= G.value(otra_story, RDFS.label).value
                if (clave_de_otro_req == clave_a_buscar):
                    load_redundantTo(req, otro_req)

def link_conflicting_requirements():
    for story, describes_op, req in G.triples((None, ONTOREQ["describesRequirement"], None)):
        texto_story= G.value(story, URIRef("http://purl.org/dc/terms/description"))
        claves_a_buscar= json.loads(texto_story)["Conflicting"]
        claves_a_buscar = [ key.strip() for key in claves_a_buscar.split(",")] if claves_a_buscar  else []
        for clave_a_buscar in claves_a_buscar:
            for otra_story, otro_describes_op, otro_req in G.triples((None, ONTOREQ["describesRequirement"], None)):
                clave_de_otro_req= G.value(otra_story, RDFS.label).value
                if (clave_de_otro_req == clave_a_buscar):
                    load_conflicts(req, otro_req)

def link_blocking_requirements():
    for story, describes_op, req in G.triples((None, ONTOREQ["describesRequirement"], None)):
        texto_story= G.value(story, URIRef("http://purl.org/dc/terms/description"))
        claves_a_buscar= json.loads(texto_story)["Blocking"]
        claves_a_buscar = [ key.strip() for key in claves_a_buscar.split(",")] if claves_a_buscar  else []
        for clave_a_buscar in claves_a_buscar:
            for otra_story, otro_describes_op, otro_req in G.triples((None, ONTOREQ["describesRequirement"], None)):
                clave_de_otro_req= G.value(otra_story, RDFS.label).value
                if (clave_de_otro_req == clave_a_buscar):
                    load_requires(req, otro_req)

def populate_graph():
    with open("data/stories.json", "r", encoding='utf-8') as file:
        requirements= json.load(file)
    requirements= CLEANER.clean_requirements(requirements)

    for requirement in requirements:
        requ= load_requirement(requirement, "Quiero")
        goal = load_goal(requirement["Con el fin de"])
        project = load_project(requirement["Project"])
        stakeholder= load_stakeholder(requirement["Como"])
        dev= load_developer(requirement["Assignee"])
        story= load_story(requirement)
        obstacle= load_obstacle(requirement["Criterios de aceptación"])
        load_hasProject(requ, project)
        load_hasGoal(requ, goal)
        load_developedBy(requ, dev)
        load_hasSource(requ, stakeholder)
        load_describesRequirement(requ, story)
        load_hasObstacle(requ, obstacle)
        

    link_related_requirements()
    link_duplicated_requirements()
    link_conflicting_requirements()
    link_blocking_requirements()
    G.serialize("ontology/data_graph.xml", format="xml", encoding="utf-8")

