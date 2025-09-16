
import streamlit as st
import pandas as pd
import ezdxf
import math
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from math import atan2, degrees, sqrt, cos, sin, tan, radians, pi
from matplotlib.patches import Rectangle, Polygon, FancyArrow

# Import custom modules
from abutment_design import AbutmentDesign
from approach_slab_design import ApproachSlabDesign

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

class EnhancedBridgeGAD:
    def __init__(self):
        self.bridge_params = {}
        self.abutment_params = {}
        self.approach_slab_params = {}
    
    def generate_complete_drawings(self):
        """Generate complete bridge drawings with all components"""
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 16))
        
        # Plan view
        self.draw_plan_view(ax1)
        
        # Sectional elevation
        self.draw_sectional_elevation(ax2)
        
        # Abutment details
        self.draw_abutment_details(ax3)
        
        # Approach slab details
        self.draw_approach_slab_details(ax4)
        
        plt.tight_layout()
        return fig
    
    def draw_plan_view(self, ax):
        """Draw plan view of the bridge"""
        # Bridge deck
        deck = Rectangle((2, 4), 8, 0.5, angle=0, facecolor='lightgray', edgecolor='black', linewidth=2)
        ax.add_patch(deck)
        
        # Add dimensions and labels
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 8)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title('Plan View')
        ax.set_xlabel('Length (m)')
        ax.set_ylabel('Width (m)')
    
    def draw_sectional_elevation(self, ax):
        """Draw sectional elevation view"""
        # Bridge deck
        deck = Rectangle((2, 4), 8, 0.5, facecolor='lightgray', edgecolor='black', linewidth=2)
        ax.add_patch(deck)
        
        # Abutments
        abutment_height = self.abutment_params.get('height', 3.5)
        left_abutment = Rectangle((1.5, 1), 0.5, abutment_height, facecolor='darkgray', edgecolor='black', linewidth=2)
        right_abutment = Rectangle((10, 1), 0.5, abutment_height, facecolor='darkgray', edgecolor='black', linewidth=2)
        ax.add_patch(left_abutment)
        ax.add_patch(right_abutment)
        
        # Approach slabs
        approach_length = self.approach_slab_params.get('length', 3.0)
        left_approach = Rectangle((1.5 - approach_length, 4), approach_length, 0.3, facecolor='lightblue', edgecolor='black', linewidth=1)
        right_approach = Rectangle((10.5, 4), approach_length, 0.3, facecolor='lightblue', edgecolor='black', linewidth=1)
        ax.add_patch(left_approach)
        ax.add_patch(right_approach)
        
        # Piers/supports
        pier_left = Rectangle((4, 1), 0.5, 3, facecolor='gray', edgecolor='black', linewidth=1)
        pier_right = Rectangle((7.5, 1), 0.5, 3, facecolor='gray', edgecolor='black', linewidth=1)
        ax.add_patch(pier_left)
        ax.add_patch(pier_right)
        
        # Ground level
        ground = Rectangle((0, 0), 12, 1, facecolor='brown', alpha=0.3)
        ax.add_patch(ground)
        
        # Dimensions and labels
        ax.annotate('', xy=(2, 5.5), xytext=(10, 5.5), arrowprops=dict(arrowstyle='<->', color='red', lw=2))
        ax.text(6, 5.7, '8.0m', fontsize=10, ha='center', color='red')
        
        ax.set_xlim(-0.5, 12.5)
        ax.set_ylim(-0.5, 6)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title('Sectional Elevation')
        ax.set_xlabel('Length (m)')
        ax.set_ylabel('Height (m)')
    
    def draw_abutment_details(self, ax):
        """Draw detailed abutment design"""
        # Abutment body
        abutment_body = Rectangle((1, 1), 2, 3, facecolor='lightgray', edgecolor='black', linewidth=2)
        ax.add_patch(abutment_body)
        
        # Foundation
        foundation = Rectangle((0.5, 0.5), 3, 0.5, facecolor='darkgray', edgecolor='black', linewidth=2)
        ax.add_patch(foundation)
        
        # Wing walls
        wing_left = Polygon([(0.5, 1), (1, 1), (1, 3), (0.5, 3.5)], facecolor='gray', edgecolor='black', linewidth=1)
        wing_right = Polygon([(3, 1), (3.5, 1), (3.5, 3.5), (3, 3)], facecolor='gray', edgecolor='black', linewidth=1)
        ax.add_patch(wing_left)
        ax.add_patch(wing_right)
        
        # Reinforcement details (simplified)
        for i in range(1, 4):
            ax.plot([1.2, 2.8], [i + 0.5, i + 0.5], 'r-', linewidth=2, alpha=0.7)
        
        for i in range(1, 3):
            ax.plot([1.2 + i * 0.4, 1.2 + i * 0.4], [1.2, 3.8], 'r-', linewidth=2, alpha=0.7)
        
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 4.5)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title('Abutment Details')
        ax.set_xlabel('Width (m)')
        ax.set_ylabel('Height (m)')
    
    def draw_approach_slab_details(self, ax):
        """Draw approach slab reinforcement details"""
        # Approach slab
        slab = Rectangle((0, 2), 4, 0.3, facecolor='lightblue', edgecolor='black', linewidth=2)
        ax.add_patch(slab)
        
        # Reinforcement - longitudinal bars
        for i in range(5):
            y_pos = 2.05 + i * 0.05
            ax.plot([0.2, 3.8], [y_pos, y_pos], 'r-', linewidth=2, alpha=0.8)
        
        # Reinforcement - transverse bars
        for i in range(8):
            x_pos = 0.2 + i * 0.5
            ax.plot([x_pos, x_pos], [2.05, 2.25], 'r-', linewidth=2, alpha=0.8)
        
        # Support details
        support = Rectangle((3.8, 1.5), 0.4, 0.8, facecolor='gray', edgecolor='black', linewidth=1)
        ax.add_patch(support)
        
        # Dimensions
        ax.annotate('', xy=(0, 1.5), xytext=(4, 1.5), arrowprops=dict(arrowstyle='<->', color='red', lw=2))
        ax.text(2, 1.3, '4.0m', fontsize=10, ha='center', color='red')
        
        ax.annotate('', xy=(4.5, 2), xytext=(4.5, 2.3), arrowprops=dict(arrowstyle='<->', color='blue', lw=1))
        ax.text(4.7, 2.15, '300mm', fontsize=8, ha='left', color='blue')
        
        ax.set_xlim(-0.5, 5.5)
        ax.set_ylim(1, 3)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title('Approach Slab Details')
        ax.set_xlabel('Length (m)')
        ax.set_ylabel('Height (m)')

