#!/usr/bin/env python3
"""Regenerate imports/*_terms.txt from the current ../cmeo.owl.
Lists every external OBO IRI (non-CMEO) that CMEO reuses, grouped by source ontology.
    cd imports && python3 make_term_lists.py [../cmeo.owl]
"""
import sys, re, collections, rdflib
from rdflib import RDF, RDFS, OWL, URIRef

path = sys.argv[1] if len(sys.argv) > 1 else "../cmeo.owl"
g = rdflib.Graph(); g.parse(path)
ext = set()
for t in (OWL.Class, OWL.ObjectProperty, OWL.AnnotationProperty, OWL.DatatypeProperty):
    ext |= {str(s) for s in g.subjects(RDF.type, t) if isinstance(s, URIRef)}
for p in (RDFS.subClassOf, OWL.someValuesFrom, OWL.allValuesFrom, OWL.onClass, OWL.onProperty,
          OWL.equivalentClass, OWL.disjointWith, RDFS.domain, RDFS.range, RDFS.subPropertyOf):
    ext |= {str(o) for o in g.objects(None, p) if isinstance(o, URIRef)}

groups = collections.defaultdict(set)
for iri in ext:
    m = re.match(r'http://purl\.obolibrary\.org/obo/([A-Z]+)_\d+$', iri)
    if m and m.group(1) != "CMEO":
        groups[m.group(1)].add(iri)

for pref, iris in sorted(groups.items()):
    fn = f"{pref.lower()}_terms.txt"
    open(fn, "w").write("\n".join(sorted(iris)) + "\n")
    print(f"{fn}: {len(iris)} terms")
print(f"\n{sum(len(v) for v in groups.values())} external terms across {len(groups)} sources")
