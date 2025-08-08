#!/usr/bin/env python3
"""
Generate comprehensive ontology documentation using rdflib
for the Clinical Metadata Exploration Ontology (CMEO)
"""

import os
import sys
import webbrowser
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef, Literal
from rdflib.namespace import DC, DCTERMS, SKOS
import json
from datetime import datetime

def load_ontology():
    """Load the CMEO ontology"""
    print("🔍 Loading CMEO ontology...")
    
    g = Graph()
    ontology_file = "cmeo_v3_05_08_2025.rdf"
    
    try:
        g.parse(ontology_file, format="xml")
        print(f"✅ Ontology loaded successfully from {ontology_file}")
        return g
    except Exception as e:
        print(f"❌ Error loading ontology: {e}")
        return None

def get_ontology_statistics(g):
    """Get comprehensive statistics about the ontology"""
    stats = {
        'classes': [],
        'object_properties': [],
        'data_properties': [],
        'individuals': [],
        'annotations': [],
        'namespaces': {}
    }
    
    # Get all classes
    for s, p, o in g.triples((None, RDF.type, OWL.Class)):
        if isinstance(s, URIRef):
            stats['classes'].append(str(s))
    
    # Get all object properties
    for s, p, o in g.triples((None, RDF.type, OWL.ObjectProperty)):
        if isinstance(s, URIRef):
            stats['object_properties'].append(str(s))
    
    # Get all data properties
    for s, p, o in g.triples((None, RDF.type, OWL.DatatypeProperty)):
        if isinstance(s, URIRef):
            stats['data_properties'].append(str(s))
    
    # Get all individuals
    for s, p, o in g.triples((None, RDF.type, OWL.NamedIndividual)):
        if isinstance(s, URIRef):
            stats['individuals'].append(str(s))
    
    # Get namespaces
    for prefix, namespace in g.namespaces():
        stats['namespaces'][prefix] = str(namespace)
    
    return stats

def get_class_details(g, class_uri):
    """Get detailed information about a class"""
    details = {
        'uri': class_uri,
        'label': '',
        'comment': '',
        'subclass_of': [],
        'superclass_of': [],
        'equivalent_to': [],
        'disjoint_with': [],
        'restrictions': [],
        'annotations': {}
    }
    
    # Get label
    for s, p, o in g.triples((URIRef(class_uri), RDFS.label, None)):
        if isinstance(o, Literal):
            details['label'] = str(o)
    
    # Get comment
    for s, p, o in g.triples((URIRef(class_uri), RDFS.comment, None)):
        if isinstance(o, Literal):
            details['comment'] = str(o)
    
    # Get subclasses
    for s, p, o in g.triples((URIRef(class_uri), RDFS.subClassOf, None)):
        if isinstance(o, URIRef):
            details['subclass_of'].append(str(o))
    
    # Get superclasses
    for s, p, o in g.triples((None, RDFS.subClassOf, URIRef(class_uri))):
        if isinstance(s, URIRef):
            details['superclass_of'].append(str(s))
    
    # Get equivalent classes
    for s, p, o in g.triples((URIRef(class_uri), OWL.equivalentClass, None)):
        if isinstance(o, URIRef):
            details['equivalent_to'].append(str(o))
    
    # Get disjoint classes
    for s, p, o in g.triples((URIRef(class_uri), OWL.disjointWith, None)):
        if isinstance(o, URIRef):
            details['disjoint_with'].append(str(o))
    
    # Get other annotations
    for s, p, o in g.triples((URIRef(class_uri), None, None)):
        if p not in [RDF.type, RDFS.label, RDFS.comment, RDFS.subClassOf, OWL.equivalentClass, OWL.disjointWith]:
            if isinstance(o, Literal):
                details['annotations'][str(p)] = str(o)
    
    return details

