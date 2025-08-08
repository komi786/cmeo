#!/usr/bin/env python3
"""
Generate comprehensive ontology documentation using Ontospy
for the Clinical Metadata Exploration Ontology (CMEO)
"""

import os
import sys
import webbrowser
from pathlib import Path
from ontospy import Ontospy
from ontospy.core import *
from ontospy.core.manager import *
from ontospy.core.utils import *
from ontospy.core.actions import *
from ontospy.core.actions.console import *
from ontospy.core.actions.html import *
from ontospy.core.actions.rdf import *
from ontospy.core.actions.sparql import *
from ontospy.core.actions.stats import *
from ontospy.core.actions.visualize import *

def generate_ontospy_documentation():
    """Generate comprehensive documentation using Ontospy"""
    
    # Configuration
    ontology_file = "cmeo_v3_05_08_2025.rdf"
    output_dir = "ontospy_docs"
    
    print("🔍 Loading CMEO ontology with Ontospy...")
    
    try:
        # Load the ontology
        onto = Ontospy(ontology_file)
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"✅ Ontology loaded successfully!")
        print(f"📊 Ontology statistics:")
        print(f"   - Classes: {len(onto.all_classes)}")
        print(f"   - Object Properties: {len(onto.all_object_properties)}")
        print(f"   - Data Properties: {len(onto.all_data_properties)}")
        print(f"   - Individuals: {len(onto.all_individuals)}")
        
        # Generate HTML documentation
        print("\n📄 Generating HTML documentation...")
        html_generator = HTMLGenerator(onto)
        html_output = html_generator.build()
        
        # Save HTML documentation
        html_file = os.path.join(output_dir, "cmeo_ontospy_documentation.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        print(f"✅ HTML documentation saved to: {html_file}")
        
        # Generate statistics
        print("\n📈 Generating statistics...")
        stats_generator = StatsGenerator(onto)
        stats_output = stats_generator.build()
        
        stats_file = os.path.join(output_dir, "cmeo_statistics.txt")
        with open(stats_file, 'w', encoding='utf-8') as f:
            f.write(stats_output)
        
        print(f"✅ Statistics saved to: {stats_file}")
        
        # Generate console output
        print("\n💻 Generating console documentation...")
        console_generator = ConsoleGenerator(onto)
        console_output = console_generator.build()
        
        console_file = os.path.join(output_dir, "cmeo_console_documentation.txt")
        with open(console_file, 'w', encoding='utf-8') as f:
            f.write(console_output)
        
        print(f"✅ Console documentation saved to: {console_file}")
        
        # Generate RDF documentation
        print("\n🔗 Generating RDF documentation...")
        rdf_generator = RDFGenerator(onto)
        rdf_output = rdf_generator.build()
        
        rdf_file = os.path.join(output_dir, "cmeo_rdf_documentation.ttl")
        with open(rdf_file, 'w', encoding='utf-8') as f:
            f.write(rdf_output)
        
        print(f"✅ RDF documentation saved to: {rdf_file}")
        
        # Generate SPARQL queries
        print("\n🔍 Generating SPARQL queries...")
        sparql_generator = SPARQLGenerator(onto)
        sparql_output = sparql_generator.build()
        
        sparql_file = os.path.join(output_dir, "cmeo_sparql_queries.txt")
        with open(sparql_file, 'w', encoding='utf-8') as f:
            f.write(sparql_output)
        
        print(f"✅ SPARQL queries saved to: {sparql_file}")
        
        # Generate visualization
        print("\n🎨 Generating visualization...")
        viz_generator = VisualizeGenerator(onto)
        viz_output = viz_generator.build()
        
        viz_file = os.path.join(output_dir, "cmeo_visualization.html")
        with open(viz_file, 'w', encoding='utf-8') as f:
            f.write(viz_output)
        
        print(f"✅ Visualization saved to: {viz_file}")
        
        # Create index file
        create_index_file(output_dir)
        
        print(f"\n🎉 Documentation generation complete!")
        print(f"📁 All files saved to: {output_dir}/")
        
        # Open the main HTML documentation
        print("\n🌐 Opening HTML documentation in browser...")
        webbrowser.open(f"file://{os.path.abspath(html_file)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating documentation: {e}")
        return False

def create_index_file(output_dir):
    """Create an index file with links to all generated documentation"""
    
    index_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CMEO Ontology Documentation - Ontospy Generated</title>
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
        .stats {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .stats h3 {
            margin: 0 0 20px 0;
            text-align: center;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
        }
        .stat-item {
            text-align: center;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            display: block;
        }
        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>CMEO Ontology Documentation</h1>
            <p>Clinical Metadata Exploration Ontology - Generated with Ontospy</p>
        </div>
        
        <div class="content">
            <div class="stats">
                <h3>📊 Ontology Statistics</h3>
                <div class="stats-grid">
                    <div class="stat-item">
                        <span class="stat-number">117</span>
                        <span class="stat-label">Classes</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">69</span>
                        <span class="stat-label">Object Properties</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">1</span>
                        <span class="stat-label">Data Properties</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">0</span>
                        <span class="stat-label">Individuals</span>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>📄 Documentation Files</h2>
                <div class="file-grid">
                    <a href="cmeo_ontospy_documentation.html" class="file-card">
                        <div class="file-type">HTML</div>
                        <h3>Main Documentation</h3>
                        <p>Comprehensive HTML documentation with all classes, properties, and relationships</p>
                    </a>
                    
                    <a href="cmeo_visualization.html" class="file-card">
                        <div class="file-type">HTML</div>
                        <h3>Ontology Visualization</h3>
                        <p>Interactive visualization of the ontology structure and relationships</p>
                    </a>
                    
                    <a href="cmeo_statistics.txt" class="file-card">
                        <div class="file-type">TXT</div>
                        <h3>Statistics Report</h3>
                        <p>Detailed statistics and metrics about the ontology</p>
                    </a>
                    
                    <a href="cmeo_console_documentation.txt" class="file-card">
                        <div class="file-type">TXT</div>
                        <h3>Console Documentation</h3>
                        <p>Text-based documentation suitable for command-line viewing</p>
                    </a>
                    
                    <a href="cmeo_rdf_documentation.ttl" class="file-card">
                        <div class="file-type">TTL</div>
                        <h3>RDF Documentation</h3>
                        <p>RDF/Turtle format documentation of the ontology</p>
                    </a>
                    
                    <a href="cmeo_sparql_queries.txt" class="file-card">
                        <div class="file-type">TXT</div>
                        <h3>SPARQL Queries</h3>
                        <p>Useful SPARQL queries for exploring the ontology</p>
                    </a>
                </div>
            </div>
            
            <div class="section">
                <h2>🔧 About This Documentation</h2>
                <p>This documentation was generated using <strong>Ontospy</strong>, a powerful Python library for ontology analysis and documentation generation. The documentation includes:</p>
                <ul>
                    <li><strong>HTML Documentation:</strong> Complete web-based documentation with navigation and search</li>
                    <li><strong>Visualization:</strong> Interactive graphs showing ontology structure</li>
                    <li><strong>Statistics:</strong> Detailed metrics about classes, properties, and relationships</li>
                    <li><strong>SPARQL Queries:</strong> Ready-to-use queries for ontology exploration</li>
                    <li><strong>RDF Output:</strong> Machine-readable documentation in Turtle format</li>
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

if __name__ == "__main__":
    print("🚀 Starting CMEO Ontology Documentation Generation with Ontospy")
    print("=" * 60)
    
    success = generate_ontospy_documentation()
    
    if success:
        print("\n✅ Documentation generation completed successfully!")
        print("📁 Check the 'ontospy_docs' directory for all generated files")
    else:
        print("\n❌ Documentation generation failed!")
        sys.exit(1)
