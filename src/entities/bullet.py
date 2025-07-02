"""
Bullet Entity - Bullet class implementation
Handles bullet physics, movement, and rendering
"""

import pygame
import math
from typing import Tuple, Optional, Union
from ..systems.physics_system import Vector2


class Bullet:
    """Bullet entity with physics and collision"""
    
    def __init__(self, x: float, y: float, angle: float, speed: float, damage: float, 
                 bullet_size: Union[float, Tuple[float, float]] = 2.0, max_distance: float = 800.0):
        # Position and movement
        self.position = Vector2(x, y)
        self.velocity = Vector2(
            math.cos(angle) * speed,
            math.sin(angle) * speed
        )
        
        # Properties
        self.damage = damage
        self.size = bullet_size
        self.max_distance = max_distance
        self.distance_traveled = 0.0
        self.active = True
        
        # Calculate numerical size for rendering and collision
        if isinstance(bullet_size, (tuple, list)):
            self.render_size = min(bullet_size)  # Use smaller dimension for rendering
        else:
            self.render_size = bullet_size
        
        # Visual properties
        self.color = (255, 255, 100)  # Yellow bullet
        self.trail_positions = []  # For bullet trail effect
        self.max_trail_length = 5
        
        # Collision - handle both tuple and float bullet_size
        if isinstance(bullet_size, (tuple, list)):
            # If bullet_size is a tuple (width, height), use the smaller dimension for radius
            self.radius = min(bullet_size) / 2
        else:
            # If bullet_size is a float, use it directly
            self.radius = bullet_size / 2
        
    def update(self, dt: float):
        """Update bullet position and check if it should be destroyed"""
        if not self.active:
            return
        
        # Store previous position for trail
        self.trail_positions.append(Vector2(self.position.x, self.position.y))
        if len(self.trail_positions) > self.max_trail_length:
            self.trail_positions.pop(0)
        
        # Update position
        old_position = Vector2(self.position.x, self.position.y)
        self.position += self.velocity * dt
        
        # Calculate distance traveled
        distance_this_frame = (self.position - old_position).length()
        self.distance_traveled += distance_this_frame
        
        # Check if bullet has traveled too far
        if self.distance_traveled >= self.max_distance:
            self.active = False
    
    def check_collision_with_player(self, player) -> bool:
        """Check collision with a player"""
        if not self.active:
            return False
        
        # Simple circle-rectangle collision
        player_center_x = player.position.x
        player_center_y = player.position.y
        player_half_width = player.width / 2
        player_half_height = player.height / 2
        
        # Find closest point on rectangle to circle center
        closest_x = max(player_center_x - player_half_width, 
                       min(self.position.x, player_center_x + player_half_width))
        closest_y = max(player_center_y - player_half_height, 
                       min(self.position.y, player_center_y + player_half_height))
        
        # Calculate distance
        distance_x = self.position.x - closest_x
        distance_y = self.position.y - closest_y
        distance_squared = distance_x * distance_x + distance_y * distance_y
        
        return distance_squared <= (self.radius * self.radius)
    
    def check_collision_with_platforms(self, platforms: list) -> bool:
        """Check collision with platforms"""
        if not self.active:
            return False
        
        bullet_rect = pygame.Rect(
            self.position.x - self.radius,
            self.position.y - self.radius,
            self.render_size,
            self.render_size
        )
        
        for platform in platforms:
            if bullet_rect.colliderect(platform):
                self.active = False
                return True
        
        return False
    
    def render(self, screen: pygame.Surface):
        """Render the bullet and its trail"""
        if not self.active:
            return
        
        # Draw trail
        for i, trail_pos in enumerate(self.trail_positions):
            alpha = int(255 * (i + 1) / len(self.trail_positions))
            trail_color = (*self.color, alpha)
            trail_size = max(1, int(self.render_size * (i + 1) / len(self.trail_positions)))
            
            # Create a surface for alpha blending
            trail_surface = pygame.Surface((trail_size * 2, trail_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, trail_color, (trail_size, trail_size), trail_size)
            screen.blit(trail_surface, (trail_pos.x - trail_size, trail_pos.y - trail_size))
        
        # Draw main bullet
        pygame.draw.circle(screen, self.color, 
                         (int(self.position.x), int(self.position.y)), 
                         int(self.radius))
    
    def destroy(self):
        """Mark bullet as inactive"""
        self.active = False


class BulletManager:
    """Manages all bullets in the game"""
    
    def __init__(self):
        self.bullets = []
    
    def add_bullet(self, bullet: Bullet):
        """Add a new bullet"""
        self.bullets.append(bullet)
    
    def update(self, dt: float, platforms: list, players: list):
        """Update all bullets and check collisions"""
        for bullet in self.bullets[:]:  # Copy list to safely modify during iteration
            if not bullet.active:
                self.bullets.remove(bullet)
                continue
            
            # Update bullet
            bullet.update(dt)
            
            # Check platform collisions
            bullet.check_collision_with_platforms(platforms)
            
            # Check player collisions
            for player in players:
                if bullet.check_collision_with_player(player):
                    player.take_damage(bullet.damage)
                    bullet.destroy()
                    break
    
    def render(self, screen: pygame.Surface):
        """Render all bullets"""
        for bullet in self.bullets:
            bullet.render(screen)
    
    def clear(self):
        """Clear all bullets"""
        self.bullets.clear()
    
    def get_bullet_count(self) -> int:
        """Get number of active bullets"""
        return len([b for b in self.bullets if b.active])
