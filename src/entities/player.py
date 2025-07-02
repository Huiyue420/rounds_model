"""
Player Entity - Player class implementation
Handles player movement, physics, and interactions
"""

import pygame
import math
from typing import Tuple, Dict, Any
from ..systems.physics_system import Vector2
from ..core.config import GameConfig


class Player:
    """Player entity with physics and movement"""
    
    def __init__(self, x: float, y: float, config: GameConfig, player_id: int = 0):
        self.player_id = player_id
        self.health = config.player_max_health
        self.max_health = config.player_max_health
        self.alive = True
        
        # Card effect modifiers
        self.damage_reduction = 0.0
        self.healing_rate = 0.0
        self.speed_multiplier = 1.0
        self.jump_force_multiplier = 1.0
        self.max_jumps = 1
        self.current_jumps = 0
        
        # Physics properties
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        
        # Player properties
        self.width = config.player_size
        self.height = config.player_size
        self.mass = 1.0
        self.on_ground = False
        
        # Movement properties
        self.move_speed = config.player_speed
        self.jump_force = config.player_jump_force
        self.friction = 0.8
        self.air_resistance = 0.98
        
        # Input state
        self.keys_pressed = {
            'left': False,
            'right': False,
            'jump': False
        }
        
        # Visual properties
        self.color = (100, 150, 255)  # Blue player
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def update(self, dt: float, gravity: float = 980.0):
        """Update player physics and position"""
        # Don't update if player is dead
        if not self.alive:
            return
            
        # Reset acceleration each frame
        self.acceleration = Vector2(0, 0)
        
        # Apply gravity
        if not self.on_ground:
            self.acceleration.y = gravity  # Set gravity, don't accumulate
        
        # Handle horizontal movement
        if self.keys_pressed['left']:
            target_velocity = -self.move_speed * self.speed_multiplier
            self.velocity.x = self._lerp(self.velocity.x, target_velocity, 10 * dt)
        elif self.keys_pressed['right']:
            target_velocity = self.move_speed * self.speed_multiplier
            self.velocity.x = self._lerp(self.velocity.x, target_velocity, 10 * dt)
        else:
            # Apply friction
            friction_factor = self.friction if self.on_ground else self.air_resistance
            self.velocity.x *= friction_factor
        
        # Handle jumping
        if self.keys_pressed['jump'] and (self.on_ground or self.current_jumps < self.max_jumps):
            if self.on_ground:
                self.current_jumps = 0
            if self.current_jumps < self.max_jumps:
                self.velocity.y = -self.jump_force * self.jump_force_multiplier
                self.current_jumps += 1
                self.on_ground = False
                self.keys_pressed['jump'] = False  # Prevent continuous jumping
        
        # Apply acceleration to velocity
        self.velocity += self.acceleration * dt
        
        # Apply velocity to position
        self.position += self.velocity * dt
        
        # Update rect for collision detection
        self.rect.x = int(self.position.x - self.width // 2)
        self.rect.y = int(self.position.y - self.height // 2)
        
        # Apply healing (only if alive)
        if self.healing_rate > 0 and self.alive:
            self.heal(self.healing_rate * dt)
    
    def handle_input(self, keys_pressed: Dict[int, bool], key_events: list):
        """Handle player input"""
        # Don't handle input if player is dead
        if not self.alive:
            return
            
        # Continuous movement keys
        self.keys_pressed['left'] = keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]
        self.keys_pressed['right'] = keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]
        
        # Jump key (only on key down event)
        for event in key_events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.keys_pressed['jump'] = True
    
    def check_ground_collision(self, platforms: list):
        """Check collision with platforms and ground"""
        self.on_ground = False
        
        # Check collision with each platform
        for platform in platforms:
            if self.rect.colliderect(platform):
                # If falling down and hitting platform from above
                if self.velocity.y > 0 and self.rect.bottom <= platform.top + 10:
                    self.position.y = platform.top - self.height // 2
                    self.velocity.y = 0
                    self.on_ground = True
                    self.current_jumps = 0
                # If moving right and hitting platform from left
                elif self.velocity.x > 0 and self.rect.right <= platform.left + 10:
                    self.position.x = platform.left - self.width // 2
                    self.velocity.x = 0
                # If moving left and hitting platform from right
                elif self.velocity.x < 0 and self.rect.left >= platform.right - 10:
                    self.position.x = platform.right + self.width // 2
                    self.velocity.x = 0
                # If jumping up and hitting platform from below
                elif self.velocity.y < 0 and self.rect.top >= platform.bottom - 10:
                    self.position.y = platform.bottom + self.height // 2
                    self.velocity.y = 0
    
    def take_damage(self, damage: float):
        """Apply damage to player"""
        actual_damage = damage * (1.0 - self.damage_reduction)
        self.health -= actual_damage
        if self.health <= 0:
            self.health = 0
            self.alive = False
    
    def heal(self, amount: float):
        """Heal the player"""
        self.health = min(self.max_health, self.health + amount)
    
    def render(self, screen: pygame.Surface):
        """Render the player"""
        # Draw player body
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw health bar above player
        health_bar_width = 40
        health_bar_height = 6
        health_bar_x = self.rect.centerx - health_bar_width // 2
        health_bar_y = self.rect.top - 15
        
        # Background (red)
        health_bg_rect = pygame.Rect(health_bar_x, health_bar_y, health_bar_width, health_bar_height)
        pygame.draw.rect(screen, (200, 50, 50), health_bg_rect)
        
        # Health bar (green)
        health_percentage = self.health / self.max_health
        health_width = int(health_bar_width * health_percentage)
        if health_width > 0:
            health_rect = pygame.Rect(health_bar_x, health_bar_y, health_width, health_bar_height)
            pygame.draw.rect(screen, (50, 200, 50), health_rect)
    
    def get_center_position(self) -> Tuple[float, float]:
        """Get player center position"""
        return (self.position.x, self.position.y)
    
    def _lerp(self, start: float, end: float, factor: float) -> float:
        """Linear interpolation"""
        return start + (end - start) * factor