# Sidebar for parameters
with st.sidebar:
    st.markdown('<div class="section-header">📊 Project Settings</div>', unsafe_allow_html=True)
    
    # Bridge parameters
    st.subheader("Bridge Parameters")
    bridge_width = st.number_input("Bridge Width (m)", min_value=5.0, max_value=20.0, value=8.0, step=0.5)
    bridge_length = st.number_input("Bridge Length (m)", min_value=10.0, max_value=100.0, value=30.0, step=1.0)
    
    # Abutment parameters
    st.subheader("Abutment Parameters")
    abutment_height = st.number_input("Abutment Height (m)", min_value=2.0, max_value=10.0, value=3.5, step=0.5)
    abutment_width = st.number_input("Abutment Width (m)", min_value=0.5, max_value=3.0, value=0.8, step=0.1)
    
    # Approach slab parameters
    st.subheader("Approach Slab Parameters")
    approach_slab_length = st.number_input("Approach Slab Length (m)", min_value=2.0, max_value=10.0, value=3.0, step=0.5)
    approach_slab_thickness = st.number_input("Approach Slab Thickness (mm)", min_value=150, max_value=500, value=300, step=25) / 1000  # Convert to meters

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
# Initialize the enhanced bridge design
bridge_design = EnhancedBridgeGAD()

# Set bridge parameters
bridge_params = {
    'width': bridge_width,
    'length': bridge_length,
    'deck_thickness': 0.5  # meters
}

# Set abutment parameters
abutment_params = {
    'height': abutment_height,
    'width': abutment_width,
    'thickness': 0.5  # meters
}

# Set approach slab parameters
approach_slab_params = {
    'length': approach_slab_length,
    'thickness': approach_slab_thickness,
    'reinforcement': {}
}

