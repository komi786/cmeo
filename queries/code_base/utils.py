Yes from rdflib import Dataset, Namespace,Graph, RDF, RDFS, URIRef, DC
from SPARQLWrapper import SPARQLWrapper, JSON
from urllib.parse import quote
import pandas as pd
from .config import settings
import requests
from thefuzz import fuzz
import os
import re
import urllib.parse
from enum import Enum



from datetime import datetime

class OntologyNamespaces(Enum):
    CMEO = Namespace("https://w3id.org/CMEO/")
    OMOP = Namespace("http://omop.org/OMOP/")
    ATC = Namespace("http://purl.bioontology.org/ontology/ATC/")
    RXNORM = Namespace("http://purl.bioontology.org/ontology/RXNORM/")
    UCUM = Namespace("http://unitsofmeasure.org/")
    OMOP_EXT = Namespace("http://omop.org/omopextension/")
    OWL = Namespace("http://www.w3.org/2002/07/owl#")
    OBI = Namespace("http://purl.obolibrary.org/obo/obi.owl/")
    OBCS = Namespace("http://purl.obolibrary.org/obo/obcs.owl/")
    BFO = Namespace("http://purl.obolibrary.org/obo/bfo.owl/")
    STATO = Namespace("http://purl.obolibrary.org/obo/stato.owl/")
    DEFAULT_VALUE = 'Unmapped'
    SNOMEDCT = Namespace("http://purl.bioontology.org/ontology/SNOMEDCT/")
    LOINC = Namespace("http://purl.bioontology.org/ontology/LNC/") 
    RO = Namespace("http://purl.obolibrary.org/obo/ro.owl/")
    IAO = Namespace("http://purl.obolibrary.org/obo/iao.owl/")
    TIME = Namespace("http://www.w3.org/2006/time#")
    SIO = Namespace("http://semanticscience.org/ontology/sio.owl/")
    ICD10 = Namespace("http://purl.bioontology.org/ontology/ICD10/")
    ICD9 = Namespace("http://purl.bioontology.org/ontology/ICD9CM/")
    DUO = Namespace("http://purl.obolibrary.org/obo/duo.owl/")
    NCBI = Namespace("http://purl.bioontology.org/ontology/NCBITAXON/")





STUDY_TYPES = {
    "observational study": URIRef(f"{OntologyNamespaces.CMEO.value}observational_study_design"),
    "randomized controlled trial": URIRef(f"{OntologyNamespaces.CMEO.value}randomized_controlled_trial_design"),
    "RCT": URIRef(f"{OntologyNamespaces.CMEO.value}randomized_controlled_trial_design"),
    "federated database": URIRef(f"{OntologyNamespaces.CMEO.value}federated_database"),
    "single-arm cross-over randomized intervention": URIRef(f"{OntologyNamespaces.CMEO.value}single_arm_cross_over_design"),
}



def normalize_text(text: str) -> str:
    if text is None or text == "nan" or text == "":
        return None
    text =str(text).lower().strip().replace(" ", "_").replace("/", "_").replace(":", "_").replace('[','').replace(']','')
    return urllib.parse.quote(text, safe='_-')



def init_graph(default_graph_identifier: str | None = "https://w3id.org/CMEO/graph/studies_metadata") -> Dataset:
    """Initialize a new RDF graph for nquads with the voc namespace bindings."""
    g = Dataset(store="Oxigraph")
    g.bind("cmeo", OntologyNamespaces.CMEO.value)
    g.bind("bfo", OntologyNamespaces.BFO.value)
    g.bind("obi", OntologyNamespaces.OBI.value)
    g.bind("stato", OntologyNamespaces.STATO.value)
    g.bind("obcs", OntologyNamespaces.OBCS.value)
    g.bind("rdf", RDF)
    g.bind("iao", OntologyNamespaces.IAO.value)
    g.bind("ro", OntologyNamespaces.RO.value)
    g.bind("time", OntologyNamespaces.TIME.value)
    g.bind("sio", OntologyNamespaces.SIO.value)
    g.bind("duo", OntologyNamespaces.DUO.value)
    g.bind("rdfs", RDFS)
    # g.bind("omop", OMOP)
    g.bind("dc", DC)
    g.bind("ncbi", OntologyNamespaces.NCBI.value) 

    g.graph(identifier=URIRef(default_graph_identifier))
    return g



def get_study_uri(study_id: str) -> URIRef:
    study_uri = URIRef(OntologyNamespaces.CMEO.value + study_id)
    return study_uri
