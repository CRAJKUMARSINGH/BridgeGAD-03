
import ezdxf
import math
from math import cos, sin, tan, radians, degrees, pi
import numpy as np

class BridgeCADUtils:
    """Enhanced CAD utilities for professional bridge drawing"""

    @staticmethod
    def create_professional_layers(doc):
        """Create a comprehensive layer structure for bridge drawings"""
        layer_definitions = [
            # Layer Name, Color, Linetype, Description
            ("0-DEFPOINTS", 7, "CONTINUOUS", "Default points layer"),
            ("GRID-MAJOR", 8, "CONTINUOUS", "Major grid lines"),
            ("GRID-MINOR", 253, "DASHED2", "Minor grid lines"),
            ("AXIS-CENTER", 4, "CENTER", "Center lines and axes"),
            ("STRUCTURE-CONCRETE", 1, "CONTINUOUS", "Concrete structural elements"),
            ("STRUCTURE-STEEL", 2, "CONTINUOUS", "Steel structural elements"),
            ("REINFORCEMENT", 3, "CONTINUOUS", "Reinforcement details"),
            ("DIMENSIONS", 6, "CONTINUOUS", "Dimension lines and text"),
            ("TEXT-LARGE", 3, "CONTINUOUS", "Large text and titles"),
            ("TEXT-MEDIUM", 2, "CONTINUOUS", "Medium text and labels"),
            ("TEXT-SMALL", 8, "CONTINUOUS", "Small text and notes"),
            ("HATCHING-CONCRETE", 9, "CONTINUOUS", "Concrete hatching"),
            ("HATCHING-STEEL", 1, "CONTINUOUS", "Steel hatching"),
            ("HATCHING-EARTH", 30, "CONTINUOUS", "Earth/soil hatching"),
            ("DETAILS", 2, "CONTINUOUS", "Detail elements"),
            ("SYMBOL", 5, "CONTINUOUS", "Symbols and markers"),
            ("HIDDEN", 8, "HIDDEN", "Hidden lines"),
            ("PHANTOM", 6, "PHANTOM", "Phantom lines"),
            ("BORDER", 7, "CONTINUOUS", "Drawing border"),
            ("TITLE-BLOCK", 7, "CONTINUOUS", "Title block elements"),
        ]

        created_layers = {}
        for name, color, linetype, description in layer_definitions:
            try:
                layer = doc.layers.new(name=name)
                layer.dxf.color = color
                layer.dxf.linetype = linetype
                layer.description = description
                created_layers[name] = layer
            except Exception as e:
                print(f"Warning: Could not create layer {name}: {e}")

        return created_layers

    @staticmethod
    def create_text_styles(doc):
        """Create professional text styles"""
        text_styles = [
            # Style name, font, height, width factor
            ("TITLE", "Arial.ttf", 0.0, 1.0),
            ("SUBTITLE", "Arial.ttf", 0.0, 0.9),
            ("STANDARD", "Arial.ttf", 0.0, 0.8),
            ("SMALL", "Arial.ttf", 0.0, 0.75),
            ("DIMENSION", "Arial.ttf", 0.0, 0.8),
            ("ANNOTATION", "Arial.ttf", 0.0, 0.8),
        ]

        created_styles = {}
        for style_name, font, height, width in text_styles:
            try:
                style = doc.styles.new(style_name, dxfattribs={
                    'font': font,
                    'height': height,
                    'width': width
                })
                created_styles[style_name] = style
            except Exception as e:
                print(f"Warning: Could not create text style {style_name}: {e}")

        return created_styles

    @staticmethod
    def create_dimension_styles(doc):
        """Create professional dimension styles"""
        # Standard dimension style
        try:
            dimstyle = doc.dimstyles.new('PROFESSIONAL')
            dimstyle.dxf.dimasz = 2.5      # Arrow size
            dimstyle.dxf.dimtxt = 2.5      # Text height
            dimstyle.dxf.dimexe = 1.25     # Extension line extension
            dimstyle.dxf.dimexo = 0.625    # Extension line offset
            dimstyle.dxf.dimgap = 0.625    # Gap between dimension line and text
            dimstyle.dxf.dimtxsty = "STANDARD"
            dimstyle.dxf.dimlwd = 25       # Dimension line lineweight
            dimstyle.dxf.dimlwe = 25       # Extension line lineweight

            # Architectural dimension style
            arch_dimstyle = doc.dimstyles.new('ARCHITECTURAL')
            arch_dimstyle.dxf.dimasz = 3.0
            arch_dimstyle.dxf.dimtxt = 3.0
            arch_dimstyle.dxf.dimexe = 1.5
            arch_dimstyle.dxf.dimexo = 0.75
            arch_dimstyle.dxf.dimgap = 0.75
            arch_dimstyle.dxf.dimtxsty = "STANDARD"

            return {'PROFESSIONAL': dimstyle, 'ARCHITECTURAL': arch_dimstyle}
        except Exception as e:
            print(f"Warning: Could not create dimension styles: {e}")
            return {}

    @staticmethod
    def add_concrete_hatch(msp, points, scale=1.0, angle=45):
        """Add concrete hatching pattern"""
        try:
            hatch = msp.add_hatch(color=9, dxfattribs={'layer': 'HATCHING-CONCRETE'})
            hatch.paths.add_polyline_path(points, is_closed=True)
            hatch.set_pattern_fill("ANSI31", scale=scale, angle=angle)
            return hatch
        except Exception as e:
            print(f"Warning: Could not add concrete hatch: {e}")
            return None

    @staticmethod
    def add_steel_hatch(msp, points, scale=1.0):
        """Add steel hatching pattern"""
        try:
            hatch = msp.add_hatch(color=1, dxfattribs={'layer': 'HATCHING-STEEL'})
            hatch.paths.add_polyline_path(points, is_closed=True)
            hatch.set_pattern_fill("STEEL", scale=scale)
            return hatch
        except Exception as e:
            print(f"Warning: Could not add steel hatch: {e}")
            return None

    @staticmethod
    def draw_reinforcement_symbol(msp, center, diameter=1.0, layer="REINFORCEMENT"):
        """Draw reinforcement bar symbol"""
        try:
            # Draw circle for rebar
            circle = msp.add_circle(center, diameter/2, dxfattribs={'layer': layer})

            # Add cross inside
            offset = diameter/4
            msp.add_line(
                (center[0] - offset, center[1] - offset),
                (center[0] + offset, center[1] + offset),
                dxfattribs={'layer': layer}
            )
            msp.add_line(
                (center[0] - offset, center[1] + offset),
                (center[0] + offset, center[1] - offset),
                dxfattribs={'layer': layer}
            )
            return circle
        except Exception as e:
            print(f"Warning: Could not draw reinforcement symbol: {e}")
            return None

