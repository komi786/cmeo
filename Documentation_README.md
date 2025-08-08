# CMEO Ontology Documentation

This directory contains comprehensive documentation for the Clinical Metadata Exploration Ontology (CMEO).

## 📁 Files Overview

### HTML Documentation
- **`CMEO_Documentation.html`** (50KB) - Basic HTML documentation with clean, simple design
- **`CMEO_Enhanced_Documentation.html`** (71KB) - Enhanced HTML documentation with categorized classes, modern styling, and interactive features
- **`CMEO_Complete_Documentation.html`** (115KB) - Complete HTML documentation with all properties (CMEO + imported ontologies), categorized by namespace

### Markdown Documentation
- **`CMEO_Documentation.md`** - Main documentation with comprehensive overview
- **`CMEO_Technical_Specification.md`** - Detailed technical specifications
- **`CMEO_Quick_Reference.md`** - Quick reference guide for users

### Python Scripts
- **`generate_html_docs.py`** - Script to generate basic HTML documentation
- **`generate_enhanced_html.py`** - Script to generate enhanced HTML documentation with categorization
- **`generate_complete_html.py`** - Script to generate complete HTML documentation with all properties
- **`open_docs.py`** - Script to open HTML files in web browser

## 🚀 Quick Start

### View Documentation
1. **Open in Browser**: Run `python open_docs.py` to open both HTML files in your default browser
2. **Manual Opening**: Double-click on any `.html` file to open in your browser

### Generate Documentation
1. **Basic HTML**: `python generate_html_docs.py`
2. **Enhanced HTML**: `python generate_enhanced_html.py`
3. **Complete HTML**: `python generate_complete_html.py`

## 📊 Documentation Features

### HTML Documentation
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Interactive Navigation**: Sticky navigation bar with smooth scrolling
- **Categorized Classes**: Classes organized into logical categories
- **Statistics Dashboard**: Visual statistics cards
- **Modern Styling**: Gradient backgrounds, hover effects, and clean typography

### Enhanced Features
- **Class Categorization**: 19 categories including Data Standards, Measurements, Statistical Measures, etc.
- **Table of Contents**: Easy navigation to different sections
- **Property Documentation**: Separate sections for Object and Data Properties
- **Visual Hierarchy**: Clear visual distinction between different types of information

## 📈 Statistics

The CMEO ontology contains:
- **117 Classes** across 19 categories
- **69 Object Properties** (2 CMEO + 67 imported from BFO, IAO, OBI, RO)
- **1 Data Property** (CMEO)
- **Comprehensive annotations** and documentation

## 🎨 Design Features

### Enhanced HTML Documentation
- **Gradient Backgrounds**: Modern gradient color schemes
- **Card-based Layout**: Information organized in clean cards
- **Hover Effects**: Interactive elements with smooth transitions
- **Color-coded Categories**: Different colors for different class categories
- **Responsive Grid**: Automatically adjusts to screen size
- **Sticky Navigation**: Navigation bar stays at top while scrolling

### Color Scheme
- **Primary Blue**: #3498db (navigation, links)
- **Dark Blue**: #2c3e50 (headers, text)
- **Light Gray**: #ecf0f1 (backgrounds, cards)
- **Accent Colors**: Different colors for different categories

## 🔧 Technical Details

### Generated Files
- **File Size**: Basic HTML ~50KB, Enhanced HTML ~70KB
- **Encoding**: UTF-8
- **Format**: HTML5 with CSS3
- **Compatibility**: Modern browsers (Chrome, Firefox, Safari, Edge)

### Dependencies
- **rdflib**: For parsing RDF/OWL files
- **Python 3.x**: Required for running scripts
- **Web Browser**: For viewing HTML documentation

## 📋 Usage Instructions

### For Users
1. Open `CMEO_Enhanced_Documentation.html` for the best experience
2. Use the navigation bar to jump to different sections
3. Browse classes by category using the table of contents
4. View statistics and overview information

### For Developers
1. Modify `generate_enhanced_html.py` to customize the HTML output
2. Add new categories or modify existing ones in the `categorize_classes()` function
3. Update styling in the `generate_enhanced_html()` function
4. Run the script to regenerate documentation

### For Ontology Maintainers
1. Update the RDF file (`cmeo_v3_05_08_2025.rdf`)
2. Run the generation scripts to update documentation
3. Review the generated HTML files
4. Commit changes to version control

## 🎯 Key Features

### Enhanced HTML Documentation
- ✅ **Categorized Classes**: 19 logical categories
- ✅ **Interactive Navigation**: Smooth scrolling and sticky nav
- ✅ **Responsive Design**: Works on all devices
- ✅ **Modern Styling**: Gradient backgrounds and hover effects
- ✅ **Statistics Dashboard**: Visual overview of ontology size
- ✅ **Property Documentation**: Separate sections for properties
- ✅ **Table of Contents**: Easy navigation
- ✅ **Accessibility**: High contrast and readable fonts

### Basic HTML Documentation
- ✅ **Simple Layout**: Clean and straightforward
- ✅ **All Classes Listed**: Complete class documentation
- ✅ **Property Information**: Object and data properties
- ✅ **Basic Styling**: Professional appearance
- ✅ **Fast Loading**: Lightweight and quick to load

## 🔄 Maintenance

### Updating Documentation
1. Make changes to the RDF ontology file
2. Run the appropriate generation script
3. Review the generated HTML files
4. Test in different browsers
5. Commit changes to version control

### Customization
- Modify the CSS styles in the generation scripts
- Add new categories or modify existing ones
- Change the color scheme or layout
- Add additional metadata or information

## 📞 Support

For questions or issues with the documentation:
- Check the generated HTML files for errors
- Review the Python scripts for syntax issues
- Ensure the RDF file is valid and well-formed
- Test in different browsers for compatibility

---

*This documentation provides comprehensive information about the CMEO ontology and its various documentation formats.*