def get_cohort_uri(cohort_id: str) -> URIRef:
    safe_cohort_id = normalize_text(cohort_id)
    if safe_cohort_id is None:
       raise ValueError("Cohort ID is empty")
    return OntologyNamespaces.CMEO.value[f"{safe_cohort_id}"]


def get_var_uri(cohort_id: str | URIRef, var_id: str) -> URIRef:
    safe_var_id = normalize_text(var_id)
    if safe_var_id == "":
        print("Variable ID is empty")
    safe_cohort_id = normalize_text(cohort_id)
    return OntologyNamespaces.CMEO.value[f"{safe_cohort_id}/{safe_var_id}"]



def extract_age_range(text):
    # Normalize Unicode comparison symbols
    text = text.strip().replace("≥", ">=").replace("≤", "<=")

    # Patterns for extracting min and max age
    age_conditions = re.findall(r'(?:age\s*)?(>=|<=|>|<)\s*(\d+(?:\.\d+)?)\s*(?:years\s*old|years)?', text, flags=re.IGNORECASE)

    min_age = None
    max_age = None

    for operator, value in age_conditions:
        value = float(value)
        if operator in ('>=', '>'):
            if min_age is None or value > min_age:
                min_age = value if operator == '>' else value  # can adjust to value + epsilon if needed
        elif operator in ('<=', '<'):
            if max_age is None or value < max_age:
                max_age = value if operator == '<' else value  # can adjust to value - epsilon if needed

    # Also handle "between X and Y years" separately
    match = re.search(r'between\s+(\d+(?:\.\d+)?)\s*(?:and|[-–])\s*(\d+(?:\.\d+)?)\s*years?', text, flags=re.IGNORECASE)
    if match:
        min_val = float(match.group(1))
        max_val = float(match.group(2))
        if min_age is None or min_val > min_age:
            min_age = min_val
        if max_age is None or max_val < max_age:
            max_age = max_val

    if min_age is not None or max_age is not None:
        return min_age, max_age

    return None

def determine_var_uri(g, cohort_id, var_name,multi_class_categorical, binary_categorical, data_type=None):
    # cohort_uri = get_cohort_uri(cohort_id)
    var_uri = get_var_uri(cohort_id, var_name)
    if var_name in binary_categorical:
        statistical_type_uri =  URIRef(var_uri + "/binary_class_variable")
        statistical_type = "binary_class_variable"
        
    elif var_name in multi_class_categorical:
        statistical_type_uri =  URIRef(var_uri + "/multi_class_variable")
        statistical_type = "multi_class_variable"
    elif data_type  and data_type in  ["str", "datetime"]:
        statistical_type_uri =  URIRef(var_uri + "/qualitative_variable")
        statistical_type = "qualitative_variable"
    else:
        statistical_type_uri =  URIRef(var_uri + "/continuous_variable")
        statistical_type = "continuous_variable"
    return statistical_type_uri,statistical_type


def extract_tick_values(texts: str) -> list[float]:
    """Extract numeric tick labels from a matplotlib Text() list‑string.

    Example input (single string):
        "Text(-2.5, 0, '−2.5') - Text(0.0, 0, '0.0') - Text(2.5, 0, '2.5')"

    Returns:
        [-2.5, 0.0, 2.5]
    """
    ticks = []
    # Split the string at the separators used by the user (" - ")
    for token in texts.split(" - "):
        # Regex captures the *label* part (text between the final pair of quotes)
        m = re.search(r"Text\([^,]+,\s*[^,]+,\s*'([^']+)'\)", token)
        if m:
            val_str = m.group(1).replace('−', '-')  # normalise Unicode minus
            try:
                ticks.append(float(val_str))
            except ValueError:
                # Skip if the captured label is not a number
                pass
    return ticks
def is_categorical_variable(df):
    binary_categorical = []
    multi_class_categorical = []
    # create dict using variable name and CATREGORICAL
    column_dict = dict(zip(df['variablename'], df['categorical']))
    for key, value in column_dict.items():
        # if pd.notna(value) and value:
            if pd.notna(value) and value != "":
                if len(value.split("|")) == 2:
                    binary_categorical.append(normalize_text(key))
                else:
                    multi_class_categorical.append(normalize_text(key))
            
    # print(f"categorical columns: ({len(binary_categorical)})")
    # print(f"categorical columns: ({len(multi_class_categorical)})")
    return binary_categorical, multi_class_categorical