class EnhancedBridgeGeometry:
    """Enhanced bridge geometry calculations"""

    def __init__(self, params):
        self.params = params
        self.scale_x = params.get('SCALE1', 100) / params.get('SCALE2', 50)
        self.scale_y = self.scale_x
        self.skew_rad = radians(params.get('SKEW', 0))

    def transform_point(self, x, y, reference_x=0, reference_y=0):
        """Transform point considering scale and skew"""
        # Apply scaling
        scaled_x = reference_x + (x - reference_x) * self.scale_x
        scaled_y = reference_y + (y - reference_y) * self.scale_y

        # Apply skew transformation if needed
        if self.skew_rad != 0:
            cos_skew = cos(self.skew_rad)
            sin_skew = sin(self.skew_rad)

            # Rotate point around reference
            rel_x = scaled_x - reference_x
            rel_y = scaled_y - reference_y

            new_x = rel_x * cos_skew - rel_y * sin_skew + reference_x
            new_y = rel_x * sin_skew + rel_y * cos_skew + reference_y

            return (new_x, new_y)

        return (scaled_x, scaled_y)

    def get_span_points(self, span_index):
        """Get key points for a specific span"""
        abtl = self.params.get('ABTL', 0)
        span1 = self.params.get('SPAN1', 30)

        start_ch = abtl + span_index * span1
        end_ch = abtl + (span_index + 1) * span1

        return {
            'start_chainage': start_ch,
            'end_chainage': end_ch,
            'center_chainage': (start_ch + end_ch) / 2,
            'length': span1
        }

    def get_pier_geometry(self, pier_index):
        """Get detailed pier geometry"""
        spans_info = self.get_span_points(pier_index)
        pier_ch = spans_info['end_chainage']

        # Pier dimensions
        piertw = self.params.get('PIERTW', 0.8)
        capw = self.params.get('CAPW', 1.2)
        capt = self.params.get('CAPT', 104)
        capb = self.params.get('CAPB', 102)
        battr = self.params.get('BATTR', 6)
        futrl = self.params.get('FUTRL', 98)
        futd = self.params.get('FUTD', 1)
        futw = self.params.get('FUTW', 2.5)
        futl = self.params.get('FUTL', 3)

        # Calculate pier geometry
        pier_height = capb - futrl - futd
        pier_batter_offset = pier_height / battr if battr > 0 else 0

        return {
            'chainage': pier_ch,
            'cap_top': capt,
            'cap_bottom': capb,
            'cap_width': capw,
            'pier_top_width': piertw,
            'pier_bottom_width': piertw + 2 * pier_batter_offset,
            'footing_top': futrl + futd,
            'footing_bottom': futrl,
            'footing_width': futw,
            'footing_length': futl,
            'batter_offset': pier_batter_offset
        }

