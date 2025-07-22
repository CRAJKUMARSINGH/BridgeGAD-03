class ApproachSlabDesign:
    def __init__(self, length, width, thickness, reinforcement_details=None):
        self.length = length
        self.width = width  
        self.thickness = thickness
        self.reinforcement_details = reinforcement_details or {}
        
    def calculate_approach_slab_loads(self):
        """Calculate loads on approach slab"""
        # Dead load calculation (concrete self-weight)
        concrete_density = 25  # kN/m³
        dead_load = self.thickness * concrete_density
        
        # Live load (IRC Class A loading)
        live_load = 5.0  # kN/m²
        
        # Total load
        total_load = dead_load + live_load
        
        return {
            'dead_load': dead_load,
            'live_load': live_load,
            'total_load': total_load
        }
    
    def design_reinforcement(self):
        """Design reinforcement for approach slab"""
        loads = self.calculate_approach_slab_loads()
        
        # Moment calculation (simplified)
        moment = (loads['total_load'] * self.length**2) / 8  # kNm/m
        
        # Steel area calculation (simplified)
        fy = 415  # N/mm²
        d = self.thickness * 1000 - 40  # Effective depth (mm)
        
        # Simplified steel area calculation
        ast_required = (moment * 1e6) / (0.87 * fy * 0.95 * d)  # mm²/m
        
        # Standard bar sizes and spacing
        bar_diameter = 12  # mm
        bar_area = 113.1  # mm² for 12mm bar
        
        # Calculate required spacing
        required_area_per_meter = ast_required  # mm²/m
        spacing = (bar_area / required_area_per_meter) * 1000  # mm c/c
        
        # Round to nearest standard spacing (50mm increments)
        spacing = min(round(spacing / 50) * 50, 300)  # Max spacing = 300mm
        
        return {
            'moment': moment,
            'ast_required': ast_required,
            'bar_diameter': bar_diameter,
            'spacing': int(spacing),
            'effective_depth': d
        }
    
    def generate_design_report(self):
        """Generate a design report for the approach slab"""
        loads = self.calculate_approach_slab_loads()
        reinforcement = self.design_reinforcement()
        
        report = {
            'design_parameters': {
                'length': f"{self.length:.2f} m",
                'width': f"{self.width:.2f} m",
                'thickness': f"{self.thickness:.3f} m"
            },
            'loads': {
                'dead_load': f"{loads['dead_load']:.2f} kN/m²",
                'live_load': f"{loads['live_load']:.2f} kN/m²",
                'total_load': f"{loads['total_load']:.2f} kN/m²"
            },
            'design_moments': {
                'bending_moment': f"{reinforcement['moment']:.2f} kNm/m"
            },
            'reinforcement': {
                'required_steel_area': f"{reinforcement['ast_required']:.2f} mm²/m",
                'provided_reinforcement': f"{reinforcement['bar_diameter']}mm @ {reinforcement['spacing']}mm c/c",
                'effective_depth': f"{reinforcement['effective_depth']:.1f} mm"
            }
        }
        
        return report