def safe_int(value):
    """Safely convert a value to an integer, returning None if the value is invalid."""
    try:
        return int(float(value)) if value else None
    except ValueError:
        print(f"Invalid integer value: {value}")
        return None



def parse_joined_string(input_str: str) -> list:
    """
    Parses a string that may be either:
    - a key-value categorical string like '1=No|2=Yes' or '1="mmol|l"|2="g|dl"'
    - a plain joined string like '"mg|dl"|mmol'
    
    Returns a list of extracted values, handling quoted values and internal pipes correctly.
    """
    if not input_str or not isinstance(input_str, str):
        return []

    # Case 1: If the string has key=value pattern
    if re.search(r'\d+\s*=', input_str):
        # Match key=value pairs with quoted or unquoted values
        pattern = r'\d+\s*=\s*"[^"]*"|\d+\s*=\s*[^|]+'
        matches = re.findall(pattern, input_str)
        values = [
            re.sub(r'^\d+\s*=\s*', '', match).strip().strip('"')
            for match in matches if match.strip()
        ]
    else:
        # Case 2: Just split by top-level pipes, respecting quotes
        pattern = r'"[^"]*"|[^|"]+'
        matches = re.findall(pattern, input_str)
        values = [match.strip().strip('"') for match in matches if match.strip()]

    return values