# Update design object with parameters
bridge_design.bridge_params = bridge_params
bridge_design.abutment_params = abutment_params
bridge_design.approach_slab_params = approach_slab_params

# Create tabs for different views
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📐 Plan View", 
    "🏗️ Sectional Elevation", 
    "🧱 Abutment Details", 
    "🛣️ Approach Slab",
    "📊 Design Calculations"
])

with tab1:
    st.subheader("Bridge Plan View")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    bridge_design.draw_plan_view(ax1)
    st.pyplot(fig1)

with tab2:
    st.subheader("Sectional Elevation")
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    bridge_design.draw_sectional_elevation(ax2)
    st.pyplot(fig2)

with tab3:
    st.subheader("Abutment Details")
    fig3, ax3 = plt.subplots(figsize=(8, 8))
    bridge_design.draw_abutment_details(ax3)
    st.pyplot(fig3)

with tab4:
    st.subheader("Approach Slab Design")
    
    # Create approach slab design instance
    approach_slab = ApproachSlabDesign(
        length=approach_slab_length,
        width=bridge_width,
        thickness=approach_slab_thickness
    )
    
    # Calculate and display design parameters
    design_report = approach_slab.generate_design_report()
    
    # Display design parameters in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Design Parameters")
        for param, value in design_report['design_parameters'].items():
            st.text(f"{param.replace('_', ' ').title()}: {value}")
        
        st.markdown("### Loads")
        for load, value in design_report['loads'].items():
            st.text(f"{load.replace('_', ' ').title()}: {value}")
    
    with col2:
        st.markdown("### Design Moments")
        for moment, value in design_report['design_moments'].items():
            st.text(f"{moment.replace('_', ' ').title()}: {value}")
        
        st.markdown("### Reinforcement")
        for item, value in design_report['reinforcement'].items():
            st.text(f"{item.replace('_', ' ').title()}: {value}")
    
    # Show approach slab details
    st.markdown("### Approach Slab Details")
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    bridge_design.draw_approach_slab_details(ax4)
    st.pyplot(fig4)

with tab5:
    st.subheader("Design Calculations")
    
    # Create design instances
    abutment_design = AbutmentDesign(
        bridge_width=bridge_width,
        bridge_height=bridge_params['deck_thickness'],
        abutment_height=abutment_height,
        approach_slab_length=approach_slab_length
    )
    
    approach_slab_design = ApproachSlabDesign(
        length=approach_slab_length,
        width=bridge_width,
        thickness=approach_slab_thickness,
        reinforcement_details={}
    )
    
    # Calculate loads and reinforcement
    approach_loads = approach_slab_design.calculate_approach_slab_loads()
    approach_reinforcement = approach_slab_design.design_reinforcement()
    
    # Display results in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Approach Slab Loads")
        st.metric("Dead Load", f"{approach_loads['dead_load']:.2f} kN/m²")
        st.metric("Live Load", f"{approach_loads['live_load']:.2f} kN/m²")
        st.metric("Total Load", f"{approach_loads['total_load']:.2f} kN/m²")
    
    with col2:
        st.markdown("### Reinforcement Details")
        st.metric("Required Steel Area", f"{approach_reinforcement['ast_required']:.2f} mm²/m")
        st.metric("Bar Diameter", f"{approach_reinforcement['bar_diameter']} mm")
        st.metric("Spacing", f"{approach_reinforcement['spacing']} mm c/c")
    
    # Show calculation summary
    st.markdown("### Design Summary")
    st.markdown("""
    - **Abutment Height**: {:.2f} m
    - **Abutment Width**: {:.2f} m
    - **Approach Slab Length**: {:.2f} m
    - **Approach Slab Thickness**: {:.0f} mm
    
    The design follows standard bridge engineering practices and includes appropriate
    factors of safety for both dead and live loads.
    """.format(
        abutment_height,
        abutment_width,
        approach_slab_length,
        approach_slab_thickness * 1000  # Convert to mm
    ))

# File upload section
st.sidebar.markdown('---')
st.sidebar.subheader("Import/Export")
uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    try:
        # Read parameters from Excel
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
