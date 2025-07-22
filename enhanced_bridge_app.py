
import streamlit as st
import pandas as pd
import ezdxf
import math
import numpy as np
from io import BytesIO
from math import atan2, degrees, sqrt, cos, sin, tan, radians, pi

# Configure the page
st.set_page_config(
    page_title="BridgeGAD Pro - Enhanced Bridge Design Generator",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.section-header {
    font-size: 1.5rem;
    color: #ff7f0e;
    border-bottom: 2px solid #ff7f0e;
    padding-bottom: 0.5rem;
    margin: 1rem 0;
}
.parameter-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
}
.info-box {
    background-color: #e8f4f8;
    border-left: 4px solid #1f77b4;
    padding: 1rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="main-header">🏗️ BridgeGAD Pro</h1>', unsafe_allow_html=True)
st.markdown('<div class="info-box">Enhanced Bridge Design Generator with Professional CAD Output</div>', unsafe_allow_html=True)

# Enhanced Bridge Drawing Class
class EnhancedBridgeDrawer:
    def __init__(self):
        self.doc = ezdxf.new("R2010", setup=True)
        self.msp = self.doc.modelspace()
        self.setup_layers()
        self.setup_styles()
        self.setup_dimension_style()

    def setup_layers(self):
        """Create organized layer structure"""
        layers = [
            ("GRID", 8, "Grid lines and axes"),
            ("STRUCTURE", 1, "Main structural elements"),
            ("DIMENSIONS", 6, "Dimension lines and text"),
            ("ANNOTATIONS", 3, "Text and labels"),
            ("CENTERLINES", 4, "Center lines"),
            ("HATCHING", 9, "Section hatching"),
            ("DETAILS", 2, "Detail elements")
        ]

        for name, color, description in layers:
            layer = self.doc.layers.new(name=name)
            layer.dxf.color = color
            layer.description = description

    def setup_styles(self):
        """Create text styles"""
        # Main text style
        self.doc.styles.new("MAIN_TEXT", dxfattribs={
            'font': 'Arial.ttf',
            'height': 2.5,
            'width': 0.8
        })

        # Title text style
        self.doc.styles.new("TITLE_TEXT", dxfattribs={
            'font': 'Arial.ttf',
            'height': 5.0,
            'width': 1.0
        })

    def setup_dimension_style(self):
        """Create professional dimension style"""
        dimstyle = self.doc.dimstyles.new('PROFESSIONAL')
        dimstyle.dxf.dimasz = 2.0      # Arrow size
        dimstyle.dxf.dimtxt = 2.5      # Text height
        dimstyle.dxf.dimexe = 1.0      # Extension line extension
        dimstyle.dxf.dimexo = 0.6      # Extension line offset
        dimstyle.dxf.dimgap = 0.6      # Gap between dimension line and text
        dimstyle.dxf.dimtxsty = "MAIN_TEXT"

    def draw_title_block(self, project_name, drawing_title, scale, date):
        """Add professional title block"""
        # Title block rectangle
        title_x, title_y = 200, 20
        title_w, title_h = 180, 60

        self.msp.add_lwpolyline([
            (title_x, title_y),
            (title_x + title_w, title_y),
            (title_x + title_w, title_y + title_h),
            (title_x, title_y + title_h)
        ], close=True, dxfattribs={'layer': 'STRUCTURE'})

        # Add title text
        self.msp.add_text(
            drawing_title,
            dxfattribs={
                'insert': (title_x + 5, title_y + title_h - 15),
                'height': 4,
                'style': 'TITLE_TEXT',
                'layer': 'ANNOTATIONS'
            }
        )

        # Add project info
        info_lines = [
            f"Project: {project_name}",
            f"Scale: {scale}",
            f"Date: {date}"
        ]

        for i, line in enumerate(info_lines):
            self.msp.add_text(
                line,
                dxfattribs={
                    'insert': (title_x + 5, title_y + 30 - i * 8),
                    'height': 2.5,
                    'style': 'MAIN_TEXT',
                    'layer': 'ANNOTATIONS'
                }
            )

    def draw_enhanced_grid(self, left, right, datum, top, x_incr, y_incr, scale):
        """Draw professional grid with proper spacing and labels"""
        # Horizontal grid lines
        current_level = datum
        while current_level <= top:
            y_pos = self.vpos(current_level, datum, scale)

            # Main grid line
            self.msp.add_line(
                (left, y_pos),
                (right, y_pos),
                dxfattribs={'layer': 'GRID', 'linetype': 'DASHED'}
            )

            # Level label
            self.msp.add_text(
                f"RL {current_level:.2f}",
                dxfattribs={
                    'insert': (left - 30, y_pos - 2),
                    'height': 2.0,
                    'style': 'MAIN_TEXT',
                    'layer': 'ANNOTATIONS'
                }
            )

            current_level += y_incr

        # Vertical grid lines
        current_ch = left
        while current_ch <= right:
            x_pos = self.hpos(current_ch, left, scale)

            # Main grid line
            self.msp.add_line(
                (x_pos, datum),
                (x_pos, self.vpos(top, datum, scale)),
                dxfattribs={'layer': 'GRID', 'linetype': 'DASHED'}
            )

            # Chainage label
            self.msp.add_text(
                f"Ch {current_ch:.0f}",
                dxfattribs={
                    'insert': (x_pos - 5, datum - 15),
                    'height': 2.0,
                    'style': 'MAIN_TEXT',
                    'layer': 'ANNOTATIONS',
                    'rotation': 90
                }
            )

            current_ch += x_incr

    def draw_enhanced_bridge_elevation(self, params):
        """Draw professional bridge elevation"""
        # Extract parameters
        abtl = params.get('ABTL', 0)
        span1 = params.get('SPAN1', 30)
        nspan = params.get('NSPAN', 3)
        rtl = params.get('RTL', 105)
        sofl = params.get('SOFL', 103)
        scale = params.get('SCALE1', 100) / params.get('SCALE2', 50)

        # Draw deck slab with enhanced appearance
        for i in range(int(nspan)):
            x1 = self.hpos(abtl + i * span1, params.get('LEFT', 0), scale)
            x2 = self.hpos(abtl + (i + 1) * span1, params.get('LEFT', 0), scale)
            y1 = self.vpos(rtl, params.get('DATUM', 100), scale)
            y2 = self.vpos(sofl, params.get('DATUM', 100), scale)

            # Deck slab outline
            deck_points = [
                (x1, y1),
                (x2, y1),
                (x2, y2),
                (x1, y2)
            ]

            # Draw filled deck slab
            self.msp.add_lwpolyline(
                deck_points,
                close=True,
                dxfattribs={'layer': 'STRUCTURE', 'color': 1}
            )

            # Add hatching for concrete
            hatch = self.msp.add_hatch(color=8)
            hatch.paths.add_polyline_path(deck_points, is_closed=True)
            hatch.set_pattern_fill("ANSI31", scale=0.5)

        # Draw piers with enhanced detail
        self.draw_enhanced_piers(params)

        # Draw approach slabs
        self.draw_approach_slabs(params)

    def draw_enhanced_piers(self, params):
        """Draw detailed pier elements"""
        nspan = int(params.get('NSPAN', 3))
        if nspan <= 1:
            return

        abtl = params.get('ABTL', 0)
        span1 = params.get('SPAN1', 30)
        capt = params.get('CAPT', 104)
        capb = params.get('CAPB', 102)
        capw = params.get('CAPW', 1.2)
        piertw = params.get('PIERTW', 0.8)
        battr = params.get('BATTR', 6)
        futrl = params.get('FUTRL', 98)
        futd = params.get('FUTD', 1)
        futw = params.get('FUTW', 2.5)
        scale = params.get('SCALE1', 100) / params.get('SCALE2', 50)

        for i in range(1, nspan):
            pier_ch = abtl + i * span1
            x_center = self.hpos(pier_ch, params.get('LEFT', 0), scale)

            # Pier cap
            cap_x1 = x_center - capw * scale / 2
            cap_x2 = x_center + capw * scale / 2
            cap_y1 = self.vpos(capt, params.get('DATUM', 100), scale)
            cap_y2 = self.vpos(capb, params.get('DATUM', 100), scale)

            self.msp.add_lwpolyline([
                (cap_x1, cap_y1),
                (cap_x2, cap_y1),
                (cap_x2, cap_y2),
                (cap_x1, cap_y2)
            ], close=True, dxfattribs={'layer': 'STRUCTURE'})

            # Pier shaft
            pier_top_half = piertw * scale / 2
            pier_height = capb - futrl - futd
            pier_bottom_half = pier_top_half + pier_height / battr

            pier_y1 = cap_y2
            pier_y2 = self.vpos(futrl + futd, params.get('DATUM', 100), scale)

            # Left pier face
            self.msp.add_line(
                (x_center - pier_top_half, pier_y1),
                (x_center - pier_bottom_half, pier_y2),
                dxfattribs={'layer': 'STRUCTURE'}
            )

            # Right pier face
            self.msp.add_line(
                (x_center + pier_top_half, pier_y1),
                (x_center + pier_bottom_half, pier_y2),
                dxfattribs={'layer': 'STRUCTURE'}
            )

            # Footing
            foot_x1 = x_center - futw * scale / 2
            foot_x2 = x_center + futw * scale / 2
            foot_y1 = pier_y2
            foot_y2 = self.vpos(futrl, params.get('DATUM', 100), scale)

            self.msp.add_lwpolyline([
                (foot_x1, foot_y1),
                (foot_x2, foot_y1),
                (foot_x2, foot_y2),
                (foot_x1, foot_y2)
            ], close=True, dxfattribs={'layer': 'STRUCTURE'})

    def draw_approach_slabs(self, params):
        """Draw approach slabs with proper details"""
        abtl = params.get('ABTL', 0)
        nspan = params.get('NSPAN', 3)
        span1 = params.get('SPAN1', 30)
        rtl = params.get('RTL', 105)
        laslab = params.get('LASLAB', 3)
        apthk = params.get('APTHK', 0.2)
        scale = params.get('SCALE1', 100) / params.get('SCALE2', 50)

        # Left approach slab
        left_start = self.hpos(abtl - laslab, params.get('LEFT', 0), scale)
        left_end = self.hpos(abtl, params.get('LEFT', 0), scale)

        # Right approach slab
        right_start = self.hpos(abtl + nspan * span1, params.get('LEFT', 0), scale)
        right_end = self.hpos(abtl + nspan * span1 + laslab, params.get('LEFT', 0), scale)

        slab_top = self.vpos(rtl, params.get('DATUM', 100), scale)
        slab_bottom = self.vpos(rtl - apthk, params.get('DATUM', 100), scale)

        # Draw approach slabs
        for start_x, end_x in [(left_start, left_end), (right_start, right_end)]:
            self.msp.add_lwpolyline([
                (start_x, slab_top),
                (end_x, slab_top),
                (end_x, slab_bottom),
                (start_x, slab_bottom)
            ], close=True, dxfattribs={'layer': 'STRUCTURE'})

    def hpos(self, chainage, left, scale):
        """Convert chainage to horizontal position"""
        return left + (chainage - left) * scale

    def vpos(self, level, datum, scale):
        """Convert level to vertical position"""
        return datum + (level - datum) * scale

    def add_professional_dimensions(self, params):
        """Add comprehensive dimensioning"""
        # Add span dimensions
        nspan = int(params.get('NSPAN', 3))
        abtl = params.get('ABTL', 0)
        span1 = params.get('SPAN1', 30)
        scale = params.get('SCALE1', 100) / params.get('SCALE2', 50)
        datum = params.get('DATUM', 100)

        dim_y = self.vpos(datum - 10, datum, scale)

        for i in range(nspan):
            x1 = self.hpos(abtl + i * span1, params.get('LEFT', 0), scale)
            x2 = self.hpos(abtl + (i + 1) * span1, params.get('LEFT', 0), scale)

            dim = self.msp.add_linear_dim(
                base=(x1, dim_y),
                p1=(x1, dim_y + 5),
                p2=(x2, dim_y + 5),
                dimstyle="PROFESSIONAL"
            )
            dim.render()

    def save_drawing(self, filename):
        """Save the DXF file"""
        self.doc.saveas(filename)

# Sidebar for parameters
with st.sidebar:
    st.markdown('<div class="section-header">📊 Project Settings</div>', unsafe_allow_html=True)

    project_name = st.text_input("Project Name", "Highway Bridge Project")
    drawing_title = st.text_input("Drawing Title", "Bridge Elevation & Plan")

    st.markdown('<div class="section-header">⚙️ Drawing Options</div>', unsafe_allow_html=True)

    add_dimensions = st.checkbox("Add Dimensions", value=True)
    add_annotations = st.checkbox("Add Annotations", value=True)
    add_title_block = st.checkbox("Add Title Block", value=True)
    drawing_scale = st.selectbox("Drawing Scale", ["1:100", "1:200", "1:500", "1:1000"])

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section-header">📁 Upload Bridge Parameters</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Choose Excel file with bridge parameters",
        type=["xlsx", "xls"],
        help="Upload an Excel file with bridge design parameters"
    )