def delete_existing_triples(graph_uri: str | URIRef, subject="?s", predicate="?p"):
    print(f"deleting existing triples from the graph={graph_uri}")
    if graph_exists(graph_uri):
        
        print(f"Graph exists: {graph_uri}")
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        DELETE WHERE {{
            GRAPH <{graph_uri!s}> {{ {subject} {predicate} ?o . }}
        }}
        """
        print(f"Query = {query}")
        
        query_endpoint = SPARQLWrapper(settings.update_endpoint)
        query_endpoint.setMethod("POST")
        query_endpoint.setRequestMethod("urlencoded")
        query_endpoint.setQuery(query)
        results =query_endpoint.query()
        response_status = results.response.status
        # response_content = results.response.read()
        print(f"graph deletion status code: {response_status}")
    else:
        print(f"Graph does not exist: {graph_uri}")
        
def graph_exists(graph_uri: str | URIRef):
    query = f"""
    ASK WHERE {{
        GRAPH <{graph_uri!s}> {{ ?s ?p ?o }}
    }}
    """
    print(f"Checking if graph exists: {query}")
    query_endpoint = SPARQLWrapper(settings.query_endpoint)
    query_endpoint.setReturnFormat(JSON)
    query_endpoint.setQuery(query)
    results = query_endpoint.query().convert()
    # print(f"Graph exists: {results['boolean']}")
    return results['boolean']


    

def save_graph_to_trig_file(graph_data, file_path):
    """
    Save RDFLib Graph data to a TRiG file under a specific named graph.
    
    :param graph_data: An RDFLib Graph containing the query results
    :param file_path: Path to the TRiG file to save data
    :param graph_uri: The named graph URI to wrap the triples under
    """
    try:
        # Serialize the graph into TriG format, placing data inside the specified named graph block
        trig_data = graph_data.serialize(format='trig')
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Write the TRiG data to a file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(trig_data)
        print(f"Graph data successfully saved to {file_path}")
    except Exception as e:
        print(f"Error saving graph to TRiG file: {e}")


def check_triple_exists(graph_uri: str | URIRef, subject: URIRef, predicate: URIRef, obj: URIRef | Literal):
    query = f"""
    ASK WHERE {{
        GRAPH <{graph_uri!s}> {{ <{subject}> <{predicate}> {f'<{obj}>' if isinstance(obj, URIRef) else f'"{obj}"'} }}
    }}
    """
    print(f"Checking if triple exists: {query}")
    query_endpoint = SPARQLWrapper(settings.query_endpoint)
    query_endpoint.setReturnFormat(JSON)
    query_endpoint.setQuery(query)
    results = query_endpoint.query().convert()
    # print(f"Triple exists: {results['boolean']}")
    return results['boolean']
    


def add_triples_to_graph(graph: Graph, triples: list, graph_context: URIRef = None) -> None:
    """
    Adds a list of triples to the graph, optionally under a specific graph context.

    :param graph: RDF Graph
    :param triples: List of triples (subject, predicate, object)
    :param graph_context: Specific graph/context to add the triples to
    """
    for subj, pred, obj in triples:
        if graph_context:
            graph.add((subj, pred, obj, graph_context))
            print(f"Added triple: {subj} {pred} {obj} in graph {graph_context}")
        else:
            graph.add((subj, pred, obj))
            print(f"Added triple: {subj} {pred} {obj}")
    return graph


  
def insert_graph_into_named_graph(g_new: Graph, graph_uri: str, chunk_size: int = 500) -> None:
    """
    Append triples from g_new into an existing named graph using SPARQL UPDATE INSERT DATA.
    Does NOT delete/replace existing data.

    :param g_new: rdflib.Graph containing only the new triples to insert
    :param graph_uri: target named graph URI (string)
    :param chunk_size: number of triples per INSERT batch (avoid huge updates)
    """
    # Convert the new triples to N-Triples lines (safe to embed in SPARQL)
    nt_bytes = g_new.serialize(format="nt")
    nt_str = nt_bytes.decode("utf-8") if isinstance(nt_bytes, (bytes, bytearray)) else nt_bytes

    lines = [ln for ln in nt_str.splitlines() if ln.strip()]
    if not lines:
        print("No new triples to insert.")
        return

    sparql = SPARQLWrapper(settings.update_endpoint)
    sparql.setMethod("POST")
    sparql.setRequestMethod("urlencoded")

    # Chunk the payload into multiple INSERT DATA blocks
    for i in range(0, len(lines), chunk_size):
        block = "\n".join(lines[i:i+chunk_size])
        query = f"""
        INSERT DATA {{
          GRAPH <{graph_uri}> {{
            {block}
          }}
        }}
        """
        sparql.setQuery(query)
        res = sparql.query()
        print(f"Inserted {min(i+chunk_size, len(lines))}/{len(lines)} triples; HTTP {res.response.status}")
        
def publish_graph_to_endpoint(g: Graph, graph_uri: str | None = None) -> bool:
    """Insert the graph into the triplestore endpoint."""
    # url = f"{settings.sparql_endpoint}/store?{graph_uri}"
    url = f"{settings.sparql_endpoint}/store"
    if graph_uri:
        url += f"?graph={graph_uri}"
        print(f"URL: {url}")
    headers = {"Content-Type": "application/trig"}
    g.serialize("/tmp/upload-data.trig", format="trig")
    with open("/tmp/upload-data.trig", "rb") as file:
        response = requests.post(url, headers=headers, data=file, timeout=300)
        print(f"Response: {response}")
    # NOTE: Fails when we pass RDF as string directly
    # response = requests.post(url, headers=headers, data=graph_data)
    # Check response status and print result
    if not response.ok:
        print(f"Failed to upload data: {response.status_code}, {response.text}")
    return response.ok

def variable_exists(cohort_uri, variable_name) -> bool:
    sparql = SPARQLWrapper(settings.query_endpoint)
    variable_name = normalize_text(variable_name)
    sparql.setReturnFormat(JSON)
    # cohort_name = cohort_uri.split('/')[-1]
    # study_variable_design_specification_uri = f"{cohort_uri}/study_design_variable_specification"
    # print(f"cohort name: {cohort_name}")
    query = f"""
            PREFIX cmeo: <https://w3id.org/CMEO/>
            PREFIX bfo: <http://purl.obolibrary.org/obo/bfo.owl/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            ASK WHERE {{
                GRAPH <{cohort_uri}> {{
                    ?variable rdf:type cmeo:data_element ;
                            dc:identifier "{variable_name}" ;
                            bfo:is_part_of ?variable_spec_uri .
                }}
            }}
    """
    # print(f"Query: {query}")        
        # print(f"SPARQL Query: {query}")
    sparql.setQuery(query)
    # print(f"Query: {query}")
    results = sparql.query().convert()
    
   # print(f"Results: {results}")
    if results['boolean'] == True:
        print(f"Variable {variable_name} exists in the graph.")
    return results['boolean']


def load_dictionary( filepath=None) -> pd.DataFrame:
        """Loads the input dataset."""
        if filepath.endswith('.sav'):
            df_input = pd.read_spss(filepath)
            # Optionally save to Excel if needed
         
        elif filepath.endswith('.csv'):
            df_input = pd.read_csv(filepath, low_memory=False)
        elif filepath.endswith('.xlsx'):
            df_input = pd.read_excel(filepath, sheet_name=0)
        else:
            raise ValueError("Unsupported file format.")
        if not df_input.empty:
            return df_input
        else:
            return None
   
   