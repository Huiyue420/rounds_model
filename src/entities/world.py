"""
World/Level management
Handles game world, platforms, and environment
"""

import pygame
from typing import List, Tuple
from ..systems.physics_system import Vector2


class Platform:
    """Simple platform for collision"""
    
    def __init__(self, x: float, y: float, width: float, height: float):
        self.rect = pygame.Rect(int(x), int(y), int(width), int(height))
        self.color = (128, 128, 128)  # Gray platform
    
    def render(self, screen: pygame.Surface):
        """Render the platform"""
        pygame.draw.rect(screen, self.color, self.rect)


class GameWorld:
    """Game world containing platforms and boundaries"""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.platforms = []
        self.background_color = (45, 45, 55)  # Dark blue-gray
        
        self._create_default_level()
    
    def _create_default_level(self):
        """Create the default level layout"""
        # Ground platform
        ground = Platform(0, self.screen_height - 50, self.screen_width, 50)
        self.platforms.append(ground)
        
        # Some floating platforms
        platform1 = Platform(200, self.screen_height - 200, 150, 20)
        self.platforms.append(platform1)
        
        platform2 = Platform(500, self.screen_height - 350, 200, 20)
        self.platforms.append(platform2)
        
        platform3 = Platform(900, self.screen_height - 250, 120, 20)
        self.platforms.append(platform3)
        
        # Side walls
        left_wall = Platform(-10, 0, 10, self.screen_height)
        right_wall = Platform(self.screen_width, 0, 10, self.screen_height)
        self.platforms.append(left_wall)
        self.platforms.append(right_wall)
    
    def get_platforms(self) -> List[pygame.Rect]:
        """Get all platform rectangles for collision detection"""
        return [platform.rect for platform in self.platforms]
    
    def render(self, screen: pygame.Surface):
        """Render the world"""
        # Fill background
        screen.fill(self.background_color)
        
        # Draw platforms
        for platform in self.platforms:
            platform.render(screen)
    
    def add_platform(self, x: float, y: float, width: float, height: float):
        """Add a new platform"""
        platform = Platform(x, y, width, height)
        self.platforms.append(platform)
    
    def check_boundaries(self, player):
        """Check if player is within world boundaries"""
        # Check if player fell off the world
        if player.position.y > self.screen_height + 100:
            # Reset player to spawn position
            player.position.x = self.screen_width // 2
            player.position.y = 100
            player.velocity = Vector2(0, 0)
            player.take_damage(20)  # Fall damage