with col2:
    st.markdown('<div class="section-header">📋 Sample Template</div>', unsafe_allow_html=True)
    if st.button("📥 Download Template"):
        # Create sample template
        sample_data = {
            'Value': [100, 50, 0, 100, 0, 0, 100, 10, 1, 11, 3, 30],
            'Variable': ['SCALE1', 'SCALE2', 'SKEW', 'DATUM', 'TOPRL', 'LEFT', 'RIGHT', 'XINCR', 'YINCR', 'NOCH', 'NSPAN', 'LBRIDGE'],
            'Description': ['Main scale factor', 'Secondary scale factor', 'Skew angle', 'Reference datum', 'Top road level', 'Left chainage', 'Right chainage', 'X increment', 'Y increment', 'Number of chainages', 'Number of spans', 'Bridge length']
        }

        template_df = pd.DataFrame(sample_data)
        st.download_button(
            "📥 Download Excel Template",
            template_df.to_excel(index=False),
            "bridge_parameters_template.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# Process uploaded file
if uploaded_file:
    try:
        # Read parameters
        df = pd.read_excel(uploaded_file, sheet_name="Sheet1")
        params = dict(zip(df['Variable'], df['Value']))

        # Display parameters in organized cards
        st.markdown('<div class="section-header">🔧 Bridge Parameters</div>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f'<div class="parameter-card"><h4>Spans</h4><p>{int(params.get("NSPAN", 0))}</p></div>',
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f'<div class="parameter-card"><h4>Span Length</h4><p>{params.get("SPAN1", 0)} m</p></div>',
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f'<div class="parameter-card"><h4>Bridge Length</h4><p>{params.get("LBRIDGE", 0)} m</p></div>',
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                f'<div class="parameter-card"><h4>Skew Angle</h4><p>{params.get("SKEW", 0)}°</p></div>',
                unsafe_allow_html=True
            )

        # Editable parameters table
        st.markdown('<div class="section-header">📝 Edit Parameters</div>', unsafe_allow_html=True)
        edited_df = st.data_editor(
            df,
            column_config={
                "Value": st.column_config.NumberColumn("Value", format="%.3f"),
                "Variable": st.column_config.TextColumn("Variable"),
                "Description": st.column_config.TextColumn("Description")
            },
            use_container_width=True,
            height=300
        )

        # Generate drawing button
        if st.button("🚀 Generate Professional DXF Drawing", type="primary", use_container_width=True):
            with st.spinner("Creating professional CAD drawing..."):
                try:
                    # Update parameters from edited data
                    params = dict(zip(edited_df['Variable'], edited_df['Value']))

                    # Create enhanced bridge drawer
                    drawer = EnhancedBridgeDrawer()

                    # Add title block if requested
                    if add_title_block:
                        drawer.draw_title_block(
                            project_name,
                            drawing_title,
                            drawing_scale,
                            pd.Timestamp.now().strftime("%Y-%m-%d")
                        )

                    # Draw grid
                    drawer.draw_enhanced_grid(
                        params.get('LEFT', 0),
                        params.get('RIGHT', 100),
                        params.get('DATUM', 100),
                        params.get('RTL', 105),
                        params.get('XINCR', 10),
                        params.get('YINCR', 1),
                        params.get('SCALE1', 100) / params.get('SCALE2', 50)
                    )

                    # Draw bridge elevation
                    drawer.draw_enhanced_bridge_elevation(params)

                    # Add dimensions if requested
                    if add_dimensions:
                        drawer.add_professional_dimensions(params)

                    # Save to temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as tmp_file:
                        drawer.save_drawing(tmp_file.name)

                        # Read file for download
                        with open(tmp_file.name, 'rb') as f:
                            dxf_data = f.read()

                        # Clean up
                        os.unlink(tmp_file.name)

                    # Success message and download
                    st.success("✅ Professional DXF drawing generated successfully!")

                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        st.download_button(
                            "📥 Download Enhanced DXF",
                            dxf_data,
                            f"{project_name.replace(' ', '_')}_bridge_design.dxf",
                            "application/dxf",
                            use_container_width=True
                        )

                    # Display drawing statistics
                    st.info(f"""
                    **Drawing Statistics:**
                    - Total Spans: {int(params.get('NSPAN', 0))}
                    - Bridge Length: {params.get('LBRIDGE', 0)} m
                    - Scale: {drawing_scale}
                    - Layers: 7 professional layers
                    - Enhanced Features: ✅ Professional dimensions, ✅ Title block, ✅ Hatching
                    """)

                except Exception as e:
                    st.error(f"❌ Error generating drawing: {str(e)}")
                    st.exception(e)

    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")

# Instructions and help
with st.expander("📖 How to Use BridgeGAD Pro"):
    st.markdown("""
    ## Getting Started

    1. **Download Template**: Click the "Download Template" button to get a sample Excel file
    2. **Fill Parameters**: Open the template and fill in your bridge design parameters
    3. **Upload File**: Use the file uploader to load your completed parameters
    4. **Review & Edit**: Check parameters in the interactive table and make adjustments if needed
    5. **Generate Drawing**: Click the generate button to create your professional DXF drawing

    ## Enhanced Features

    - 🎨 **Professional Layers**: Organized layer structure for different drawing elements
    - 📏 **Smart Dimensioning**: Automatic dimension generation with proper styling
    - 🏗️ **Detailed Elements**: Enhanced pier, deck, and approach slab representations
    - 📋 **Title Blocks**: Professional title blocks with project information
    - 🎯 **Grid System**: Comprehensive grid with proper labeling
    - 🔄 **Hatching**: Concrete hatching for better visualization

    ## File Requirements

    Your Excel file should contain:
    - **Sheet1**: Parameters with columns: Value, Variable, Description
    - **Sheet2** (optional): Cross-section data with Chainage and RL values

    ## Professional Output

    The generated DXF files are compatible with:
    - AutoCAD
    - BricsCAD  
    - QCAD
    - LibreCAD
    - And other CAD software supporting DXF R2010 format
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🏗️ <strong>BridgeGAD Pro</strong> - Professional Bridge Design Generator</p>
    <p>Enhanced version with professional CAD output quality</p>
</div>
""", unsafe_allow_html=True)
