# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

BridgeGAD-03 is a comprehensive bridge design and CAD generation application built with Python/Streamlit. It transforms civil engineering bridge design calculations into professional-quality DXF drawings. The project includes multiple implementations and enhancements focused on structural engineering automation.

## Development Commands

### Python Environment Setup
```powershell
# Create and activate virtual environment
python -m venv bridgegad_env
.\bridgegad_env\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Running Applications
```powershell
# Main bridge design app
streamlit run app.py

# Enhanced bridge application (professional CAD output)
streamlit run enhanced_bridge_app.py

# Enhanced CAD-focused application
streamlit run enhanced_bridge_cad_app.py

# BridgeDesignPro module (modular architecture)
cd BridgeDesignPro
streamlit run app.py
```

### Development Tools
```powershell
# Create sample input files
python create_sample_input.py

# Run setup scripts
.\setup.bat          # Windows
bash setup.sh        # Linux/Mac
```

## Architecture Overview

### Core Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **CAD Engine**: ezdxf (DXF file generation)
- **Data Processing**: pandas, numpy
- **Engineering Calculations**: Custom Python modules
- **File Handling**: openpyxl (Excel integration)

### Application Variants

1. **app.py**: Basic bridge design interface with Excel parameter input
2. **enhanced_bridge_app.py**: Enhanced UI with professional styling and improved UX
3. **enhanced_bridge_cad_app.py**: Advanced CAD generation with professional drawing standards
4. **BridgeDesignPro/**: Modular architecture with separate design modules

### Key Engineering Modules

- **Bridge Geometry**: Span calculations, alignment, and geometric design
- **Abutment Design**: Retaining wall and foundation design calculations
- **Approach Slab Design**: Deck slab design and reinforcement calculations
- **CAD Generation**: Professional DXF output with layers, dimensions, and annotations

## File Structure Patterns

### Input Files
- **Excel Templates**: `bridge_parameters_template.xlsx`, `input.xlsx`
  - Sheet1: Bridge parameters (Value, Variable, Description columns)
  - Sheet2: Cross-section data (Chainage, RL columns)

### Output Files
- **DXF Drawings**: Professional CAD files with organized layers
- **Generated Names**: `{project_name}_bridge_drawing.dxf`

### Key Source Files
```
├── app.py                      # Main application entry point
├── enhanced_bridge_app.py      # Enhanced version with modern UI
├── enhanced_bridge_cad_app.py  # Professional CAD output version
├── BridgeDesignPro/           # Modular architecture implementation
│   ├── app.py                 # Main modular app
│   ├── bridge_geometry.py     # Geometric calculations
│   ├── abutment_design.py     # Abutment design module
│   └── approach_slab_design.py # Approach slab calculations
├── cad_utils.py               # CAD generation utilities
├── abutment_design.py         # Standalone abutment calculations
├── approach_slab_design.py    # Standalone approach slab calculations
└── requirements.txt           # Python dependencies
```

## Engineering Features

### Bridge Design Capabilities
- **Multi-span continuous bridges**
- **Skew bridge support** (angular crossings)
- **Variable span lengths**
- **Professional elevation and plan drawings**
- **Pier and abutment design**
- **Approach slab integration**

### CAD Output Standards
- **Professional Layers**: STRUCTURE, DIMENSIONS, TEXT, GRID, HATCHING
- **Industry Standards**: DXF R2010 format compatible with AutoCAD, Civil 3D
- **Professional Dimensioning**: Automatic dimension generation with proper styling
- **Text Hierarchy**: Multiple text styles for titles, annotations, dimensions
- **Concrete Hatching**: ANSI31 standard patterns for structural sections

### Calculation Standards
- **IS 456:2000**: Indian concrete code compliance
- **IRC Standards**: Indian Roads Congress bridge design guidelines
- **Load Factor Design**: Modern structural design approach
- **Reinforcement Detailing**: Steel area calculations and bar layouts

## Development Notes

### Key Dependencies
```python
streamlit==1.31.0     # Web framework
pandas==2.1.4         # Data manipulation
ezdxf==1.1.3         # DXF file generation
openpyxl==3.1.2      # Excel file handling
numpy==1.26.3        # Numerical computations
plotly==5.17.0       # Interactive plotting
matplotlib==3.8.2    # Static plotting
```

### Input Parameter Pattern
Bridge parameters follow a standardized Excel format:
- **Variable Names**: NSPAN, SPAN1, LBRIDGE, SKEW, RTL, SOFL
- **Geometry**: Cap dimensions (CAPT, CAPB, CAPW), pier dimensions (PIERTW, BATTR)
- **Levels**: Foundation level (FUTRL), footing dimensions (FUTD, FUTW, FUTL)

### CAD Generation Pattern
1. **Parameter Validation**: Check input completeness and ranges
2. **Geometry Calculation**: Compute derived dimensions and coordinates
3. **Layer Setup**: Create professional layer structure
4. **Drawing Generation**: Generate elevation, plan, and section views
5. **Annotation**: Add dimensions, text, and title blocks
6. **File Export**: Save as DXF with proper formatting

### Error Handling Standards
- **Input Validation**: Comprehensive parameter checking with user-friendly messages
- **File Handling**: Graceful handling of missing or corrupted files
- **CAD Generation**: Robust error recovery during drawing creation
- **Progress Indicators**: Real-time feedback during long operations

## Common Development Tasks

### Adding New Bridge Types
1. Extend geometry calculation functions in bridge modules
2. Update CAD generation logic for new structural elements
3. Modify UI to include new parameters
4. Add validation rules for new bridge type

### Enhancing CAD Output
1. Modify layer structure in CAD utilities
2. Update dimension styles and text formatting
3. Add new drawing views or details
4. Integrate additional hatching patterns

### Improving User Interface
1. Enhance Streamlit components with custom CSS
2. Add interactive parameter validation
3. Implement better progress indicators
4. Create help documentation and tooltips

### Debugging CAD Generation
- Use `st.write()` or `st.json()` to debug parameter values
- Enable DXF validation in ezdxf for geometry checking
- Use CAD software to verify output quality
- Check layer organization and entity properties

---

*This documentation enables efficient development and maintenance of the BridgeGAD-03 bridge design system.*