def get_property_details(g, property_uri):
    """Get detailed information about a property"""
    details = {
        'uri': property_uri,
        'label': '',
        'comment': '',
        'domain': [],
        'range': [],
        'subproperty_of': [],
        'superproperty_of': [],
        'equivalent_to': [],
        'inverse_of': [],
        'annotations': {}
    }
    
    # Get label
    for s, p, o in g.triples((URIRef(property_uri), RDFS.label, None)):
        if isinstance(o, Literal):
            details['label'] = str(o)
    
    # Get comment
    for s, p, o in g.triples((URIRef(property_uri), RDFS.comment, None)):
        if isinstance(o, Literal):
            details['comment'] = str(o)
    
    # Get domain
    for s, p, o in g.triples((URIRef(property_uri), RDFS.domain, None)):
        if isinstance(o, URIRef):
            details['domain'].append(str(o))
    
    # Get range
    for s, p, o in g.triples((URIRef(property_uri), RDFS.range, None)):
        if isinstance(o, URIRef):
            details['range'].append(str(o))
    
    # Get subproperties
    for s, p, o in g.triples((URIRef(property_uri), RDFS.subPropertyOf, None)):
        if isinstance(o, URIRef):
            details['subproperty_of'].append(str(o))
    
    # Get superproperties
    for s, p, o in g.triples((None, RDFS.subPropertyOf, URIRef(property_uri))):
        if isinstance(s, URIRef):
            details['superproperty_of'].append(str(s))
    
    # Get equivalent properties
    for s, p, o in g.triples((URIRef(property_uri), OWL.equivalentProperty, None)):
        if isinstance(o, URIRef):
            details['equivalent_to'].append(str(o))
    
    # Get inverse properties
    for s, p, o in g.triples((URIRef(property_uri), OWL.inverseOf, None)):
        if isinstance(o, URIRef):
            details['inverse_of'].append(str(o))
    
    # Get other annotations
    for s, p, o in g.triples((URIRef(property_uri), None, None)):
        if p not in [RDF.type, RDFS.label, RDFS.comment, RDFS.domain, RDFS.range, RDFS.subPropertyOf, OWL.equivalentProperty, OWL.inverseOf]:
            if isinstance(o, Literal):
                details['annotations'][str(p)] = str(o)
    
    return details

