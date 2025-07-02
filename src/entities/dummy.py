"""
Test Dummy Entity - A simple target for testing weapon damage and card selection
Provides a static or moving target that can take damage and trigger card selection on death
"""

import pygame
import random
from typing import Tuple, Dict, Any, Optional
from ..systems.physics_system import Vector2
from ..core.config import GameConfig


class TestDummy:
    """Test dummy entity for weapon testing"""
    
    def __init__(self, x: float, y: float, config: GameConfig, dummy_id: int = 0):
        self.dummy_id = dummy_id
        self.max_health = 100
        self.health = self.max_health
        self.alive = True
        
        # Physics properties
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        
        # Visual properties
        self.width = 40
        self.height = 60
        self.color = (150, 75, 0)  # Brown color
        self.damaged_color = (255, 100, 100)  # Red when damaged
        self.dead_color = (100, 100, 100)  # Gray when dead
        
        # Damage effect
        self.damage_flash_timer = 0.0
        self.damage_flash_duration = 0.3
        
        # Movement (optional - for moving dummy)
        self.is_moving = False
        self.move_speed = 30.0
        self.move_direction = 1
        self.move_range = 100.0
        self.start_x = x
        
        # Respawn system
        self.respawn_timer = 0.0
        self.respawn_delay = 3.0  # 3 seconds to respawn
        self.should_respawn = True
        
    def set_moving(self, moving: bool = True, speed: float = 30.0, move_range: float = 100.0):
        """Set dummy to move back and forth"""
        self.is_moving = moving
        self.move_speed = speed
        self.move_range = move_range
        
    def update(self, dt: float):
        """Update dummy state"""
        # Update damage flash
        if self.damage_flash_timer > 0:
            self.damage_flash_timer -= dt
        
        # Handle respawn
        if not self.alive and self.should_respawn:
            self.respawn_timer += dt
            if self.respawn_timer >= self.respawn_delay:
                self.respawn()
        
        # Handle movement (if enabled and alive)
        if self.alive and self.is_moving:
            self._update_movement(dt)
    
    def _update_movement(self, dt: float):
        """Update dummy movement"""
        # Move back and forth
        self.position.x += self.move_direction * self.move_speed * dt
        
        # Check boundaries and reverse direction
        distance_from_start = abs(self.position.x - self.start_x)
        if distance_from_start >= self.move_range:
            self.move_direction *= -1
            # Clamp position to boundary
            if self.position.x > self.start_x:
                self.position.x = self.start_x + self.move_range
            else:
                self.position.x = self.start_x - self.move_range
    
    def take_damage(self, damage: int, damage_source: str = "unknown") -> bool:
        """Apply damage to dummy"""
        if not self.alive:
            return False
        
        self.health -= damage
        self.damage_flash_timer = self.damage_flash_duration
        
        print(f"Dummy {self.dummy_id} took {damage} damage from {damage_source}. Health: {self.health}/{self.max_health}")
        
        # Check if dummy is killed
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.respawn_timer = 0.0
            print(f"Dummy {self.dummy_id} has been killed!")
            return True  # Indicates dummy was killed
        
        return False
    
    def heal(self, heal_amount: int):
        """Heal the dummy"""
        if not self.alive:
            return
        
        old_health = self.health
        self.health = min(self.max_health, self.health + heal_amount)
        healed = self.health - old_health
        
        if healed > 0:
            print(f"Dummy {self.dummy_id} healed for {healed}. Health: {self.health}/{self.max_health}")
    
    def respawn(self):
        """Respawn the dummy"""
        self.health = self.max_health
        self.alive = True
        self.damage_flash_timer = 0.0
        self.respawn_timer = 0.0
        print(f"Dummy {self.dummy_id} has respawned!")
    
    def get_rect(self) -> pygame.Rect:
        """Get collision rectangle"""
        return pygame.Rect(
            self.position.x - self.width // 2,
            self.position.y - self.height // 2,
            self.width,
            self.height
        )
    
    def get_center(self) -> Tuple[float, float]:
        """Get center position"""
        return (self.position.x, self.position.y)
    
    def render(self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)):
        """Render the dummy"""
        # Calculate screen position
        screen_x = self.position.x - camera_offset[0] - self.width // 2
        screen_y = self.position.y - camera_offset[1] - self.height // 2
        
        # Choose color based on state
        if not self.alive:
            color = self.dead_color
        elif self.damage_flash_timer > 0:
            color = self.damaged_color
        else:
            color = self.color
        
        # Draw main body
        dummy_rect = pygame.Rect(screen_x, screen_y, self.width, self.height)
        pygame.draw.rect(screen, color, dummy_rect)
        pygame.draw.rect(screen, (0, 0, 0), dummy_rect, 2)  # Black outline
        
        # Draw face (if alive)
        if self.alive:
            # Eyes
            eye_size = 4
            left_eye_x = screen_x + 10
            right_eye_x = screen_x + 26
            eye_y = screen_y + 15
            
            pygame.draw.circle(screen, (0, 0, 0), (left_eye_x, eye_y), eye_size)
            pygame.draw.circle(screen, (0, 0, 0), (right_eye_x, eye_y), eye_size)
            
            # Mouth
            mouth_x = screen_x + 20
            mouth_y = screen_y + 30
            mouth_width = 8
            mouth_height = 4
            
            pygame.draw.ellipse(screen, (0, 0, 0), 
                               (mouth_x - mouth_width//2, mouth_y - mouth_height//2, 
                                mouth_width, mouth_height))
        
        # Draw health bar
        self._render_health_bar(screen, screen_x, screen_y - 15)
        
        # Draw respawn timer if dead
        if not self.alive and self.should_respawn:
            self._render_respawn_timer(screen, screen_x, screen_y - 30)
    
    def _render_health_bar(self, screen: pygame.Surface, x: float, y: float):
        """Render health bar above dummy"""
        bar_width = self.width
        bar_height = 8
        
        # Background
        bg_rect = pygame.Rect(x, y, bar_width, bar_height)
        pygame.draw.rect(screen, (100, 100, 100), bg_rect)
        
        # Health bar
        health_ratio = self.health / self.max_health if self.alive else 0
        health_width = int(bar_width * health_ratio)
        
        if health_width > 0:
            # Color based on health percentage
            if health_ratio > 0.6:
                health_color = (0, 255, 0)  # Green
            elif health_ratio > 0.3:
                health_color = (255, 255, 0)  # Yellow
            else:
                health_color = (255, 0, 0)  # Red
            
            health_rect = pygame.Rect(x, y, health_width, bar_height)
            pygame.draw.rect(screen, health_color, health_rect)
        
        # Border
        pygame.draw.rect(screen, (0, 0, 0), bg_rect, 1)
        
        # Health text
        font = pygame.font.Font(None, 16)
        health_text = f"{self.health}/{self.max_health}"
        text_surface = font.render(health_text, True, (255, 255, 255))
        text_x = x + (bar_width - text_surface.get_width()) // 2
        text_y = y - 18
        screen.blit(text_surface, (text_x, text_y))
    
    def _render_respawn_timer(self, screen: pygame.Surface, x: float, y: float):
        """Render respawn countdown"""
        if self.alive:
            return
        
        remaining_time = max(0, self.respawn_delay - self.respawn_timer)
        countdown_text = f"Respawn in: {remaining_time:.1f}s"
        
        font = pygame.font.Font(None, 20)
        text_surface = font.render(countdown_text, True, (255, 255, 0))
        text_x = x + (self.width - text_surface.get_width()) // 2
        screen.blit(text_surface, (text_x, y))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert dummy to dictionary for serialization"""
        return {
            'dummy_id': self.dummy_id,
            'position': {'x': self.position.x, 'y': self.position.y},
            'health': self.health,
            'max_health': self.max_health,
            'alive': self.alive,
            'is_moving': self.is_moving,
            'move_speed': self.move_speed
        }


class DummyManager:
    """Manages multiple test dummies"""
    
    def __init__(self, config: GameConfig):
        self.config = config
        self.dummies = []
        self.next_dummy_id = 0
    
    def add_dummy(self, x: float, y: float, moving: bool = False, 
                  move_speed: float = 30.0, move_range: float = 100.0) -> TestDummy:
        """Add a new dummy at specified position"""
        dummy = TestDummy(x, y, self.config, self.next_dummy_id)
        self.next_dummy_id += 1
        
        if moving:
            dummy.set_moving(True, move_speed, move_range)
        
        self.dummies.append(dummy)
        print(f"Added dummy {dummy.dummy_id} at position ({x}, {y})")
        return dummy
    
    def remove_dummy(self, dummy_id: int) -> bool:
        """Remove dummy by ID"""
        for i, dummy in enumerate(self.dummies):
            if dummy.dummy_id == dummy_id:
                self.dummies.pop(i)
                print(f"Removed dummy {dummy_id}")
                return True
        return False
    
    def get_dummy_at_position(self, x: float, y: float, radius: float = 50.0) -> Optional[TestDummy]:
        """Get dummy near specified position"""
        for dummy in self.dummies:
            distance = ((dummy.position.x - x) ** 2 + (dummy.position.y - y) ** 2) ** 0.5
            if distance <= radius:
                return dummy
        return None
    
    def update(self, dt: float):
        """Update all dummies"""
        for dummy in self.dummies:
            dummy.update(dt)
    
    def render(self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)):
        """Render all dummies"""
        for dummy in self.dummies:
            dummy.render(screen, camera_offset)
    
    def handle_bullet_collision(self, bullet_rect: pygame.Rect, damage: int, 
                               damage_source: str = "bullet") -> Optional[TestDummy]:
        """Check bullet collision with dummies and apply damage"""
        for dummy in self.dummies:
            if dummy.alive and dummy.get_rect().colliderect(bullet_rect):
                was_killed = dummy.take_damage(damage, damage_source)
                return dummy if was_killed else None
        return None
    
    def get_alive_dummies(self):
        """Get list of alive dummies"""
        return [dummy for dummy in self.dummies if dummy.alive]
    
    def get_all_dummies(self):
        """Get all dummies"""
        return self.dummies
    
    def clear_all(self):
        """Remove all dummies"""
        self.dummies.clear()
        self.next_dummy_id = 0
        print("Cleared all dummies")
