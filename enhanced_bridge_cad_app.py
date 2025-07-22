#!/usr/bin/env python3
"""
Bridge General Arrangement Drawing Generator

A comprehensive Python application for automatically generating general arrangement 
drawings of various bridge types including beam bridges, truss bridges, arch bridges,
suspension bridges, and cable-stayed bridges.

Features:
- Multiple bridge type support
- Parametric design with customizable dimensions
- Professional engineering drawings with proper annotations
- Multiple output formats (SVG, PNG, PDF)
- Standard engineering symbols and conventions
- Automatic dimensioning and labeling
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Arc, Circle, Polygon, Rectangle, FancyBboxPatch
import numpy as np
import svgwrite
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, A4
from reportlab.lib.units import mm
from reportlab.lib.colors import black, blue, red
import math
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Any
from enum import Enum
import argparse
import os
import ezdxf


class BridgeType(Enum):
    """Enumeration of supported bridge types"""
    BEAM = "beam"
    TRUSS = "truss" 
    ARCH = "arch"
    SUSPENSION = "suspension"
    CABLE_STAYED = "cable_stayed"
    T_BEAM = "t_beam"
    SLAB = "slab"


class OutputFormat(Enum):
    """Supported output formats"""
    SVG = "svg"
    PNG = "png"
    PDF = "pdf"
    DXF = "dxf"
    ALL = "all"


@dataclass
class BridgeParameters:
    """Parameters defining bridge geometry and specifications"""
    span_length: float  # Main span length in meters
    deck_width: float   # Deck width in meters
    height: float       # Overall height in meters
    supports: int       # Number of intermediate supports
    load_capacity: float  # Design load in kN/m
    material: str       # Primary material (steel, concrete, timber)
    
    # Optional parameters with defaults
    approach_length: float = 50.0
    foundation_depth: float = 5.0
    girder_depth: float = 2.0
    rail_height: float = 1.2
    
    def __post_init__(self):
        """Validate parameters after initialization"""
        if self.span_length <= 0:
            raise ValueError("Span length must be positive")
        if self.deck_width <= 0:
            raise ValueError("Deck width must be positive")
        if self.height <= 0:
            raise ValueError("Height must be positive")


class BridgeDrawingGenerator:
    """Main class for generating bridge drawings"""
    
    def __init__(self, bridge_type: BridgeType, parameters: BridgeParameters):
        self.bridge_type = bridge_type
        self.params = parameters
        self.figure = None
        self.ax_elevation = None
        self.ax_plan = None
        self.scale = 1.0
        self.include_plan_view = True
        
        # Drawing settings
        self.line_width = 2.0
        self.annotation_fontsize = 10
        self.title_fontsize = 14
        self.dimension_fontsize = 8
        
        # Colors for different elements
        self.colors = {
            'structure': 'black',
            'deck': 'gray',
            'supports': 'darkblue',
            'foundations': 'brown',
            'dimensions': 'red',
            'annotations': 'blue',
            'plan_deck': 'lightgray',
            'plan_structure': 'darkgray'
        }
    
    def setup_drawing(self, width: float = 20, height: float = 16):
        """Initialize the drawing canvas with elevation and plan views"""
        # Create subplots for elevation and plan views
        self.figure, (self.ax_elevation, self.ax_plan) = plt.subplots(2, 1, figsize=(width, height))
        
        if self.ax_elevation is None or self.ax_plan is None:
            raise RuntimeError("Failed to create matplotlib axes")
        
        # Setup elevation view (side view)
        self.ax_elevation.set_aspect('equal')
        self.ax_elevation.grid(True, alpha=0.3)
        
        margin = max(self.params.span_length * 0.1, 20)
        self.ax_elevation.set_xlim(-margin, self.params.span_length + margin)
        self.ax_elevation.set_ylim(-self.params.foundation_depth - 10, 
                                 self.params.height + margin)
        
        self.ax_elevation.set_xlabel('Distance (m)', fontsize=self.annotation_fontsize)
        self.ax_elevation.set_ylabel('Elevation (m)', fontsize=self.annotation_fontsize)
        self.ax_elevation.set_title('ELEVATION VIEW', fontsize=self.title_fontsize, fontweight='bold')
        
        # Setup plan view (top view)
        self.ax_plan.set_aspect('equal')
        self.ax_plan.grid(True, alpha=0.3)
        
        plan_margin = max(self.params.deck_width * 0.2, 5)
        self.ax_plan.set_xlim(-margin, self.params.span_length + margin)
        self.ax_plan.set_ylim(-plan_margin, self.params.deck_width + plan_margin)
        
        self.ax_plan.set_xlabel('Distance (m)', fontsize=self.annotation_fontsize)
        self.ax_plan.set_ylabel('Width (m)', fontsize=self.annotation_fontsize)
        self.ax_plan.set_title('PLAN VIEW', fontsize=self.title_fontsize, fontweight='bold')
        
        # Overall title
        bridge_name = f"{self.bridge_type.value.title()} Bridge"
        overall_title = f"General Arrangement Drawing - {bridge_name}\n"
        overall_title += f"Span: {self.params.span_length}m, Width: {self.params.deck_width}m"
        self.figure.suptitle(overall_title, fontsize=self.title_fontsize + 2, fontweight='bold')
    
    def draw_beam_bridge(self):
        """Generate elevation and plan views for beam bridge"""
        self.draw_beam_bridge_elevation()
        self.draw_beam_bridge_plan()
    
    def draw_beam_bridge_elevation(self):
        """Generate elevation view for beam bridge"""
        # Main deck
        deck_y = self.params.height - self.params.girder_depth
        deck = Rectangle((0, deck_y), self.params.span_length, 
                        self.params.girder_depth, 
                        facecolor=self.colors['deck'], alpha=0.7,
                        edgecolor=self.colors['structure'], linewidth=self.line_width)
        self.ax_elevation.add_patch(deck)
        
        # Girders (simplified as rectangles under deck)
        girder_height = self.params.girder_depth * 0.8
        girder_y = deck_y - girder_height
        
        # Main girders
        for i in range(2):  # Two main girders
            girder = Rectangle((0, girder_y), self.params.span_length, 
                             girder_height * 0.3,
                             facecolor=self.colors['structure'], alpha=0.8)
            self.ax_elevation.add_patch(girder)
        
        # Supports/piers
        if self.params.supports > 0:
            support_spacing = self.params.span_length / (self.params.supports + 1)
            support_width = 2.0
            
            for i in range(self.params.supports):
                x_pos = support_spacing * (i + 1) - support_width / 2
                
                # Pier
                pier = Rectangle((x_pos, -self.params.foundation_depth), 
                               support_width, self.params.height - self.params.girder_depth + self.params.foundation_depth,
                               facecolor=self.colors['supports'], alpha=0.8,
                               edgecolor=self.colors['structure'], linewidth=self.line_width)
                self.ax_elevation.add_patch(pier)
                
                # Foundation
                foundation_width = support_width * 2
                foundation = Rectangle((x_pos - support_width/2, -self.params.foundation_depth), 
                                     foundation_width, self.params.foundation_depth * 0.6,
                                     facecolor=self.colors['foundations'], alpha=0.8)
                self.ax_elevation.add_patch(foundation)
        
        # Abutments at ends
        abutment_width = 3.0
        for x_pos in [0, self.params.span_length]:
            abutment = Rectangle((x_pos - abutment_width/2, -self.params.foundation_depth), 
                               abutment_width, self.params.height - self.params.girder_depth + self.params.foundation_depth,
                               facecolor=self.colors['supports'], alpha=0.6,
                               edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_elevation.add_patch(abutment)
        
        # Railings
        rail_y = self.params.height
        self.ax_elevation.plot([0, self.params.span_length], [rail_y, rail_y], 
                             color=self.colors['structure'], linewidth=1.5)
    
    def draw_beam_bridge_plan(self):
        """Generate plan view for beam bridge"""
        # Deck outline
        deck_plan = Rectangle((0, 0), self.params.span_length, self.params.deck_width,
                            facecolor=self.colors['plan_deck'], alpha=0.7,
                            edgecolor=self.colors['structure'], linewidth=self.line_width)
        self.ax_plan.add_patch(deck_plan)
        
        # Main girders (longitudinal)
        girder_width = 0.6
        girder_positions = [self.params.deck_width * 0.2, self.params.deck_width * 0.8]
        
        for y_pos in girder_positions:
            girder_plan = Rectangle((0, y_pos - girder_width/2), self.params.span_length, girder_width,
                                  facecolor=self.colors['plan_structure'], alpha=0.9,
                                  edgecolor=self.colors['structure'], linewidth=1)
            self.ax_plan.add_patch(girder_plan)
        
        # Cross-beams/diaphragms
        num_cross_beams = max(5, int(self.params.span_length / 15))
        cross_beam_spacing = self.params.span_length / (num_cross_beams - 1)
        cross_beam_width = 0.3
        
        for i in range(num_cross_beams):
            x_pos = i * cross_beam_spacing
            cross_beam = Rectangle((x_pos - cross_beam_width/2, 0), cross_beam_width, self.params.deck_width,
                                 facecolor=self.colors['plan_structure'], alpha=0.6,
                                 edgecolor=self.colors['structure'], linewidth=0.5)
            self.ax_plan.add_patch(cross_beam)
        
        # Supports/piers in plan
        if self.params.supports > 0:
            support_spacing = self.params.span_length / (self.params.supports + 1)
            support_width = 2.0
            support_depth = 1.5
            
            for i in range(self.params.supports):
                x_pos = support_spacing * (i + 1) - support_width / 2
                y_pos = (self.params.deck_width - support_depth) / 2
                
                pier_plan = Rectangle((x_pos, y_pos), support_width, support_depth,
                                    facecolor=self.colors['supports'], alpha=0.8,
                                    edgecolor=self.colors['structure'], linewidth=self.line_width)
                self.ax_plan.add_patch(pier_plan)
        
        # Centerline
        self.ax_plan.plot([0, self.params.span_length], [self.params.deck_width/2, self.params.deck_width/2], 
                         '--', color=self.colors['annotations'], linewidth=1, alpha=0.7)
        
        # Edge lines  
        self.ax_plan.plot([0, self.params.span_length], [0, 0], 
                         color=self.colors['structure'], linewidth=2)
        self.ax_plan.plot([0, self.params.span_length], [self.params.deck_width, self.params.deck_width], 
                         color=self.colors['structure'], linewidth=2)
    
    def draw_truss_bridge(self):
        """Generate elevation and plan views for truss bridge"""
        self.draw_truss_bridge_elevation()
        self.draw_truss_bridge_plan()
    
    def draw_truss_bridge_elevation(self):
        """Generate elevation view for truss bridge"""
        # Support multi-span capability (up to 30 spans)
        num_spans = min(max(1, self.params.supports + 1), 30)
        span_length = self.params.span_length / num_spans
        
        for span_idx in range(num_spans):
            span_start = span_idx * span_length
            span_end = (span_idx + 1) * span_length
            
            # Deck level for this span
            deck_y = self.params.height * 0.3
            deck = Rectangle((span_start, deck_y), span_length, 0.5,
                            facecolor=self.colors['deck'], alpha=0.7,
                            edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_elevation.add_patch(deck)
        
            # Truss structure for this span
            truss_height = self.params.height - deck_y - 1
            num_panels = max(4, int(span_length / 10))  # Panel every ~10m
            panel_width = span_length / num_panels
            
            # Top chord
            top_y = deck_y + truss_height
            self.ax_elevation.plot([span_start, span_end], [top_y, top_y], 
                                 color=self.colors['structure'], linewidth=self.line_width * 1.5)
            
            # Bottom chord (deck level)
            self.ax_elevation.plot([span_start, span_end], [deck_y, deck_y], 
                                 color=self.colors['structure'], linewidth=self.line_width * 1.5)
            
            # Vertical members and diagonals for this span
            for i in range(num_panels + 1):
                x = span_start + i * panel_width
                
                # Vertical members
                self.ax_elevation.plot([x, x], [deck_y, top_y], 
                                     color=self.colors['structure'], linewidth=self.line_width)
                
                # Diagonal members (alternating pattern)
                if i < num_panels:
                    x_next = span_start + (i + 1) * panel_width
                    if i % 2 == 0:
                        # Diagonal up-right
                        self.ax_elevation.plot([x, x_next], [deck_y, top_y], 
                                             color=self.colors['structure'], linewidth=self.line_width * 0.8)
                    else:
                        # Diagonal down-right  
                        self.ax_elevation.plot([x, x_next], [top_y, deck_y], 
                                             color=self.colors['structure'], linewidth=self.line_width * 0.8)
        
        # Supports at intermediate points and ends
        support_width = 2.5
        for i in range(num_spans + 1):
            x_pos = i * span_length
            support = Rectangle((x_pos - support_width/2, -self.params.foundation_depth), 
                              support_width, deck_y + self.params.foundation_depth,
                              facecolor=self.colors['supports'], alpha=0.8,
                              edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_elevation.add_patch(support)
    
    def draw_truss_bridge_plan(self):
        """Generate plan view for truss bridge"""
        # Deck outline
        deck_plan = Rectangle((0, 0), self.params.span_length, self.params.deck_width,
                            facecolor=self.colors['plan_deck'], alpha=0.7,
                            edgecolor=self.colors['structure'], linewidth=self.line_width)
        self.ax_plan.add_patch(deck_plan)
        
        # Main trusses (two parallel trusses)
        truss_width = 1.0
        truss_positions = [self.params.deck_width * 0.15, self.params.deck_width * 0.85]
        
        for y_pos in truss_positions:
            truss_plan = Rectangle((0, y_pos - truss_width/2), self.params.span_length, truss_width,
                                 facecolor=self.colors['plan_structure'], alpha=0.9,
                                 edgecolor=self.colors['structure'], linewidth=1.5)
            self.ax_plan.add_patch(truss_plan)
        
        # Cross-bracing/floor beams
        num_cross_frames = max(8, int(self.params.span_length / 10))
        cross_frame_spacing = self.params.span_length / (num_cross_frames - 1)
        
        for i in range(num_cross_frames):
            x_pos = i * cross_frame_spacing
            self.ax_plan.plot([x_pos, x_pos], [truss_positions[0], truss_positions[1]], 
                             color=self.colors['structure'], linewidth=1.5, alpha=0.8)
        
        # Support positions in plan
        num_spans = min(max(1, self.params.supports + 1), 30)
        span_length = self.params.span_length / num_spans
        support_width = 2.5
        
        for i in range(num_spans + 1):
            x_pos = i * span_length
            support_plan = Rectangle((x_pos - support_width/2, (self.params.deck_width - support_width)/2), 
                                   support_width, support_width,
                                   facecolor=self.colors['supports'], alpha=0.8,
                                   edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_plan.add_patch(support_plan)
    
    def draw_arch_bridge(self):
        """Generate elevation and plan views for arch bridge"""
        self.draw_arch_bridge_elevation()
        self.draw_arch_bridge_plan()
    
    def draw_arch_bridge_elevation(self):
        """Generate elevation view for arch bridge"""
        # Support multi-span arches
        num_spans = min(max(1, self.params.supports + 1), 30)
        span_length = self.params.span_length / num_spans
        
        for span_idx in range(num_spans):
            span_start = span_idx * span_length
            span_end = (span_idx + 1) * span_length
            
            # Arch parameters for this span
            arch_center_y = 0
            arch_rise = self.params.height * 0.7
            
            # Create arch using parametric equations
            theta = np.linspace(0, np.pi, 100)
            arch_x = span_length/2 * np.cos(theta) + span_start + span_length/2
            arch_y = arch_rise * np.sin(theta) + arch_center_y
            
            # Arch structure (hollow)
            arch_thickness = 2.0
            inner_x = (span_length/2 - arch_thickness) * np.cos(theta) + span_start + span_length/2
            inner_y = (arch_rise - arch_thickness) * np.sin(theta) + arch_center_y
            
            # Draw arch
            self.ax_elevation.fill_between(arch_x, arch_y, inner_y, 
                                         where=inner_y <= arch_y, alpha=0.8,
                                         facecolor=self.colors['structure'], 
                                         edgecolor=self.colors['structure'],
                                         linewidth=self.line_width)
            
            # Spandrel walls/supports between arch and deck for this span
            num_spandrels = max(3, int(span_length / 20))
            spandrel_spacing = span_length / (num_spandrels + 1)
            
            for i in range(1, num_spandrels + 1):
                x_pos = span_start + i * spandrel_spacing
                # Find corresponding arch height at this x position
                arch_height_at_x = arch_rise * np.sin(np.pi * (x_pos - span_start) / span_length)
                
                spandrel = Rectangle((x_pos - 0.3, arch_height_at_x), 0.6, 
                                   (arch_rise + 2) - arch_height_at_x,
                                   facecolor=self.colors['supports'], alpha=0.6,
                                   edgecolor=self.colors['structure'], linewidth=1)
                self.ax_elevation.add_patch(spandrel)
        
        # Continuous deck/roadway above arches
        deck_y = arch_rise + 2
        deck = Rectangle((0, deck_y), self.params.span_length, 0.8,
                        facecolor=self.colors['deck'], alpha=0.7,
                        edgecolor=self.colors['structure'], linewidth=self.line_width)
        self.ax_elevation.add_patch(deck)
        
        # Abutments and piers
        abutment_width = 4.0
        abutment_height = arch_rise + 5
        
        # End abutments
        for x_pos in [0, self.params.span_length]:
            abutment = Rectangle((x_pos - abutment_width/2, -self.params.foundation_depth), 
                               abutment_width, abutment_height + self.params.foundation_depth,
                               facecolor=self.colors['supports'], alpha=0.8,
                               edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_elevation.add_patch(abutment)
        
        # Intermediate piers for multi-span
        for i in range(1, num_spans):
            x_pos = i * span_length
            pier = Rectangle((x_pos - abutment_width/3, -self.params.foundation_depth), 
                           abutment_width * 2/3, abutment_height + self.params.foundation_depth,
                           facecolor=self.colors['supports'], alpha=0.8,
                           edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_elevation.add_patch(pier)
    
    def draw_arch_bridge_plan(self):
        """Generate plan view for arch bridge"""
        # Deck outline
        deck_plan = Rectangle((0, 0), self.params.span_length, self.params.deck_width,
                            facecolor=self.colors['plan_deck'], alpha=0.7,
                            edgecolor=self.colors['structure'], linewidth=self.line_width)
        self.ax_plan.add_patch(deck_plan)
        
        # Arch ribs (multiple parallel arches)
        num_ribs = 3  # Three parallel arch ribs
        rib_width = 1.0
        rib_spacing = self.params.deck_width / (num_ribs + 1)
        
        for i in range(num_ribs):
            y_pos = (i + 1) * rib_spacing - rib_width/2
            rib_plan = Rectangle((0, y_pos), self.params.span_length, rib_width,
                               facecolor=self.colors['plan_structure'], alpha=0.9,
                               edgecolor=self.colors['structure'], linewidth=1.5)
            self.ax_plan.add_patch(rib_plan)
        
        # Spandrel structure (cross-walls)
        num_spans = min(max(1, self.params.supports + 1), 30)
        span_length = self.params.span_length / num_spans
        
        for span_idx in range(num_spans):
            span_start = span_idx * span_length
            num_spandrels = max(3, int(span_length / 20))
            spandrel_spacing = span_length / (num_spandrels + 1)
            
            for i in range(1, num_spandrels + 1):
                x_pos = span_start + i * spandrel_spacing
                spandrel_plan = Rectangle((x_pos - 0.3, 0), 0.6, self.params.deck_width,
                                        facecolor=self.colors['plan_structure'], alpha=0.4,
                                        edgecolor=self.colors['structure'], linewidth=0.5)
                self.ax_plan.add_patch(spandrel_plan)
        
        # Supports in plan view
        support_width = 4.0
        
        # End abutments
        for x_pos in [0, self.params.span_length]:
            abutment_plan = Rectangle((x_pos - support_width/2, (self.params.deck_width - support_width)/2), 
                                    support_width, support_width,
                                    facecolor=self.colors['supports'], alpha=0.8,
                                    edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_plan.add_patch(abutment_plan)
        
        # Intermediate piers
        for i in range(1, num_spans):
            x_pos = i * span_length
            pier_plan = Rectangle((x_pos - support_width/3, (self.params.deck_width - support_width*2/3)/2), 
                                support_width * 2/3, support_width * 2/3,
                                facecolor=self.colors['supports'], alpha=0.8,
                                edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_plan.add_patch(pier_plan)
    
    def draw_suspension_bridge(self):
        """Generate elevation and plan views for suspension bridge"""
        self.draw_suspension_bridge_elevation()
        self.draw_suspension_bridge_plan()
    
    def draw_suspension_bridge_elevation(self):
        """Generate elevation view for suspension bridge"""
        # Towers
        tower_height = self.params.height
        tower_width = 3.0
        tower_positions = [self.params.span_length * 0.2, self.params.span_length * 0.8]
        
        for x_pos in tower_positions:
            # Tower shaft
            tower = Rectangle((x_pos - tower_width/2, -self.params.foundation_depth), 
                            tower_width, tower_height + self.params.foundation_depth,
                            facecolor=self.colors['supports'], alpha=0.8,
                            edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_elevation.add_patch(tower)
            
            # Tower top cross-beam
            crossbeam = Rectangle((x_pos - tower_width, tower_height - 2), 
                                tower_width * 2, 1,
                                facecolor=self.colors['structure'], alpha=0.9)
            self.ax_elevation.add_patch(crossbeam)
        
        # Main cables (catenary curve approximation)
        cable_sag = self.params.height * 0.3
        deck_y = self.params.height * 0.4
        
        # Main span cable
        x_cable = np.linspace(tower_positions[0], tower_positions[1], 100)
        y_cable = deck_y + cable_sag * (1 - 4 * (x_cable - self.params.span_length/2)**2 / 
                                       (tower_positions[1] - tower_positions[0])**2)
        self.ax_elevation.plot(x_cable, y_cable, color='black', linewidth=3, label='Main Cable')
        
        # Side span cables
        x_left = np.linspace(0, tower_positions[0], 50)
        y_left = tower_height - (tower_height - deck_y) * (x_left / tower_positions[0])**2
        self.ax_elevation.plot(x_left, y_left, color='black', linewidth=3)
        
        x_right = np.linspace(tower_positions[1], self.params.span_length, 50)
        y_right = tower_height - (tower_height - deck_y) * ((x_right - self.params.span_length) / 
                                                            (tower_positions[1] - self.params.span_length))**2
        self.ax_elevation.plot(x_right, y_right, color='black', linewidth=3)
        
        # Deck
        deck = Rectangle((0, deck_y), self.params.span_length, 0.8,
                        facecolor=self.colors['deck'], alpha=0.7,
                        edgecolor=self.colors['structure'], linewidth=self.line_width)
        self.ax_elevation.add_patch(deck)
        
        # Hangers (vertical cables)
        num_hangers = 20
        hanger_spacing = self.params.span_length / num_hangers
        
        for i in range(1, num_hangers):
            x_hanger = i * hanger_spacing
            if tower_positions[0] <= x_hanger <= tower_positions[1]:
                # Main span hanger
                y_cable_at_x = deck_y + cable_sag * (1 - 4 * (x_hanger - self.params.span_length/2)**2 / 
                                                    (tower_positions[1] - tower_positions[0])**2)
                self.ax_elevation.plot([x_hanger, x_hanger], [deck_y + 0.8, y_cable_at_x], 
                                     color='gray', linewidth=1, alpha=0.8)
        
        # Anchorages
        anchorage_width = 6.0
        for x_pos in [0, self.params.span_length]:
            anchorage = Rectangle((x_pos - anchorage_width/2, -self.params.foundation_depth), 
                                anchorage_width, deck_y + self.params.foundation_depth,
                                facecolor=self.colors['foundations'], alpha=0.8,
                                edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_elevation.add_patch(anchorage)
    
    def draw_suspension_bridge_plan(self):
        """Generate plan view for suspension bridge"""
        # Deck outline
        deck_plan = Rectangle((0, 0), self.params.span_length, self.params.deck_width,
                            facecolor=self.colors['plan_deck'], alpha=0.7,
                            edgecolor=self.colors['structure'], linewidth=self.line_width)
        self.ax_plan.add_patch(deck_plan)
        
        # Main cables (two parallel cables)
        cable_positions = [self.params.deck_width * 0.1, self.params.deck_width * 0.9]
        cable_width = 0.5
        
        for y_pos in cable_positions:
            cable_plan = Rectangle((0, y_pos - cable_width/2), self.params.span_length, cable_width,
                                 facecolor='black', alpha=0.9,
                                 edgecolor='black', linewidth=1)
            self.ax_plan.add_patch(cable_plan)
        
        # Towers in plan
        tower_positions = [self.params.span_length * 0.2, self.params.span_length * 0.8]
        tower_width = 3.0
        tower_depth = 2.0
        
        for x_pos in tower_positions:
            tower_plan = Rectangle((x_pos - tower_width/2, (self.params.deck_width - tower_depth)/2), 
                                 tower_width, tower_depth,
                                 facecolor=self.colors['supports'], alpha=0.8,
                                 edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_plan.add_patch(tower_plan)
        
        # Deck stiffening trusses/girders
        truss_positions = [self.params.deck_width * 0.25, self.params.deck_width * 0.75]
        truss_width = 0.8
        
        for y_pos in truss_positions:
            truss_plan = Rectangle((0, y_pos - truss_width/2), self.params.span_length, truss_width,
                                 facecolor=self.colors['plan_structure'], alpha=0.6,
                                 edgecolor=self.colors['structure'], linewidth=1)
            self.ax_plan.add_patch(truss_plan)
        
        # Anchorages in plan
        anchorage_width = 6.0
        for x_pos in [0, self.params.span_length]:
            anchorage_plan = Rectangle((x_pos - anchorage_width/2, (self.params.deck_width - anchorage_width)/2), 
                                     anchorage_width, anchorage_width,
                                     facecolor=self.colors['foundations'], alpha=0.8,
                                     edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_plan.add_patch(anchorage_plan)
    
    def draw_cable_stayed_bridge(self):
        """Generate elevation and plan views for cable-stayed bridge"""
        self.draw_cable_stayed_bridge_elevation()
        self.draw_cable_stayed_bridge_plan()
    
    def draw_cable_stayed_bridge_elevation(self):
        """Generate elevation view for cable-stayed bridge"""
        # Support multi-tower design for longer spans
        num_spans = min(max(1, self.params.supports + 1), 30)
        span_length = self.params.span_length / num_spans
        
        # Tower positions (at each support point)
        tower_positions = []
        for i in range(self.params.supports):
            tower_positions.append((i + 1) * span_length)
        
        tower_height = self.params.height
        tower_width = 4.0
        
        # Draw towers
        for tower_x in tower_positions:
            tower = Rectangle((tower_x - tower_width/2, -self.params.foundation_depth), 
                            tower_width, tower_height + self.params.foundation_depth,
                            facecolor=self.colors['supports'], alpha=0.8,
                            edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_elevation.add_patch(tower)
        
        # Deck
        deck_y = self.params.height * 0.3
        deck = Rectangle((0, deck_y), self.params.span_length, 0.8,
                        facecolor=self.colors['deck'], alpha=0.7,
                        edgecolor=self.colors['structure'], linewidth=self.line_width)
        self.ax_elevation.add_patch(deck)
        
        # Stay cables for each tower
        num_cables = max(4, int(span_length / 15))  # Scale cables with span length
        cable_attachment_height = tower_height * 0.8
        
        for tower_x in tower_positions:
            for i in range(1, num_cables + 1):
                # Left side cables from this tower
                if tower_x > 0:
                    deck_x_left = tower_x - (i * min(tower_x, span_length) / (num_cables + 1))
                    if deck_x_left >= 0:
                        self.ax_elevation.plot([tower_x, deck_x_left], [cable_attachment_height, deck_y + 0.8], 
                                             color='red', linewidth=2, alpha=0.8)
                
                # Right side cables from this tower
                if tower_x < self.params.span_length:
                    deck_x_right = tower_x + (i * min(self.params.span_length - tower_x, span_length) / (num_cables + 1))
                    if deck_x_right <= self.params.span_length:
                        self.ax_elevation.plot([tower_x, deck_x_right], [cable_attachment_height, deck_y + 0.8], 
                                             color='red', linewidth=2, alpha=0.8)
        
        # Abutments at ends
        abutment_width = 5.0
        for x_pos in [0, self.params.span_length]:
            abutment = Rectangle((x_pos - abutment_width/2, -self.params.foundation_depth), 
                               abutment_width, deck_y + self.params.foundation_depth,
                               facecolor=self.colors['supports'], alpha=0.8,
                               edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_elevation.add_patch(abutment)
    
    def draw_cable_stayed_bridge_plan(self):
        """Generate plan view for cable-stayed bridge"""
        # Deck outline
        deck_plan = Rectangle((0, 0), self.params.span_length, self.params.deck_width,
                            facecolor=self.colors['plan_deck'], alpha=0.7,
                            edgecolor=self.colors['structure'], linewidth=self.line_width)
        self.ax_plan.add_patch(deck_plan)
        
        # Tower positions in plan
        num_spans = min(max(1, self.params.supports + 1), 30)
        span_length = self.params.span_length / num_spans
        tower_width = 4.0
        tower_depth = 3.0
        
        tower_positions = []
        for i in range(self.params.supports):
            tower_positions.append((i + 1) * span_length)
        
        for tower_x in tower_positions:
            tower_plan = Rectangle((tower_x - tower_width/2, (self.params.deck_width - tower_depth)/2), 
                                 tower_width, tower_depth,
                                 facecolor=self.colors['supports'], alpha=0.8,
                                 edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_plan.add_patch(tower_plan)
        
        # Cable arrangement (stays in plan view)
        cable_positions = [self.params.deck_width * 0.15, self.params.deck_width * 0.85]
        
        for tower_x in tower_positions:
            for y_cable in cable_positions:
                # Draw cable lines radiating from tower center
                num_cables = max(4, int(span_length / 15))
                for i in range(1, num_cables + 1):
                    # Left side cables
                    if tower_x > 0:
                        deck_x_left = tower_x - (i * min(tower_x, span_length) / (num_cables + 1))
                        if deck_x_left >= 0:
                            self.ax_plan.plot([tower_x, deck_x_left], [self.params.deck_width/2, y_cable], 
                                            color='red', linewidth=1, alpha=0.6)
                    
                    # Right side cables
                    if tower_x < self.params.span_length:
                        deck_x_right = tower_x + (i * min(self.params.span_length - tower_x, span_length) / (num_cables + 1))
                        if deck_x_right <= self.params.span_length:
                            self.ax_plan.plot([tower_x, deck_x_right], [self.params.deck_width/2, y_cable], 
                                            color='red', linewidth=1, alpha=0.6)
        
        # Main girders
        girder_positions = [self.params.deck_width * 0.2, self.params.deck_width * 0.8]
        girder_width = 0.8
        
        for y_pos in girder_positions:
            girder_plan = Rectangle((0, y_pos - girder_width/2), self.params.span_length, girder_width,
                                  facecolor=self.colors['plan_structure'], alpha=0.6,
                                  edgecolor=self.colors['structure'], linewidth=1)
            self.ax_plan.add_patch(girder_plan)
        
        # Abutments in plan
        abutment_width = 5.0
        for x_pos in [0, self.params.span_length]:
            abutment_plan = Rectangle((x_pos - abutment_width/2, (self.params.deck_width - abutment_width)/2), 
                                    abutment_width, abutment_width,
                                    facecolor=self.colors['supports'], alpha=0.8,
                                    edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_plan.add_patch(abutment_plan)
    
    def draw_t_beam_bridge(self):
        """Generate elevation and plan views for T-beam bridge"""
        self.draw_t_beam_bridge_elevation()
        self.draw_t_beam_bridge_plan()
    
    def draw_t_beam_bridge_elevation(self):
        """Generate elevation view for T-beam bridge"""
        # Support multi-span capability
        num_spans = min(max(1, self.params.supports + 1), 30)
        span_length = self.params.span_length / num_spans
        
        # Main deck slab
        deck_y = self.params.height - self.params.girder_depth
        deck_thickness = 0.6  # Deck slab thickness
        deck = Rectangle((0, deck_y), self.params.span_length, deck_thickness,
                        facecolor=self.colors['deck'], alpha=0.7,
                        edgecolor=self.colors['structure'], linewidth=self.line_width)
        self.ax_elevation.add_patch(deck)
        
        # T-beam girders (showing the T-shape in elevation)
        girder_height = self.params.girder_depth - deck_thickness
        girder_y = deck_y - girder_height
        
        # Number of T-beams based on deck width
        num_beams = max(3, int(self.params.deck_width / 3))  # T-beam every ~3m
        beam_spacing = self.params.span_length / 20  # Show beams every 20m for visibility
        
        for i in range(0, int(self.params.span_length / beam_spacing) + 1):
            x_pos = i * beam_spacing
            if x_pos <= self.params.span_length:
                # Web of T-beam (vertical part)
                web_width = 0.4
                web = Rectangle((x_pos - web_width/2, girder_y), web_width, girder_height,
                              facecolor=self.colors['structure'], alpha=0.8,
                              edgecolor=self.colors['structure'], linewidth=1)
                self.ax_elevation.add_patch(web)
                
                # Flange of T-beam (bottom horizontal part)
                flange_width = 1.2
                flange_height = 0.3
                flange = Rectangle((x_pos - flange_width/2, girder_y - flange_height), 
                                 flange_width, flange_height,
                                 facecolor=self.colors['structure'], alpha=0.8,
                                 edgecolor=self.colors['structure'], linewidth=1)
                self.ax_elevation.add_patch(flange)
        
        # Supports/piers for multi-span
        if num_spans > 1:
            support_width = 2.0
            for i in range(1, num_spans):
                x_pos = i * span_length - support_width / 2
                pier = Rectangle((x_pos, -self.params.foundation_depth), 
                               support_width, self.params.height - self.params.girder_depth + self.params.foundation_depth,
                               facecolor=self.colors['supports'], alpha=0.8,
                               edgecolor=self.colors['structure'], linewidth=self.line_width)
                self.ax_elevation.add_patch(pier)
        
        # Abutments at ends
        abutment_width = 3.0
        for x_pos in [0, self.params.span_length]:
            abutment = Rectangle((x_pos - abutment_width/2, -self.params.foundation_depth), 
                               abutment_width, self.params.height - self.params.girder_depth + self.params.foundation_depth,
                               facecolor=self.colors['supports'], alpha=0.6,
                               edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_elevation.add_patch(abutment)
    
    def draw_t_beam_bridge_plan(self):
        """Generate plan view for T-beam bridge"""
        # Deck slab outline
        deck_plan = Rectangle((0, 0), self.params.span_length, self.params.deck_width,
                            facecolor=self.colors['plan_deck'], alpha=0.7,
                            edgecolor=self.colors['structure'], linewidth=self.line_width)
        self.ax_plan.add_patch(deck_plan)
        
        # T-beam girders (longitudinal beams)
        num_beams = max(3, int(self.params.deck_width / 3))  # T-beam every ~3m
        beam_spacing = self.params.deck_width / (num_beams + 1)
        beam_width = 0.4  # Web width of T-beam
        
        for i in range(num_beams):
            y_pos = (i + 1) * beam_spacing - beam_width/2
            beam_plan = Rectangle((0, y_pos), self.params.span_length, beam_width,
                                facecolor=self.colors['plan_structure'], alpha=0.9,
                                edgecolor=self.colors['structure'], linewidth=1.5)
            self.ax_plan.add_patch(beam_plan)
        
        # Diaphragms/cross-beams
        num_diaphragms = max(5, int(self.params.span_length / 20))
        diaphragm_spacing = self.params.span_length / (num_diaphragms - 1)
        diaphragm_width = 0.3
        
        for i in range(num_diaphragms):
            x_pos = i * diaphragm_spacing
            diaphragm = Rectangle((x_pos - diaphragm_width/2, 0), diaphragm_width, self.params.deck_width,
                                facecolor=self.colors['plan_structure'], alpha=0.6,
                                edgecolor=self.colors['structure'], linewidth=0.8)
            self.ax_plan.add_patch(diaphragm)
        
        # Support locations in plan
        num_spans = min(max(1, self.params.supports + 1), 30)
        span_length = self.params.span_length / num_spans
        support_width = 2.0
        
        # Intermediate supports
        for i in range(1, num_spans):
            x_pos = i * span_length
            support_plan = Rectangle((x_pos - support_width/2, (self.params.deck_width - support_width)/2), 
                                   support_width, support_width,
                                   facecolor=self.colors['supports'], alpha=0.8,
                                   edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_plan.add_patch(support_plan)
        
        # End abutments
        abutment_width = 3.0
        for x_pos in [0, self.params.span_length]:
            abutment_plan = Rectangle((x_pos - abutment_width/2, (self.params.deck_width - abutment_width)/2), 
                                    abutment_width, abutment_width,
                                    facecolor=self.colors['supports'], alpha=0.6,
                                    edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_plan.add_patch(abutment_plan)
    
    def draw_slab_bridge(self):
        """Generate elevation and plan views for slab bridge"""
        self.draw_slab_bridge_elevation()
        self.draw_slab_bridge_plan()
    
    def draw_slab_bridge_elevation(self):
        """Generate elevation view for slab bridge"""
        # Support multi-span capability
        num_spans = min(max(1, self.params.supports + 1), 30)
        span_length = self.params.span_length / num_spans
        
        # Main concrete slab (thick deck structure)
        slab_thickness = max(0.8, self.params.span_length / 100)  # Slab thickness scales with span
        deck_y = self.params.height - slab_thickness
        
        # Draw slab as continuous structure
        slab = Rectangle((0, deck_y), self.params.span_length, slab_thickness,
                        facecolor=self.colors['deck'], alpha=0.8,
                        edgecolor=self.colors['structure'], linewidth=self.line_width)
        self.ax_elevation.add_patch(slab)
        
        # Show reinforcement pattern (simplified representation)
        rebar_spacing = 2.0  # Show rebar every 2m
        for x in range(0, int(self.params.span_length), int(rebar_spacing)):
            # Longitudinal reinforcement (bottom)
            self.ax_elevation.plot([x, x + rebar_spacing], [deck_y + 0.1, deck_y + 0.1], 
                                 color='darkred', linewidth=2, alpha=0.7)
            # Transverse reinforcement
            self.ax_elevation.plot([x + rebar_spacing/2, x + rebar_spacing/2], 
                                 [deck_y + 0.1, deck_y + slab_thickness - 0.1], 
                                 color='darkred', linewidth=1, alpha=0.5)
        
        # Supports/piers for multi-span
        if num_spans > 1:
            support_width = 2.5
            for i in range(1, num_spans):
                x_pos = i * span_length - support_width / 2
                pier = Rectangle((x_pos, -self.params.foundation_depth), 
                               support_width, deck_y + self.params.foundation_depth,
                               facecolor=self.colors['supports'], alpha=0.8,
                               edgecolor=self.colors['structure'], linewidth=self.line_width)
                self.ax_elevation.add_patch(pier)
        
        # Abutments at ends (wider for slab bridges)
        abutment_width = 4.0
        for x_pos in [0, self.params.span_length]:
            abutment = Rectangle((x_pos - abutment_width/2, -self.params.foundation_depth), 
                               abutment_width, deck_y + self.params.foundation_depth,
                               facecolor=self.colors['supports'], alpha=0.8,
                               edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_elevation.add_patch(abutment)
        
        # Expansion joints (for multi-span)
        if num_spans > 1:
            for i in range(1, num_spans):
                x_pos = i * span_length
                # Show expansion joint as a gap
                joint = Rectangle((x_pos - 0.05, deck_y), 0.1, slab_thickness,
                                facecolor='white', alpha=1.0,
                                edgecolor=self.colors['structure'], linewidth=1)
                self.ax_elevation.add_patch(joint)
    
    def draw_slab_bridge_plan(self):
        """Generate plan view for slab bridge"""
        # Main slab outline
        slab_plan = Rectangle((0, 0), self.params.span_length, self.params.deck_width,
                            facecolor=self.colors['plan_deck'], alpha=0.8,
                            edgecolor=self.colors['structure'], linewidth=self.line_width)
        self.ax_plan.add_patch(slab_plan)
        
        # Reinforcement pattern in plan view
        rebar_spacing_long = 3.0  # Longitudinal spacing
        rebar_spacing_trans = 2.5  # Transverse spacing
        
        # Longitudinal reinforcement lines
        for y in range(0, int(self.params.deck_width), int(rebar_spacing_trans)):
            if y <= self.params.deck_width:
                self.ax_plan.plot([0, self.params.span_length], [y, y], 
                                color='darkred', linewidth=0.8, alpha=0.6, linestyle='--')
        
        # Transverse reinforcement lines  
        for x in range(0, int(self.params.span_length), int(rebar_spacing_long)):
            if x <= self.params.span_length:
                self.ax_plan.plot([x, x], [0, self.params.deck_width], 
                                color='darkred', linewidth=0.8, alpha=0.6, linestyle='--')
        
        # Construction joints (for large slabs)
        if self.params.span_length > 30:
            num_joints = int(self.params.span_length / 30)
            joint_spacing = self.params.span_length / (num_joints + 1)
            
            for i in range(1, num_joints + 1):
                x_pos = i * joint_spacing
                self.ax_plan.plot([x_pos, x_pos], [0, self.params.deck_width], 
                                color=self.colors['annotations'], linewidth=2, alpha=0.8, linestyle=':')
        
        # Support locations in plan
        num_spans = min(max(1, self.params.supports + 1), 30)
        span_length = self.params.span_length / num_spans
        support_width = 2.5
        
        # Intermediate supports
        for i in range(1, num_spans):
            x_pos = i * span_length
            support_plan = Rectangle((x_pos - support_width/2, (self.params.deck_width - support_width)/2), 
                                   support_width, support_width,
                                   facecolor=self.colors['supports'], alpha=0.8,
                                   edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_plan.add_patch(support_plan)
        
        # End abutments
        abutment_width = 4.0
        for x_pos in [0, self.params.span_length]:
            abutment_plan = Rectangle((x_pos - abutment_width/2, (self.params.deck_width - abutment_width)/2), 
                                    abutment_width, abutment_width,
                                    facecolor=self.colors['supports'], alpha=0.8,
                                    edgecolor=self.colors['structure'], linewidth=self.line_width)
            self.ax_plan.add_patch(abutment_plan)
        
        # Edge markings to show slab thickness
        edge_marking_spacing = 10.0
        for x in range(0, int(self.params.span_length), int(edge_marking_spacing)):
            if x <= self.params.span_length:
                # Top edge markings
                self.ax_plan.plot([x, x + 2], [self.params.deck_width, self.params.deck_width], 
                                color=self.colors['structure'], linewidth=3, alpha=0.8)
                # Bottom edge markings
                self.ax_plan.plot([x, x + 2], [0, 0], 
                                color=self.colors['structure'], linewidth=3, alpha=0.8)
    
    def _add_dimensions(self):
        """Add dimension lines and annotations to both views"""
        # Elevation view dimensions
        dim_y = self.params.height + 10
        self.ax_elevation.annotate('', xy=(0, dim_y), xytext=(self.params.span_length, dim_y),
                                 arrowprops=dict(arrowstyle='<->', color=self.colors['dimensions'], lw=1.5))
        self.ax_elevation.text(self.params.span_length/2, dim_y + 2, f'{self.params.span_length:.0f} m',
                             ha='center', va='bottom', fontsize=self.dimension_fontsize, 
                             color=self.colors['dimensions'], weight='bold')
        
        # Height dimension
        dim_x = self.params.span_length + 15
        self.ax_elevation.annotate('', xy=(dim_x, 0), xytext=(dim_x, self.params.height),
                                 arrowprops=dict(arrowstyle='<->', color=self.colors['dimensions'], lw=1.5))
        self.ax_elevation.text(dim_x + 2, self.params.height/2, f'{self.params.height:.0f} m',
                             ha='left', va='center', fontsize=self.dimension_fontsize, 
                             color=self.colors['dimensions'], weight='bold', rotation=90)
        
        # Plan view dimensions
        dim_y_plan = self.params.deck_width + 3
        self.ax_plan.annotate('', xy=(0, dim_y_plan), xytext=(self.params.span_length, dim_y_plan),
                            arrowprops=dict(arrowstyle='<->', color=self.colors['dimensions'], lw=1.5))
        self.ax_plan.text(self.params.span_length/2, dim_y_plan + 1, f'{self.params.span_length:.0f} m',
                        ha='center', va='bottom', fontsize=self.dimension_fontsize, 
                        color=self.colors['dimensions'], weight='bold')
        
        # Width dimension
        dim_x_plan = self.params.span_length + 10
        self.ax_plan.annotate('', xy=(dim_x_plan, 0), xytext=(dim_x_plan, self.params.deck_width),
                            arrowprops=dict(arrowstyle='<->', color=self.colors['dimensions'], lw=1.5))
        self.ax_plan.text(dim_x_plan + 1, self.params.deck_width/2, f'{self.params.deck_width:.1f} m',
                        ha='left', va='center', fontsize=self.dimension_fontsize, 
                        color=self.colors['dimensions'], weight='bold', rotation=90)
        
        # Add specification text box to elevation view
        num_spans = min(max(1, self.params.supports + 1), 30)
        specs_text = f"""Bridge Specifications:
Type: {self.bridge_type.value.title()}
Total Length: {self.params.span_length:.0f} m
Number of Spans: {num_spans}
Span Length: {self.params.span_length/num_spans:.1f} m
Width: {self.params.deck_width:.1f} m
Height: {self.params.height:.0f} m
Material: {self.params.material.title()}
Load: {self.params.load_capacity:.0f} kN/m"""
        
        self.ax_elevation.text(0.02, 0.98, specs_text, transform=self.ax_elevation.transAxes,
                             fontsize=8, verticalalignment='top',
                             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    def generate_drawing(self):
        """Main method to generate the bridge drawing"""
        self.setup_drawing()
        
        # Call appropriate drawing method based on bridge type
        if self.bridge_type == BridgeType.BEAM:
            self.draw_beam_bridge()
        elif self.bridge_type == BridgeType.TRUSS:
            self.draw_truss_bridge()
        elif self.bridge_type == BridgeType.ARCH:
            self.draw_arch_bridge()
        elif self.bridge_type == BridgeType.SUSPENSION:
            self.draw_suspension_bridge()
        elif self.bridge_type == BridgeType.CABLE_STAYED:
            self.draw_cable_stayed_bridge()
        elif self.bridge_type == BridgeType.T_BEAM:
            self.draw_t_beam_bridge()
        elif self.bridge_type == BridgeType.SLAB:
            self.draw_slab_bridge()
        else:
            raise ValueError(f"Unsupported bridge type: {self.bridge_type}")
        
        plt.tight_layout()
        return self.figure
    
    def save_drawing(self, filename: str, format: OutputFormat = OutputFormat.PNG, dpi: int = 300):
        """Save the drawing in specified format"""
        if not self.figure:
            raise ValueError("No drawing generated. Call generate_drawing() first.")
        
        base_name = os.path.splitext(filename)[0]
        
        if format == OutputFormat.PNG or format == OutputFormat.ALL:
            self.figure.savefig(f"{base_name}.png", dpi=dpi, bbox_inches='tight', 
                              facecolor='white', edgecolor='none')
            print(f"Saved PNG: {base_name}.png")
        
        if format == OutputFormat.SVG or format == OutputFormat.ALL:
            self.figure.savefig(f"{base_name}.svg", format='svg', bbox_inches='tight',
                              facecolor='white', edgecolor='none')
            print(f"Saved SVG: {base_name}.svg")
        
        if format == OutputFormat.PDF or format == OutputFormat.ALL:
            self.figure.savefig(f"{base_name}.pdf", format='pdf', bbox_inches='tight',
                              facecolor='white', edgecolor='none')
            print(f"Saved PDF: {base_name}.pdf")
        
        if format == OutputFormat.DXF or format == OutputFormat.ALL:
            self.save_as_dxf(f"{base_name}.dxf")
            print(f"Saved DXF: {base_name}.dxf")
    
    def save_as_dxf(self, filename: str):
        """Save bridge drawing as DXF file for AutoCAD compatibility"""
        try:
            # Create new DXF document
            doc = ezdxf.new('R2010')  # AutoCAD 2010 format for wide compatibility
            msp = doc.modelspace()
            
            # Add layers for different elements
            doc.layers.add('FOUNDATION', color=2)  # Yellow
            doc.layers.add('STRUCTURE', color=1)   # Red  
            doc.layers.add('DECK', color=3)        # Green
            doc.layers.add('RAILINGS', color=4)    # Cyan
            doc.layers.add('DIMENSIONS', color=5)  # Blue
            doc.layers.add('TEXT', color=7)        # White/Black
            
            # Convert bridge elements to DXF entities
            self._add_bridge_elements_to_dxf(msp)
            
            # Save DXF file
            doc.saveas(filename)
            
        except Exception as e:
            raise RuntimeError(f"Failed to create DXF file: {str(e)}")
    
    def _add_bridge_elements_to_dxf(self, msp):
        """Add bridge structural elements to DXF modelspace"""
        span = self.params.span_length
        height = self.params.height
        width = self.params.deck_width
        
        # Foundation elements
        found_width = 8.0
        found_height = self.params.foundation_depth
        
        # Left abutment foundation
        msp.add_lwpolyline([
            (0, 0),
            (found_width, 0),
            (found_width, -found_height),
            (0, -found_height),
            (0, 0)
        ], dxfattribs={'layer': 'FOUNDATION'})
        
        # Right abutment foundation  
        msp.add_lwpolyline([
            (span - found_width, 0),
            (span, 0),
            (span, -found_height),
            (span - found_width, -found_height),
            (span - found_width, 0)
        ], dxfattribs={'layer': 'FOUNDATION'})
        
        # Bridge-specific elements
        if self.bridge_type == BridgeType.BEAM:
            self._add_beam_bridge_to_dxf(msp, span, height, width)
        elif self.bridge_type == BridgeType.TRUSS:
            self._add_truss_bridge_to_dxf(msp, span, height, width)
        elif self.bridge_type == BridgeType.ARCH:
            self._add_arch_bridge_to_dxf(msp, span, height, width)
        elif self.bridge_type == BridgeType.SUSPENSION:
            self._add_suspension_bridge_to_dxf(msp, span, height, width)
        elif self.bridge_type == BridgeType.CABLE_STAYED:
            self._add_cable_stayed_bridge_to_dxf(msp, span, height, width)
        
        # Add dimensions
        self._add_dimensions_to_dxf(msp, span, height)
        
        # Add text specifications
        self._add_text_to_dxf(msp, span)
    
    def _add_beam_bridge_to_dxf(self, msp, span, height, width):
        """Add beam bridge elements to DXF"""
        deck_thickness = 1.0
        deck_y = height - deck_thickness
        
        # Deck
        msp.add_lwpolyline([
            (0, deck_y),
            (span, deck_y),
            (span, height),
            (0, height),
            (0, deck_y)
        ], dxfattribs={'layer': 'DECK'})
        
        # Girders
        girder_depth = self.params.girder_depth
        num_girders = 4
        for i in range(num_girders):
            x = (i + 1) * span / (num_girders + 1)
            msp.add_line((x, 0), (x, deck_y), dxfattribs={'layer': 'STRUCTURE'})
            # Girder depth
            msp.add_lwpolyline([
                (x - 0.3, deck_y - girder_depth),
                (x + 0.3, deck_y - girder_depth),
                (x + 0.3, deck_y),
                (x - 0.3, deck_y),
                (x - 0.3, deck_y - girder_depth)
            ], dxfattribs={'layer': 'STRUCTURE'})
        
        # Railings
        rail_height = self.params.rail_height
        msp.add_line((0, height), (0, height + rail_height), dxfattribs={'layer': 'RAILINGS'})
        msp.add_line((span, height), (span, height + rail_height), dxfattribs={'layer': 'RAILINGS'})
        msp.add_line((0, height + rail_height), (span, height + rail_height), dxfattribs={'layer': 'RAILINGS'})
    
    def _add_truss_bridge_to_dxf(self, msp, span, height, width):
        """Add truss bridge elements to DXF"""
        deck_y = height * 0.2
        truss_top = height
        
        # Deck
        msp.add_line((0, deck_y), (span, deck_y), dxfattribs={'layer': 'DECK'})
        
        # Top and bottom chords
        msp.add_line((0, truss_top), (span, truss_top), dxfattribs={'layer': 'STRUCTURE'})
        msp.add_line((0, deck_y), (span, deck_y), dxfattribs={'layer': 'STRUCTURE'})
        
        # Verticals and diagonals
        num_panels = 8
        panel_length = span / num_panels
        
        for i in range(num_panels + 1):
            x = i * panel_length
            # Verticals
            msp.add_line((x, deck_y), (x, truss_top), dxfattribs={'layer': 'STRUCTURE'})
            
            # Diagonals
            if i < num_panels:
                x_next = (i + 1) * panel_length
                msp.add_line((x, deck_y), (x_next, truss_top), dxfattribs={'layer': 'STRUCTURE'})
                msp.add_line((x, truss_top), (x_next, deck_y), dxfattribs={'layer': 'STRUCTURE'})
    
    def _add_arch_bridge_to_dxf(self, msp, span, height, width):
        """Add arch bridge elements to DXF"""
        deck_y = height * 0.8
        arch_rise = height * 0.6
        
        # Deck
        msp.add_line((0, deck_y), (span, deck_y), dxfattribs={'layer': 'DECK'})
        
        # Arch (approximated with line segments)
        num_segments = 20
        arch_points = []
        for i in range(num_segments + 1):
            x = i * span / num_segments
            # Parabolic arch
            y = arch_rise * (1 - (2 * x / span - 1) ** 2)
            arch_points.append((x, y))
        
        msp.add_lwpolyline(arch_points, dxfattribs={'layer': 'STRUCTURE'})
    
    def _add_suspension_bridge_to_dxf(self, msp, span, height, width):
        """Add suspension bridge elements to DXF"""
        tower_width = 2.0
        tower_height = height
        deck_y = height * 0.3
        
        # Towers
        tower1_x = span * 0.25
        tower2_x = span * 0.75
        
        msp.add_line((tower1_x, 0), (tower1_x, tower_height), dxfattribs={'layer': 'STRUCTURE'})
        msp.add_line((tower2_x, 0), (tower2_x, tower_height), dxfattribs={'layer': 'STRUCTURE'})
        
        # Deck
        msp.add_line((0, deck_y), (span, deck_y), dxfattribs={'layer': 'DECK'})
        
        # Main cables (parabolic curve)
        num_points = 30
        cable_points = []
        for i in range(num_points + 1):
            x = i * span / num_points
            # Parabolic cable shape
            if tower1_x <= x <= tower2_x:
                y = deck_y + 0.1 * ((x - span/2) / (span/4)) ** 2 * (tower_height - deck_y)
            else:
                y = tower_height
            cable_points.append((x, y))
        
        msp.add_lwpolyline(cable_points, dxfattribs={'layer': 'STRUCTURE'})
        
        # Hangers
        for i in range(1, num_points):
            x = i * span / num_points
            if tower1_x < x < tower2_x:
                cable_y = deck_y + 0.1 * ((x - span/2) / (span/4)) ** 2 * (tower_height - deck_y)
                msp.add_line((x, deck_y), (x, cable_y), dxfattribs={'layer': 'STRUCTURE'})
    
    def _add_cable_stayed_bridge_to_dxf(self, msp, span, height, width):
        """Add cable-stayed bridge elements to DXF"""
        tower_x = span / 2
        tower_height = height
        deck_y = height * 0.2
        
        # Tower
        msp.add_line((tower_x, 0), (tower_x, tower_height), dxfattribs={'layer': 'STRUCTURE'})
        
        # Deck
        msp.add_line((0, deck_y), (span, deck_y), dxfattribs={'layer': 'DECK'})
        
        # Cables
        num_cables = 8
        for i in range(1, num_cables + 1):
            # Left side cables
            x_left = i * tower_x / (num_cables + 1)
            cable_top_y = tower_height * (1 - i / (num_cables + 2))
            msp.add_line((x_left, deck_y), (tower_x, cable_top_y), dxfattribs={'layer': 'STRUCTURE'})
            
            # Right side cables
            x_right = tower_x + i * tower_x / (num_cables + 1)
            msp.add_line((x_right, deck_y), (tower_x, cable_top_y), dxfattribs={'layer': 'STRUCTURE'})
    
    def _add_dimensions_to_dxf(self, msp, span, height):
        """Add dimension lines to DXF"""
        # Span dimension
        dim_y = -5
        msp.add_line((0, dim_y), (span, dim_y), dxfattribs={'layer': 'DIMENSIONS'})
        msp.add_line((0, dim_y - 1), (0, dim_y + 1), dxfattribs={'layer': 'DIMENSIONS'})
        msp.add_line((span, dim_y - 1), (span, dim_y + 1), dxfattribs={'layer': 'DIMENSIONS'})
        
        # Height dimension
        dim_x = span + 5
        msp.add_line((dim_x, 0), (dim_x, height), dxfattribs={'layer': 'DIMENSIONS'})
        msp.add_line((dim_x - 1, 0), (dim_x + 1, 0), dxfattribs={'layer': 'DIMENSIONS'})
        msp.add_line((dim_x - 1, height), (dim_x + 1, height), dxfattribs={'layer': 'DIMENSIONS'})
    
    def _add_text_to_dxf(self, msp, span):
        """Add text annotations to DXF"""
        from ezdxf.enums import TextEntityAlignment
        
        # Title
        title_text = f"{self.bridge_type.value.title().replace('_', ' ')} Bridge"
        title = msp.add_text(title_text, dxfattribs={'layer': 'TEXT', 'height': 3})
        title.set_placement((span/2, -15), align=TextEntityAlignment.MIDDLE_CENTER)
        
        # Specifications
        specs = [
            f"Span: {self.params.span_length:.0f}m",
            f"Width: {self.params.deck_width:.0f}m", 
            f"Height: {self.params.height:.0f}m",
            f"Material: {self.params.material.title()}",
            f"Load: {self.params.load_capacity:.0f} kN/m"
        ]
        
        for i, spec in enumerate(specs):
            spec_text = msp.add_text(spec, dxfattribs={'layer': 'TEXT', 'height': 1.5})
            spec_text.set_placement((5, -25 - i*3), align=TextEntityAlignment.LEFT)


def create_example_bridges():
    """Create example bridges of different types"""
    examples = []
    
    # Beam bridge example
    beam_params = BridgeParameters(
        span_length=40.0,
        deck_width=12.0,
        height=8.0,
        supports=1,
        load_capacity=50.0,
        material="concrete"
    )
    examples.append((BridgeType.BEAM, beam_params, "beam_bridge_example"))
    
    # Truss bridge example
    truss_params = BridgeParameters(
        span_length=80.0,
        deck_width=15.0,
        height=20.0,
        supports=0,
        load_capacity=75.0,
        material="steel"
    )
    examples.append((BridgeType.TRUSS, truss_params, "truss_bridge_example"))
    
    # Arch bridge example
    arch_params = BridgeParameters(
        span_length=60.0,
        deck_width=14.0,
        height=25.0,
        supports=0,
        load_capacity=100.0,
        material="stone"
    )
    examples.append((BridgeType.ARCH, arch_params, "arch_bridge_example"))
    
    # Suspension bridge example
    suspension_params = BridgeParameters(
        span_length=200.0,
        deck_width=20.0,
        height=80.0,
        supports=0,
        load_capacity=120.0,
        material="steel"
    )
    examples.append((BridgeType.SUSPENSION, suspension_params, "suspension_bridge_example"))
    
    # Cable-stayed bridge example
    cable_stayed_params = BridgeParameters(
        span_length=150.0,
        deck_width=18.0,
        height=60.0,
        supports=0,
        load_capacity=100.0,
        material="steel"
    )
    examples.append((BridgeType.CABLE_STAYED, cable_stayed_params, "cable_stayed_bridge_example"))
    
    return examples


def main():
    """Main function for command-line interface"""
    parser = argparse.ArgumentParser(description='Generate bridge general arrangement drawings')
    parser.add_argument('bridge_type', choices=[bt.value for bt in BridgeType],
                       help='Type of bridge to generate')
    parser.add_argument('--span', type=float, default=100.0,
                       help='Main span length in meters (default: 100.0)')
    parser.add_argument('--width', type=float, default=12.0,
                       help='Deck width in meters (default: 12.0)')
    parser.add_argument('--height', type=float, default=20.0,
                       help='Overall height in meters (default: 20.0)')
    parser.add_argument('--supports', type=int, default=0,
                       help='Number of intermediate supports (default: 0)')
    parser.add_argument('--load', type=float, default=50.0,
                       help='Design load in kN/m (default: 50.0)')
    parser.add_argument('--material', default='steel',
                       help='Primary material (default: steel)')
    parser.add_argument('--output', default='bridge_drawing',
                       help='Output filename (without extension)')
    parser.add_argument('--format', choices=[of.value for of in OutputFormat], 
                       default='png', help='Output format (default: png)')
    parser.add_argument('--examples', action='store_true',
                       help='Generate example bridges of all types')
    
    args = parser.parse_args()
    
    if args.examples:
        print("Generating example bridges...")
        examples = create_example_bridges()
        
        for bridge_type, params, filename in examples:
            generator = BridgeDrawingGenerator(bridge_type, params)
            generator.generate_drawing()
            generator.save_drawing(filename, OutputFormat.ALL)
            print(f"Generated {bridge_type.value} bridge example")
        
        print("All example bridges generated successfully!")
        return
    
    # Create bridge parameters from command line arguments
    try:
        params = BridgeParameters(
            span_length=args.span,
            deck_width=args.width,
            height=args.height,
            supports=args.supports,
            load_capacity=args.load,
            material=args.material
        )
        
        bridge_type = BridgeType(args.bridge_type)
        output_format = OutputFormat(args.format)
        
        print(f"Generating {bridge_type.value} bridge drawing...")
        print(f"Parameters: {params}")
        
        generator = BridgeDrawingGenerator(bridge_type, params)
        generator.generate_drawing()
        generator.save_drawing(args.output, output_format)
        
        print(f"Bridge drawing saved successfully!")
        
    except Exception as e:
        print(f"Error generating bridge drawing: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())king
Copy<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BridgeGAD Pro - Enhanced Bridge Design Generator</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .cad-grid {
            background-image: 
                linear-gradient(to right, #e5e7eb 1px, transparent 1px),
                linear-gradient(to bottom, #e5e7eb 1px, transparent 1px);
            background-size: 20px 20px;
        }
        .cad-paper {
            background-color: #fefefe;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        .technical-line {
            stroke: #1f2937;
            stroke-width: 2;
            fill: none;
        }
        .dimension-line {
            stroke: #ef4444;
            stroke-width: 1;
            fill: none;
        }
        .construction-line {
            stroke: #6b7280;
            stroke-width: 1;
            stroke-dasharray: 5,5;
            fill: none;
        }
        .bridge-slab {
            fill: #d1d5db;
            stroke: #374151;
            stroke-width: 2;
        }
        .bridge-pier {
            fill: #9ca3af;
            stroke: #1f2937;
            stroke-width: 2;
        }
        .approach-slab {
            fill: #e5e7eb;
            stroke: #374151;
            stroke-width: 1.5;
        }
        .wearing-course {
            fill: #374151;
            stroke: #111827;
            stroke-width: 1;
        }
        .water-line {
            stroke: #3b82f6;
            stroke-width: 3;
            fill: none;
        }
        .ground-line {
            stroke: #92400e;
            stroke-width: 2;
            fill: none;
        }
    </style>
</head>
<body class="bg-gray-50 font-sans">
    <!-- Header -->
    <header class="bg-gradient-to-r from-blue-900 to-blue-800 text-white py-6">
        <div class="container mx-auto px-6">
            <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4">
                    <i class="fas fa-bridge text-3xl"></i>
                    <div>
                        <h1 class="text-3xl font-bold">BridgeGAD Pro</h1>
                        <p class="text-blue-200">Enhanced Bridge Design Generator</p>
                    </div>
                </div>
                <div class="text-right">
                    <div class="bg-blue-800 px-4 py-2 rounded-lg">
                        <i class="fas fa-drafting-compass mr-2"></i>
                        <span class="font-semibold">Professional CAD Output</span>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <div class="container mx-auto px-6 py-8 space-y-8">
        
        <!-- Parameters Input Section -->
        <section class="bg-white rounded-xl shadow-lg p-6">
            <div class="flex items-center mb-6">
                <i class="fas fa-cogs text-2xl text-blue-600 mr-3"></i>
                <h2 class="text-2xl font-bold text-gray-800">Bridge Design Parameters</h2>
            </div>
            
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- Geometry Parameters -->
                <div class="bg-gray-50 rounded-lg p-4">
                    <h3 class="font-semibold text-gray-700 mb-4 flex items-center">
                        <i class="fas fa-ruler-combined mr-2"></i>
                        Geometry
                    </h3>
                    <div class="space-y-3">
                        <div>
                            <label class="block text-sm font-medium text-gray-600 mb-1">Number of Spans</label>
                            <input type="number" id="nspan" value="3" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-600 mb-1">Span Length (m)</label>
                            <input type="number" id="span1" value="30" step="0.1" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-600 mb-1">Skew Angle (°)</label>
                            <input type="number" id="skew" value="0" step="0.1" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-600 mb-1">Clear Carriageway (m)</label>
                            <input type="number" id="ccbr" value="7.5" step="0.1" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        </div>
                    </div>
                </div>

                <!-- Levels -->
                <div class="bg-gray-50 rounded-lg p-4">
                    <h3 class="font-semibold text-gray-700 mb-4 flex items-center">
                        <i class="fas fa-layer-group mr-2"></i>
                        Levels
                    </h3>
                    <div class="space-y-3">
                        <div>
                            <label class="block text-sm font-medium text-gray-600 mb-1">Road Top Level (m)</label>
                            <input type="number" id="rtl" value="105" step="0.001" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-600 mb-1">Soffit Level (m)</label>
                            <input type="number" id="sofl" value="103" step="0.001" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-600 mb-1">Founding Level (m)</label>
                            <input type="number" id="futrl" value="98" step="0.001" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-600 mb-1">Datum Level (m)</label>
                            <input type="number" id="datum" value="100" step="0.001" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        </div>
                    </div>
                </div>

                <!-- Structural Details -->
                <div class="bg-gray-50 rounded-lg p-4">
                    <h3 class="font-semibold text-gray-700 mb-4 flex items-center">
                        <i class="fas fa-building mr-2"></i>
                        Structure
                    </h3>
                    <div class="space-y-3">
                        <div>
                            <label class="block text-sm font-medium text-gray-600 mb-1">Slab Thickness Center (m)</label>
                            <input type="number" id="slbthc" value="0.4" step="0.01" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-600 mb-1">Pier Width (m)</label>
                            <input type="number" id="piertw" value="1.2" step="0.01" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-600 mb-1">Pier Batter</label>
                            <input type="number" id="battr" value="6" step="0.1" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-600 mb-1">Footing Width (m)</label>
                            <input type="number" id="futw" value="3.0" step="0.1" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        </div>
                    </div>
                </div>
            </div>

            <div class="mt-6 flex justify-center">
                <button id="generateBtn" class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-semibold transition duration-200 flex items-center">
                    <i class="fas fa-magic mr-2"></i>
                    Generate Bridge Design
                </button>
            </div>
        </section>

        <!-- Bridge Visualization Section -->
        <section class="bg-white rounded-xl shadow-lg p-6">
            <div class="flex items-center justify-between mb-6">
                <div class="flex items-center">
                    <i class="fas fa-eye text-2xl text-green-600 mr-3"></i>
                    <h2 class="text-2xl font-bold text-gray-800">Bridge Visualization</h2>
                </div>
                <div class="flex space-x-2">
                    <button class="view-btn active bg-green-600 text-white px-4 py-2 rounded-lg" data-view="elevation">Elevation</button>
                    <button class="view-btn bg-gray-200 text-gray-700 px-4 py-2 rounded-lg" data-view="plan">Plan</button>
                    <button class="view-btn bg-gray-200 text-gray-700 px-4 py-2 rounded-lg" data-view="section">Section</button>
                </div>
            </div>

            <!-- Drawing Canvas -->
            <div class="cad-paper cad-grid rounded-lg p-4" style="height: 600px; overflow: hidden;">
                <svg id="bridgeDrawing" width="100%" height="100%" class="border border-gray-300 rounded">
                    <!-- Grid and reference lines will be added here -->
                    <defs>
                        <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#e5e7eb" stroke-width="1"/>
                        </pattern>
                        <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                            <polygon points="0 0, 10 3.5, 0 7" fill="#ef4444"/>
                        </marker>
                    </defs>
                    <rect width="100%" height="100%" fill="url(#grid)"/>
                </svg>
            </div>
        </section>

        <!-- Technical Specifications -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            
            <!-- Cross-Section Analysis -->
            <section class="bg-white rounded-xl shadow-lg p-6">
                <div class="flex items-center mb-4">
                    <i class="fas fa-chart-line text-2xl text-purple-600 mr-3"></i>
                    <h2 class="text-xl font-bold text-gray-800">Cross-Section Analysis</h2>
                </div>
                <div class="bg-gray-50 rounded-lg p-4" style="height: 300px;">
                    <canvas id="crossSectionChart" style="height: 100%;"></canvas>
                </div>
            </section>

            <!-- Design Summary -->
            <section class="bg-white rounded-xl shadow-lg p-6">
                <div class="flex items-center mb-4">
                    <i class="fas fa-clipboard-list text-2xl text-orange-600 mr-3"></i>
                    <h2 class="text-xl font-bold text-gray-800">Design Summary</h2>
                </div>
                <div class="space-y-4">
                    <div class="grid grid-cols-2 gap-4">
                        <div class="bg-blue-50 p-3 rounded-lg">
                            <div class="text-sm text-gray-600">Total Length</div>
                            <div id="totalLength" class="text-xl font-bold text-blue-600">90.0 m</div>
                        </div>
                        <div class="bg-green-50 p-3 rounded-lg">
                            <div class="text-sm text-gray-600">Deck Area</div>
                            <div id="deckArea" class="text-xl font-bold text-green-600">675 m²</div>
                        </div>
                        <div class="bg-purple-50 p-3 rounded-lg">
                            <div class="text-sm text-gray-600">Max Height</div>
                            <div id="maxHeight" class="text-xl font-bold text-purple-600">7.0 m</div>
                        </div>
                        <div class="bg-orange-50 p-3 rounded-lg">
                            <div class="text-sm text-gray-600">Clearance</div>
                            <div id="clearance" class="text-xl font-bold text-orange-600">5.0 m</div>
                        </div>
                    </div>
                    
                    <div class="border-t pt-4">
                        <h3 class="font-semibold text-gray-700 mb-3">Material Quantities</h3>
                        <div class="space-y-2 text-sm">
                            <div class="flex justify-between">
                                <span>Concrete (m³):</span>
                                <span id="concreteVol" class="font-semibold">245.5</span>
                            </div>
                            <div class="flex justify-between">
                                <span>Reinforcement (kg):</span>
                                <span id="steelWeight" class="font-semibold">12,275</span>
                            </div>
                            <div class="flex justify-between">
                                <span>Formwork (m²):</span>
                                <span id="formworkArea" class="font-semibold">892</span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>

        <!-- Drawing Output Preview -->
        <section class="bg-white rounded-xl shadow-lg p-6">
            <div class="flex items-center justify-between mb-6">
                <div class="flex items-center">
                    <i class="fas fa-file-alt text-2xl text-red-600 mr-3"></i>
                    <h2 class="text-2xl font-bold text-gray-800">DXF Drawing Output</h2>
                </div>
                <div class="flex space-x-2">
                    <button class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg flex items-center">
                        <i class="fas fa-download mr-2"></i>
                        Download DXF
                    </button>
                    <button class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg flex items-center">
                        <i class="fas fa-print mr-2"></i>
                        Print
                    </button>
                </div>
            </div>

            <!-- Drawing Layers Control -->
            <div class="bg-gray-50 rounded-lg p-4 mb-4">
                <h3 class="font-semibold text-gray-700 mb-3">Drawing Layers</h3>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <label class="flex items-center">
                        <input type="checkbox" checked class="mr-2" data-layer="structure">
                        <span class="text-sm">Structure</span>
                    </label>
                    <label class="flex items-center">
                        <input type="checkbox" checked class="mr-2" data-layer="dimensions">
                        <span class="text-sm">Dimensions</span>
                    </label>
                    <label class="flex items-center">
                        <input type="checkbox" checked class="mr-2" data-layer="annotations">
                        <span class="text-sm">Annotations</span>
                    </label>
                    <label class="flex items-center">
                        <input type="checkbox" checked class="mr-2" data-layer="grid">
                        <span class="text-sm">Grid</span>
                    </label>
                </div>
            </div>

            <!-- Professional Drawing Output -->
            <div class="cad-paper rounded-lg border-2 border-gray-300 p-6" style="height: 800px; overflow: hidden;">
                <div class="h-full flex flex-col">
                    <!-- Title Block -->
                    <div class="border-2 border-gray-800 p-4 mb-4 bg-white">
                        <div class="grid grid-cols-3 gap-4">
                            <div>
                                <h3 class="font-bold text-lg">BRIDGE GENERAL ARRANGEMENT</h3>
                                <p class="text-sm text-gray-600">Scale: 1:500 @ A1</p>
                            </div>
                            <div class="text-center">
                                <p class="font-semibold">Drawing No: BRG-001</p>
                                <p class="text-sm">Rev: A</p>
                            </div>
                            <div class="text-right">
                                <p class="text-sm">Date: <span id="currentDate"></span></p>
                                <p class="text-sm">Checked: <span class="font-semibold">BridgeGAD Pro</span></p>
                            </div>
                        </div>
                    </div>

                    <!-- Main Drawing Area -->
                    <div class="flex-1 cad-grid">
                        <svg id="finalDrawing" width="100%" height="100%">
                            <!-- Professional bridge drawing will be rendered here -->
                        </svg>
                    </div>
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="bg-gray-800 text-white py-6 rounded-xl">
            <div class="text-center">
                <div class="flex items-center justify-center mb-2">
                    <i class="fas fa-bridge text-xl mr-2"></i>
                    <span class="font-semibold text-lg">BridgeGAD Pro</span>
                </div>
                <p class="text-gray-300">Professional Bridge Design Generator | Enhanced CAD Output</p>
                <p class="text-sm text-gray-400 mt-2">© 2024 - Advanced Engineering Solutions</p>
            </div>
        </footer>
    </div>

    <script>
        // Bridge Design Application
        class BridgeDesigner {
            constructor() {
                this.parameters = {};
                this.currentView = 'elevation';
                this.init();
            }

            init() {
                this.setupEventListeners();
                this.updateDate();
                this.generateDesign();
                this.initializeChart();
            }

            setupEventListeners() {
                // Generate button
                document.getElementById('generateBtn').addEventListener('click', () => {
                    this.generateDesign();
                });

                // View buttons
                document.querySelectorAll('.view-btn').forEach(btn => {
                    btn.addEventListener('click', (e) => {
                        document.querySelectorAll('.view-btn').forEach(b => {
                            b.classList.remove('active', 'bg-green-600', 'text-white');
                            b.classList.add('bg-gray-200', 'text-gray-700');
                        });
                        e.target.classList.add('active', 'bg-green-600', 'text-white');
                        e.target.classList.remove('bg-gray-200', 'text-gray-700');
                        this.currentView = e.target.dataset.view;
                        this.drawBridge();
                    });
                });

                // Parameter inputs
                document.querySelectorAll('input[type="number"]').forEach(input => {
                    input.addEventListener('change', () => {
                        this.updateParameters();
                        this.generateDesign();
                    });
                });
            }

            updateDate() {
                document.getElementById('currentDate').textContent = new Date().toLocaleDateString();
            }

            updateParameters() {
                this.parameters = {
                    nspan: parseFloat(document.getElementById('nspan').value) || 3,
                    span1: parseFloat(document.getElementById('span1').value) || 30,
                    skew: parseFloat(document.getElementById('skew').value) || 0,
                    ccbr: parseFloat(document.getElementById('ccbr').value) || 7.5,
                    rtl: parseFloat(document.getElementById('rtl').value) || 105,
                    sofl: parseFloat(document.getElementById('sofl').value) || 103,
                    futrl: parseFloat(document.getElementById('futrl').value) || 98,
                    datum: parseFloat(document.getElementById('datum').value) || 100,
                    slbthc: parseFloat(document.getElementById('slbthc').value) || 0.4,
                    piertw: parseFloat(document.getElementById('piertw').value) || 1.2,
                    battr: parseFloat(document.getElementById('battr').value) || 6,
                    futw: parseFloat(document.getElementById('futw').value) || 3.0
                };
            }

            generateDesign() {
                this.updateParameters();
                this.updateSummary();
                this.drawBridge();
                this.drawFinalOutput();
                this.updateChart();
            }

            updateSummary() {
                const totalLength = this.parameters.nspan * this.parameters.span1;
                const deckArea = totalLength * this.parameters.ccbr;
                const maxHeight = this.parameters.rtl - this.parameters.futrl;
                const clearance = this.parameters.sofl - this.parameters.futrl;

                document.getElementById('totalLength').textContent = `${totalLength.toFixed(1)} m`;
                document.getElementById('deckArea').textContent = `${deckArea.toFixed(0)} m²`;
                document.getElementById('maxHeight').textContent = `${maxHeight.toFixed(1)} m`;
                document.getElementById('clearance').textContent = `${clearance.toFixed(1)} m`;

                // Calculate material quantities (simplified)
                const concreteVol = (deckArea * this.parameters.slbthc * 1.2).toFixed(1);
                const steelWeight = (concreteVol * 50).toFixed(0);
                const formworkArea = (deckArea * 1.3).toFixed(0);

                document.getElementById('concreteVol').textContent = concreteVol;
                document.getElementById('steelWeight').textContent = steelWeight.toLocaleString();
                document.getElementById('formworkArea').textContent = formworkArea;
            }

            drawBridge() {
                const svg = document.getElementById('bridgeDrawing');
                svg.innerHTML = '';

                // Add grid
                const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                rect.setAttribute('width', '100%');
                rect.setAttribute('height', '100%');
                rect.setAttribute('fill', 'url(#grid)');
                svg.appendChild(rect);

                const viewBox = svg.getBoundingClientRect();
                const scale = Math.min(viewBox.width, viewBox.height) / 100;

                if (this.currentView === 'elevation') {
                    this.drawElevationView(svg, scale);
                } else if (this.currentView === 'plan') {
                    this.drawPlanView(svg, scale);
                } else if (this.currentView === 'section') {
                    this.drawSectionView(svg, scale);
                }
            }

            drawElevationView(svg, scale) {
                const centerY = 300;
                const startX = 100;
                const spanWidth = 150;

                // Draw deck slab
                for (let i = 0; i < this.parameters.nspan; i++) {
                    const x = startX + i * spanWidth;
                    this.createRect(svg, x, centerY - 20, spanWidth - 10, 40, 'bridge-slab');
                }

                // Draw piers
                for (let i = 1; i < this.parameters.nspan; i++) {
                    const x = startX + i * spanWidth - 5;
                    this.createRect(svg, x - 15, centerY + 20, 30, 80, 'bridge-pier');
                    this.createRect(svg, x - 25, centerY + 100, 50, 20, 'bridge-pier');
                }

                // Draw approach slabs
                this.createRect(svg, startX - 80, centerY - 15, 70, 30, 'approach-slab');
                this.createRect(svg, startX + this.parameters.nspan * spanWidth, centerY - 15, 70, 30, 'approach-slab');

                // Add dimensions
                this.addDimension(svg, startX, centerY - 60, startX + spanWidth - 10, centerY - 60, `${this.parameters.span1}m`);

                // Add labels
                this.addText(svg, startX + spanWidth/2, centerY - 80, 'DECK SLAB', 'middle');
                this.addText(svg, startX + spanWidth, centerY + 60, 'PIER', 'middle');
            }

            drawPlanView(svg, scale) {
                const centerX = 400;
                const centerY = 300;
                const bridgeWidth = this.parameters.ccbr * 10;

                // Draw bridge deck
                this.createRect(svg, centerX - bridgeWidth/2, centerY - 200, bridgeWidth, 400, 'bridge-slab');

                // Draw piers in plan
                for (let i = 1; i < this.parameters.nspan; i++) {
                    const y = centerY - 200 + (400 * i / this.parameters.nspan);
                    this.createRect(svg, centerX - 20, y - 10, 40, 20, 'bridge-pier');
                }

                // Add dimensions
                this.addDimension(svg, centerX - bridgeWidth/2 - 30, centerY - 200, centerX - bridgeWidth/2 - 30, centerY + 200, `${this.parameters.nspan * this.parameters.span1}m`);
                this.addDimension(svg, centerX - bridgeWidth/2, centerY + 230, centerX + bridgeWidth/2, centerY + 230, `${this.parameters.ccbr}m`);
            }

            drawSectionView(svg, scale) {
                const centerX = 400;
                const centerY = 300;
                const deckWidth = this.parameters.ccbr * 15;

                // Draw cross-section
                this.createRect(svg, centerX - deckWidth/2, centerY - 30, deckWidth, 60, 'bridge-slab');
                
                // Draw wearing course
                this.createRect(svg, centerX - deckWidth/2, centerY - 35, deckWidth, 10, 'wearing-course');

                // Draw piers (if in section)
                this.createRect(svg, centerX - 20, centerY + 30, 40, 100, 'bridge-pier');

                // Add section markers
                this.addText(svg, centerX, centerY - 80, 'TYPICAL CROSS SECTION', 'middle');
            }

            drawFinalOutput() {
                const svg = document.getElementById('finalDrawing');
                svg.innerHTML = '';

                // Professional elevation drawing
                const scale = 2;
                const startX = 50;
                const baseY = 400;
                const spanWidth = 200;

                // Draw detailed elevation
                for (let i = 0; i < this.parameters.nspan; i++) {
                    const x = startX + i * spanWidth;
                    
                    // Deck slab with proper thickness
                    this.createRect(svg, x, baseY - 40, spanWidth - 10, 40, 'bridge-slab');
                    
                    // Wearing course
                    this.createRect(svg, x, baseY - 45, spanWidth - 10, 5, 'wearing-course');
                }

                // Detailed piers
                for (let i = 1; i < this.parameters.nspan; i++) {
                    const x = startX + i * spanWidth - 5;
                    
                    // Pier shaft
                    const pierHeight = (this.parameters.rtl - this.parameters.futrl) * 20;
                    this.createRect(svg, x - 15, baseY, 30, pierHeight, 'bridge-pier');
                    
                    // Pier cap
                    this.createRect(svg, x - 25, baseY - 15, 50, 15, 'bridge-pier');
                    
                    // Footing
                    this.createRect(svg, x - 30, baseY + pierHeight, 60, 20, 'bridge-pier');
                }

                // Add professional dimensions
                const totalSpan = this.parameters.nspan * spanWidth;
                this.addDimension(svg, startX, baseY - 80, startX + totalSpan - 10, baseY - 80, `${(this.parameters.nspan * this.parameters.span1).toFixed(1)}m`);

                // Add level annotations
                this.addText(svg, 20, baseY - 40, `RL ${this.parameters.rtl.toFixed(2)}`, 'start');
                this.addText(svg, 20, baseY, `RL ${this.parameters.sofl.toFixed(2)}`, 'start');

                // Add construction lines
                const line1 = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                line1.setAttribute('x1', '30');
                line1.setAttribute('y1', baseY - 40);
                line1.setAttribute('x2', startX + totalSpan + 50);
                line1.setAttribute('y2', baseY - 40);
                line1.setAttribute('class', 'construction-line');
                svg.appendChild(line1);
            }

            createRect(svg, x, y, width, height, className) {
                const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                rect.setAttribute('x', x);
                rect.setAttribute('y', y);
                rect.setAttribute('width', width);
                rect.setAttribute('height', height);
                rect.setAttribute('class', className);
                svg.appendChild(rect);
                return rect;
            }

            addDimension(svg, x1, y1, x2, y2, text) {
                const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                line.setAttribute('x1', x1);
                line.setAttribute('y1', y1);
                line.setAttribute('x2', x2);
                line.setAttribute('y2', y2);
                line.setAttribute('class', 'dimension-line');
                line.setAttribute('marker-end', 'url(#arrowhead)');
                line.setAttribute('marker-start', 'url(#arrowhead)');
                svg.appendChild(line);

                const textEl = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                textEl.setAttribute('x', (x1 + x2) / 2);
                textEl.setAttribute('y', y1 - 5);
                textEl.setAttribute('text-anchor', 'middle');
                textEl.setAttribute('font-size', '12');
                textEl.setAttribute('fill', '#ef4444');
                textEl.textContent = text;
                svg.appendChild(textEl);
            }

            addText(svg, x, y, text, anchor = 'start') {
                const textEl = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                textEl.setAttribute('x', x);
                textEl.setAttribute('y', y);
                textEl.setAttribute('text-anchor', anchor);
                textEl.setAttribute('font-size', '14');
                textEl.setAttribute('fill', '#374151');
                textEl.setAttribute('font-weight', 'bold');
                textEl.textContent = text;
                svg.appendChild(textEl);
                return textEl;
            }

            initializeChart() {
                const ctx = document.getElementById('crossSectionChart').getContext('2d');
                
                // Sample cross-section data
                const chainages = Array.from({length: 20}, (_, i) => i * 5);
                const levels = chainages.map(ch => this.parameters.futrl + Math.sin(ch/10) * 2 + Math.random() * 0.5);

                this.chart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: chainages,
                        datasets: [{
                            label: 'Ground Level',
                            data: levels,
                            borderColor: '#92400e',
                            backgroundColor: 'rgba(146, 64, 14, 0.1)',
                            fill: true,
                            tension: 0.4
                        }, {
                            label: 'Soffit Level',
                            data: Array(20).fill(this.parameters.sofl),
                            borderColor: '#3b82f6',
                            borderDash: [5, 5],
                            fill: false
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'top'
                            }
                        },
                        scales: {
                            x: {
                                title: {
                                    display: true,
                                    text: 'Chainage (m)'
                                }
                            },
                            y: {
                                title: {
                                    display: true,
                                    text: 'Level (m)'
                                }
                            }
                        }
                    }
                });
            }

            updateChart() {
                if (this.chart) {
                    this.chart.data.datasets[1].data = Array(20).fill(this.parameters.sofl);
                    this.chart.update();
                }
            }
        }

        // Initialize the application
        document.addEventListener('DOMContentLoaded', () => {
            const app = new BridgeDesigner();
        });
    </script>
</body>
</html>