def generate_html_documentation(g, stats, output_dir):
    """Generate comprehensive HTML documentation"""
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CMEO Ontology Documentation</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            border-radius: 15px;
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .nav {{
            background: #34495e;
            padding: 15px 40px;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        
        .nav ul {{
            list-style: none;
            display: flex;
            gap: 30px;
            flex-wrap: wrap;
        }}
        
        .nav a {{
            color: white;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 20px;
            transition: all 0.3s ease;
        }}
        
        .nav a:hover {{
            background: #3498db;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 50px;
        }}
        
        .section h2 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
            font-size: 1.8em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            display: block;
        }}
        
        .stat-label {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .class-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
        }}
        
        .class-card {{
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 10px;
            padding: 20px;
            transition: all 0.3s ease;
        }}
        
        .class-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }}
        
        .class-name {{
            color: #2c3e50;
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        .class-comment {{
            color: #6c757d;
            margin-bottom: 15px;
            font-style: italic;
        }}
        
        .class-details {{
            font-size: 0.9em;
        }}
        
        .class-details strong {{
            color: #2c3e50;
        }}
        
        .property-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
        }}
        
        .property-card {{
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 10px;
            padding: 20px;
            transition: all 0.3s ease;
        }}
        
        .property-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }}
        
        .property-name {{
            color: #2c3e50;
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        .namespace-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        .namespace-table th,
        .namespace-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .namespace-table th {{
            background: #f8f9fa;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .uri {{
            font-family: monospace;
            background: #f1f3f4;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.9em;
        }}
        
        .timestamp {{
            text-align: center;
            color: #6c757d;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e9ecef;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>CMEO Ontology Documentation</h1>
            <p>Clinical Metadata Exploration Ontology - Comprehensive Documentation</p>
        </div>
        
        <nav class="nav">
            <ul>
                <li><a href="#overview">Overview</a></li>
                <li><a href="#classes">Classes</a></li>
                <li><a href="#object-properties">Object Properties</a></li>
                <li><a href="#data-properties">Data Properties</a></li>
                <li><a href="#namespaces">Namespaces</a></li>
            </ul>
        </nav>
        
        <div class="content">
            <section id="overview" class="section">
                <h2>📊 Ontology Overview</h2>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <span class="stat-number">{len(stats['classes'])}</span>
                        <span class="stat-label">Classes</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">{len(stats['object_properties'])}</span>
                        <span class="stat-label">Object Properties</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">{len(stats['data_properties'])}</span>
                        <span class="stat-label">Data Properties</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">{len(stats['individuals'])}</span>
                        <span class="stat-label">Individuals</span>
                    </div>
                </div>
                
                <p>This documentation provides a comprehensive overview of the Clinical Metadata Exploration Ontology (CMEO), including all classes, properties, and their relationships. The ontology is designed to support clinical metadata exploration and analysis.</p>
            </section>
            
            <section id="classes" class="section">
                <h2>🏗️ Classes</h2>
                <p>The ontology contains {len(stats['classes'])} classes that represent various aspects of clinical metadata and data standards.</p>
                
                <div class="class-grid">"""
    
    # Add classes
    for class_uri in stats['classes']:
        details = get_class_details(g, class_uri)
        
        html_content += f"""
                    <div class="class-card">
                        <div class="class-name">{details['label'] or class_uri.split('/')[-1]}</div>
                        <div class="class-comment">{details['comment']}</div>
                        <div class="class-details">
                            <strong>URI:</strong> <span class="uri">{class_uri}</span><br>"""
        
        if details['subclass_of']:
            html_content += f"<strong>Subclass of:</strong> {', '.join([f'<span class="uri">{uri.split("/")[-1]}</span>' for uri in details['subclass_of']])}<br>"
        
        if details['equivalent_to']:
            html_content += f"<strong>Equivalent to:</strong> {', '.join([f'<span class="uri">{uri.split("/")[-1]}</span>' for uri in details['equivalent_to']])}<br>"
        
        if details['disjoint_with']:
            html_content += f"<strong>Disjoint with:</strong> {', '.join([f'<span class="uri">{uri.split("/")[-1]}</span>' for uri in details['disjoint_with']])}<br>"
        
        html_content += """
                        </div>
                    </div>"""
    
    html_content += """
                </div>
            </section>
            
            <section id="object-properties" class="section">
                <h2>🔗 Object Properties</h2>
                <p>The ontology contains {len(stats['object_properties'])} object properties that define relationships between classes.</p>
                
                <div class="property-grid">"""
    
    # Add object properties
    for prop_uri in stats['object_properties']:
        details = get_property_details(g, prop_uri)
        
        html_content += f"""
                    <div class="property-card">
                        <div class="property-name">{details['label'] or prop_uri.split('/')[-1]}</div>
                        <div class="class-comment">{details['comment']}</div>
                        <div class="class-details">
                            <strong>URI:</strong> <span class="uri">{prop_uri}</span><br>"""
        
        if details['domain']:
            html_content += f"<strong>Domain:</strong> {', '.join([f'<span class="uri">{uri.split("/")[-1]}</span>' for uri in details['domain']])}<br>"
        
        if details['range']:
            html_content += f"<strong>Range:</strong> {', '.join([f'<span class="uri">{uri.split("/")[-1]}</span>' for uri in details['range']])}<br>"
        
        if details['subproperty_of']:
            html_content += f"<strong>Subproperty of:</strong> {', '.join([f'<span class="uri">{uri.split("/")[-1]}</span>' for uri in details['subproperty_of']])}<br>"
        
        html_content += """
                        </div>
                    </div>"""
    
    html_content += """
                </div>
            </section>
            
            <section id="data-properties" class="section">
                <h2>📝 Data Properties</h2>
                <p>The ontology contains {len(stats['data_properties'])} data properties that define relationships between classes and data values.</p>
                
                <div class="property-grid">"""
    
    # Add data properties
    for prop_uri in stats['data_properties']:
        details = get_property_details(g, prop_uri)
        
        html_content += f"""
                    <div class="property-card">
                        <div class="property-name">{details['label'] or prop_uri.split('/')[-1]}</div>
                        <div class="class-comment">{details['comment']}</div>
                        <div class="class-details">
                            <strong>URI:</strong> <span class="uri">{prop_uri}</span><br>"""
        
        if details['domain']:
            html_content += f"<strong>Domain:</strong> {', '.join([f'<span class="uri">{uri.split("/")[-1]}</span>' for uri in details['domain']])}<br>"
        
        if details['range']:
            html_content += f"<strong>Range:</strong> {', '.join([f'<span class="uri">{uri.split("/")[-1]}</span>' for uri in details['range']])}<br>"
        
        html_content += """
                        </div>
                    </div>"""
    
    html_content += f"""
                </div>
            </section>
            
            <section id="namespaces" class="section">
                <h2>📚 Namespaces</h2>
                <p>The ontology uses the following namespaces:</p>
                
                <table class="namespace-table">
                    <thead>
                        <tr>
                            <th>Prefix</th>
                            <th>Namespace URI</th>
                        </tr>
                    </thead>
                    <tbody>"""
    
    for prefix, namespace in stats['namespaces'].items():
        html_content += f"""
                        <tr>
                            <td><strong>{prefix}</strong></td>
                            <td><span class="uri">{namespace}</span></td>
                        </tr>"""
    
    html_content += f"""
                    </tbody>
                </table>
            </section>
            
            <div class="timestamp">
                <p>Documentation generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Generated using rdflib and custom documentation generator</p>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    # Save HTML file
    html_file = os.path.join(output_dir, "cmeo_comprehensive_documentation.html")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML documentation saved to: {html_file}")
    return html_file

def generate_json_documentation(g, stats, output_dir):
    """Generate JSON documentation"""
    
    documentation = {
        'metadata': {
            'title': 'CMEO Ontology Documentation',
            'description': 'Clinical Metadata Exploration Ontology',
            'generated_at': datetime.now().isoformat(),
            'statistics': {
                'classes': len(stats['classes']),
                'object_properties': len(stats['object_properties']),
                'data_properties': len(stats['data_properties']),
                'individuals': len(stats['individuals'])
            }
        },
        'classes': {},
        'object_properties': {},
        'data_properties': {},
        'namespaces': stats['namespaces']
    }
    
    # Add class details
    for class_uri in stats['classes']:
        details = get_class_details(g, class_uri)
        documentation['classes'][class_uri] = details
    
    # Add object property details
    for prop_uri in stats['object_properties']:
        details = get_property_details(g, prop_uri)
        documentation['object_properties'][prop_uri] = details
    
    # Add data property details
    for prop_uri in stats['data_properties']:
        details = get_property_details(g, prop_uri)
        documentation['data_properties'][prop_uri] = details
    
    # Save JSON file
    json_file = os.path.join(output_dir, "cmeo_documentation.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(documentation, f, indent=2, ensure_ascii=False)
    
    print(f"✅ JSON documentation saved to: {json_file}")

def generate_markdown_documentation(g, stats, output_dir):
    """Generate Markdown documentation"""
    
    md_content = f"""# CMEO Ontology Documentation

## Overview

The Clinical Metadata Exploration Ontology (CMEO) is a comprehensive ontology designed to support clinical metadata exploration and analysis.

## Statistics

- **Classes**: {len(stats['classes'])}
- **Object Properties**: {len(stats['object_properties'])}
- **Data Properties**: {len(stats['data_properties'])}
- **Individuals**: {len(stats['individuals'])}

## Classes

The ontology contains the following classes:

"""
    
    for class_uri in stats['classes']:
        details = get_class_details(g, class_uri)
        label = details['label'] or class_uri.split('/')[-1]
        comment = details['comment']
        
        md_content += f"### {label}\n\n"
        if comment:
            md_content += f"*{comment}*\n\n"
        md_content += f"**URI**: `{class_uri}`\n\n"
        
        if details['subclass_of']:
            md_content += f"**Subclass of**: {', '.join([f'`{uri.split("/")[-1]}`' for uri in details['subclass_of']])}\n\n"
        
        if details['equivalent_to']:
            md_content += f"**Equivalent to**: {', '.join([f'`{uri.split("/")[-1]}`' for uri in details['equivalent_to']])}\n\n"
        
        md_content += "---\n\n"
    
    md_content += "## Object Properties\n\n"
    
    for prop_uri in stats['object_properties']:
        details = get_property_details(g, prop_uri)
        label = details['label'] or prop_uri.split('/')[-1]
        comment = details['comment']
        
        md_content += f"### {label}\n\n"
        if comment:
            md_content += f"*{comment}*\n\n"
        md_content += f"**URI**: `{prop_uri}`\n\n"
        
        if details['domain']:
            md_content += f"**Domain**: {', '.join([f'`{uri.split("/")[-1]}`' for uri in details['domain']])}\n\n"
        
        if details['range']:
            md_content += f"**Range**: {', '.join([f'`{uri.split("/")[-1]}`' for uri in details['range']])}\n\n"
        
        md_content += "---\n\n"
    
    md_content += "## Data Properties\n\n"
    
    for prop_uri in stats['data_properties']:
        details = get_property_details(g, prop_uri)
        label = details['label'] or prop_uri.split('/')[-1]
        comment = details['comment']
        
        md_content += f"### {label}\n\n"
        if comment:
            md_content += f"*{comment}*\n\n"
        md_content += f"**URI**: `{prop_uri}`\n\n"
        
        if details['domain']:
            md_content += f"**Domain**: {', '.join([f'`{uri.split("/")[-1]}`' for uri in details['domain']])}\n\n"
        
        if details['range']:
            md_content += f"**Range**: {', '.join([f'`{uri.split("/")[-1]}`' for uri in details['range']])}\n\n"
        
        md_content += "---\n\n"
    
    md_content += "## Namespaces\n\n"
    
    for prefix, namespace in stats['namespaces'].items():
        md_content += f"- **{prefix}**: `{namespace}`\n"
    
    md_content += f"\n---\n\n*Documentation generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
    
    # Save Markdown file
    md_file = os.path.join(output_dir, "cmeo_documentation.md")
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"✅ Markdown documentation saved to: {md_file}")

def create_index_file(output_dir):
    """Create an index file with links to all generated documentation"""
    
    index_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CMEO Ontology Documentation - Index</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        .header p {
            margin: 10px 0 0 0;
            font-size: 1.2em;
            opacity: 0.9;
        }
        .content {
            padding: 40px;
        }
        .section {
            margin-bottom: 40px;
        }
        .section h2 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .file-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .file-card {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 10px;
            padding: 20px;
            transition: all 0.3s ease;
            text-decoration: none;
            color: inherit;
        }
        .file-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            border-color: #3498db;
        }
        .file-card h3 {
            color: #2c3e50;
            margin: 0 0 10px 0;
            font-size: 1.2em;
        }
        .file-card p {
            color: #6c757d;
            margin: 0;
            font-size: 0.9em;
        }
        .file-type {
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>CMEO Ontology Documentation</h1>
            <p>Clinical Metadata Exploration Ontology - Generated with rdflib</p>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>📄 Documentation Files</h2>
                <div class="file-grid">
                    <a href="cmeo_comprehensive_documentation.html" class="file-card">
                        <div class="file-type">HTML</div>
                        <h3>Comprehensive Documentation</h3>
                        <p>Complete HTML documentation with all classes, properties, and relationships</p>
                    </a>
                    
                    <a href="cmeo_documentation.json" class="file-card">
                        <div class="file-type">JSON</div>
                        <h3>JSON Documentation</h3>
                        <p>Machine-readable documentation in JSON format</p>
                    </a>
                    
                    <a href="cmeo_documentation.md" class="file-card">
                        <div class="file-type">Markdown</div>
                        <h3>Markdown Documentation</h3>
                        <p>Text-based documentation in Markdown format</p>
                    </a>
                </div>
            </div>
            
            <div class="section">
                <h2>🔧 About This Documentation</h2>
                <p>This documentation was generated using <strong>rdflib</strong>, a powerful Python library for RDF processing. The documentation includes:</p>
                <ul>
                    <li><strong>HTML Documentation:</strong> Complete web-based documentation with navigation and search</li>
                    <li><strong>JSON Documentation:</strong> Machine-readable format for programmatic access</li>
                    <li><strong>Markdown Documentation:</strong> Text-based format suitable for version control</li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    index_file = os.path.join(output_dir, "index.html")
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"✅ Index file created: {index_file}")

def main():
    """Main function to generate documentation"""
    
    print("🚀 Starting CMEO Ontology Documentation Generation with rdflib")
    print("=" * 60)
    
    # Load ontology
    g = load_ontology()
    if not g:
        print("❌ Failed to load ontology")
        sys.exit(1)
    
    # Get statistics
    stats = get_ontology_statistics(g)
    print(f"📊 Ontology statistics:")
    print(f"   - Classes: {len(stats['classes'])}")
    print(f"   - Object Properties: {len(stats['object_properties'])}")
    print(f"   - Data Properties: {len(stats['data_properties'])}")
    print(f"   - Individuals: {len(stats['individuals'])}")
    print(f"   - Namespaces: {len(stats['namespaces'])}")
    
    # Create output directory
    output_dir = "rdflib_docs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate documentation
    print("\n📄 Generating documentation...")
    
    # Generate HTML documentation
    html_file = generate_html_documentation(g, stats, output_dir)
    
    # Generate JSON documentation
    generate_json_documentation(g, stats, output_dir)
    
    # Generate Markdown documentation
    generate_markdown_documentation(g, stats, output_dir)
    
    # Create index file
    create_index_file(output_dir)
    
    print(f"\n🎉 Documentation generation complete!")
    print(f"📁 All files saved to: {output_dir}/")
    
    # Open the main HTML documentation
    print("\n🌐 Opening HTML documentation in browser...")
    webbrowser.open(f"file://{os.path.abspath(html_file)}")
    
    return True

if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n❌ Documentation generation failed!")
        sys.exit(1)