class ProfessionalTitleBlock:
    """Professional title block generator"""

    def __init__(self, doc, msp):
        self.doc = doc
        self.msp = msp

    def create_standard_title_block(self, x, y, width=200, height=80, project_info=None):
        """Create standard engineering title block"""
        if project_info is None:
            project_info = {}

        # Main title block rectangle
        self.msp.add_lwpolyline([
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height)
        ], close=True, dxfattribs={'layer': 'TITLE-BLOCK'})

        # Internal divisions
        sections = [
            (0, height*0.6, width, height),      # Title section
            (0, height*0.3, width*0.6, height*0.6), # Project info
            (width*0.6, height*0.3, width, height*0.6), # Drawing info
            (0, 0, width*0.3, height*0.3),      # Date/revision
            (width*0.3, 0, width*0.6, height*0.3), # Scale
            (width*0.6, 0, width, height*0.3),  # Drawing number
        ]

        for sx, sy, ex, ey in sections:
            self.msp.add_line((x + sx, y + sy), (x + sx, y + ey), dxfattribs={'layer': 'TITLE-BLOCK'})
            self.msp.add_line((x + sx, y + sy), (x + ex, y + sy), dxfattribs={'layer': 'TITLE-BLOCK'})
            self.msp.add_line((x + ex, y + sy), (x + ex, y + ey), dxfattribs={'layer': 'TITLE-BLOCK'})
            self.msp.add_line((x + sx, y + ey), (x + ex, y + ey), dxfattribs={'layer': 'TITLE-BLOCK'})

        # Add text content
        title = project_info.get('title', 'BRIDGE DESIGN DRAWING')
        self.msp.add_text(title, dxfattribs={
            'insert': (x + 5, y + height*0.75),
            'height': 4.0,
            'style': 'TITLE',
            'layer': 'TEXT-LARGE'
        })

        # Project information
        project_name = project_info.get('project', 'HIGHWAY BRIDGE PROJECT')
        self.msp.add_text(f"PROJECT: {project_name}", dxfattribs={
            'insert': (x + 5, y + height*0.5),
            'height': 2.5,
            'style': 'STANDARD',
            'layer': 'TEXT-MEDIUM'
        })

        # Drawing information
        drawing_type = project_info.get('type', 'ELEVATION & PLAN')
        self.msp.add_text(drawing_type, dxfattribs={
            'insert': (x + width*0.65, y + height*0.5),
            'height': 2.0,
            'style': 'STANDARD',
            'layer': 'TEXT-MEDIUM'
        })

        # Scale, date, drawing number
        scale = project_info.get('scale', '1:100')
        date = project_info.get('date', '2024-01-01')
        dwg_no = project_info.get('drawing_no', 'BRG-001')

        self.msp.add_text(f"SCALE: {scale}", dxfattribs={
            'insert': (x + width*0.35, y + height*0.15),
            'height': 2.0,
            'style': 'STANDARD',
            'layer': 'TEXT-SMALL'
        })

        self.msp.add_text(f"DATE: {date}", dxfattribs={
            'insert': (x + 5, y + height*0.15),
            'height': 2.0,
            'style': 'STANDARD',
            'layer': 'TEXT-SMALL'
        })

        self.msp.add_text(f"DWG NO: {dwg_no}", dxfattribs={
            'insert': (x + width*0.65, y + height*0.15),
            'height': 2.0,
            'style': 'STANDARD',
            'layer': 'TEXT-SMALL'
        })

        return (x, y, width, height)
