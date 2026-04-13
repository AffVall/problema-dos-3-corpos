import math
import os
from random import randint, uniform
from typing import List, Tuple, Dict
import numpy as np
from config import Config

'''
G= 6.67430e-11  NM^2/kg^2
Mterra= 5.97e24 kg
100
83
Gatual= 3.9845571e14
'''


class Body:
    GRAVITATIONAL_CONSTANT = 6.67430e-11  
    def __init__(self, mass, velocity, position, max_velocity=0.1, size=1.0, name=None):
        self.size = float(size) 
        self.name = name
        self.mass = float(mass)
        self.max_velocity = float(max_velocity)
        
        if isinstance(velocity, dict):
            self.velocity = {
                'x': float(velocity.get('x', 0)),
                'y': float(velocity.get('y', 0)),
            }
        else:
            self.velocity = {'x': 0.0, 'y': 0.0}
        
        self.position = {
            'x': float(position['x']),
            'y': float(position['y']),
        }
        
        self.acceleration = {'x': 0.0, 'y': 0.0}
        self.calculate_body_size()
        self.__str__()
    
    def gravitational_field(self, point):
        """
        Calculate gravitational field (acceleration) at a given point.
        
        Args:
            point: Position dict {'x': px, 'y': py}
            
        Returns:
            tuple: (gx, gy) gravitational field components
        """
        dx = point['x'] - self.position['x']
        dy = point['y'] - self.position['y']
        dist_sq = dx*dx + dy*dy

        if dist_sq == 0:
            return (0, 0)
        
        dist = math.sqrt(dist_sq)
        field_mag = self.GRAVITATIONAL_CONSTANT * self.mass / dist_sq
        
        return (-field_mag * dx / dist, -field_mag * dy / dist)
    
    def calculate_resultant_force(self, bodies_list):
        """
        Calculate total gravitational force from all bodies.
        
        Args:
            bodies_list: List of Body objects (excluding this body)
            
        Returns:
            tuple: (fx, fy) total force components
        """
        fx, fy = 0.0, 0.0
        
        for body in bodies_list:
            field = body.gravitational_field(self.position)
            fx += field[0] * self.mass
            fy += field[1] * self.mass
        
        return (fx, fy)
    
    def update_acceleration(self, force):
        """Update acceleration from force (a = F/m)."""
        if self.mass != 0:
            self.acceleration['x'] = min(force[0] / self.mass, self.max_velocity)
            self.acceleration['y'] = min(force[1] / self.mass, self.max_velocity)
    
    def update_velocity(self, time_step=1.0):
        """Update velocity from acceleration (v = v0 + at)."""
        self.velocity['x'] += self.acceleration['x'] * time_step
        self.velocity['y'] += self.acceleration['y'] * time_step
    
    def update_position(self, time_step=1.0):
        """Update position from velocity (x = x0 + vt)."""
        self.position['x'] += self.velocity['x'] * time_step
        self.position['y'] += self.velocity['y'] * time_step
    
    def get_distance_from(self, other_body):
        """Calculate Euclidean distance to another body."""
        dx = self.position['x'] - other_body.position['x']
        dy = self.position['y'] - other_body.position['y']
        return math.sqrt(dx*dx + dy*dy)
    
    def __str__(self):
        """String representation of body state."""
        return (f"Body: {self.name}\n"
                f"  Mass: {self.mass:.2f} kg\n"
                f"  Position: x={self.position['x']:.2f}, y={self.position['y']:.2f}\n"
                f"  Velocity: x={self.velocity['x']:.2e}, y={self.velocity['y']:.2e}\n"
                f"  Acceleration: x={self.acceleration['x']:.2e}, y={self.acceleration['y']:.2e}")

    def calculate_body_size(self, config: Config) -> float:
        if config['calculate_sizes']:
            scale = config.get('size_scale_factor', 100)
            size = np.sqrt(self.mass) * scale
            return max(5.0, min(100.0, size))
        return 25.0

    def initialize_bodies(self, bodies: List, COLORS: List[str]) -> None:
        
        for body, color in zip(bodies, COLORS):
            name = body['name']
            mass = body['mass']
            size = body.calculate_body_size(body)
            pos_x = body['pos_x']
            pos_y = body['pos_y']
            vel_x = body['vel_x']
            vel_y = body['vel_y']
