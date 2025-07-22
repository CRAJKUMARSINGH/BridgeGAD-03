import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

class AbutmentDesign:
    def __init__(self, bridge_width, bridge_height, abutment_height, approach_slab_length):
        self.bridge_width = bridge_width
        self.bridge_height = bridge_height
        self.abutment_height = abutment_height
        self.approach_slab_length = approach_slab_length
        
    def draw_sectional_elevation(self, ax=None):
        """Draw sectional elevation with abutments and approach slabs"""
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=(15, 8))
            return_fig = True
        else:
            return_fig = False
        
        # Bridge deck
        bridge_deck = Rectangle((2, 3), self.bridge_width, 0.5, 
                              facecolor='lightgray', edgecolor='black', linewidth=2)
        ax.add_patch(bridge_deck)
        
        # Left abutment
        left_abutment = Rectangle((1.5, 1), 0.5, self.abutment_height, 
                                facecolor='darkgray', edgecolor='black', linewidth=2)
        ax.add_patch(left_abutment)
        
        # Right abutment
        right_abutment = Rectangle((self.bridge_width + 2, 1), 0.5, self.abutment_height, 
                                 facecolor='darkgray', edgecolor='black', linewidth=2)
        ax.add_patch(right_abutment)
        
        # Left approach slab
        left_approach = Rectangle((1.5 - self.approach_slab_length, 3), 
                                self.approach_slab_length, 0.3, 
                                facecolor='lightblue', edgecolor='black', linewidth=1)
        ax.add_patch(left_approach)
        
        # Right approach slab
        right_approach = Rectangle((self.bridge_width + 2.5, 3), 
                                 self.approach_slab_length, 0.3, 
                                 facecolor='lightblue', edgecolor='black', linewidth=1)
        ax.add_patch(right_approach)
        
        # Ground level
        ground = Rectangle((0, 0), 12, 1, facecolor='brown', alpha=0.3)
        ax.add_patch(ground)
        
        # Dimensions and labels
        ax.text(2 + self.bridge_width/2, 3.7, 'Bridge Deck', fontsize=12, ha='center', fontweight='bold')
        ax.text(1.75, 1 + self.abutment_height/2, 'Left\nAbutment', fontsize=10, ha='center', va='center')
        ax.text(self.bridge_width + 2.25, 1 + self.abutment_height/2, 'Right\nAbutment', fontsize=10, ha='center', va='center')
        ax.text(1.5 - self.approach_slab_length/2, 3.4, 'Approach Slab', fontsize=10, ha='center')
        ax.text(self.bridge_width + 2.5 + self.approach_slab_length/2, 3.4, 'Approach Slab', fontsize=10, ha='center')
        
        # Set axis properties
        ax.set_xlim(-0.5, self.bridge_width + 4.5)
        ax.set_ylim(-0.5, 5)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('Length (m)')
        ax.set_ylabel('Height (m)')
        ax.set_title('Bridge Sectional Elevation with Abutments and Approach Slabs')
        
        if return_fig:
            return fig, ax
        return ax
