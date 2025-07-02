"""
Game UI System - Optimized Version with English Text
Handles in-game user interface display, including health bars, ammo display, weapon info, etc.
"""

try:
    import pygame
except ImportError:
    pygame = None

from typing import Dict, List, Optional, Tuple, Any
import logging

from ..core.config import GameConfig
from ..core.event_manager import EventManager, EventType


class UIElement:
    """Base UI element class"""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
        self.enabled = True
    
    def render(self, screen, font) -> None:
        """Render UI element"""
        pass
    
    def update(self, dt: float) -> None:
        """Update UI element"""
        pass


class HealthBar(UIElement):
    """Health bar UI element"""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.current_health = 100
        self.max_health = 100
        self.background_color = (100, 100, 100)
        self.health_color = (100, 200, 100)
        self.low_health_color = (200, 100, 100)
        self.border_color = (255, 255, 255)
        self.low_health_threshold = 0.3
    
    def set_health(self, current: int, maximum: int) -> None:
        """Set health values"""
        self.current_health = max(0, current)
        self.max_health = max(1, maximum)
    
    def render(self, screen, font) -> None:
        """Render health bar"""
        if not self.visible or not pygame:
            return
        
        # Background
        bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.background_color, bg_rect)
        
        # Health bar
        health_ratio = self.current_health / self.max_health
        health_width = int(self.width * health_ratio)
        
        if health_width > 0:
            # Choose color based on health
            color = self.low_health_color if health_ratio < self.low_health_threshold else self.health_color
            health_rect = pygame.Rect(self.x, self.y, health_width, self.height)
            pygame.draw.rect(screen, color, health_rect)
        
        # Border
        pygame.draw.rect(screen, self.border_color, bg_rect, 2)
        
        # Health text
        health_text = f"{self.current_health}/{self.max_health}"
        text_surface = font.render(health_text, True, (255, 255, 255))
        text_x = self.x + (self.width - text_surface.get_width()) // 2
        text_y = self.y + (self.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))


class AmmoDisplay(UIElement):
    """Ammo display UI element"""
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 120, 30)
        self.current_ammo = 0
        self.max_ammo = 0
        self.is_reloading = False
        self.reload_progress = 0.0
        self.text_color = (255, 255, 255)
        self.reload_color = (255, 255, 0)
    
    def set_ammo(self, current: int, maximum: int, reloading: bool = False, reload_progress: float = 0.0) -> None:
        """Set ammo information"""
        self.current_ammo = current
        self.max_ammo = maximum
        self.is_reloading = reloading
        self.reload_progress = reload_progress
    
    def render(self, screen, font) -> None:
        """Render ammo display"""
        if not self.visible or not pygame:
            return
        
        if self.is_reloading:
            # Show reload progress
            progress_text = f"Reloading... {int(self.reload_progress * 100)}%"
            text_surface = font.render(progress_text, True, self.reload_color)
        else:
            # Show ammo count
            ammo_text = f"Ammo: {self.current_ammo}/{self.max_ammo}"
            text_surface = font.render(ammo_text, True, self.text_color)
        
        screen.blit(text_surface, (self.x, self.y))


class WeaponDisplay(UIElement):
    """Weapon display UI element"""
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 120, 30)
        self.weapon_name = "Unknown"
        self.text_color = (255, 255, 255)
    
    def set_weapon(self, weapon_name: str) -> None:
        """Set weapon name"""
        self.weapon_name = weapon_name
    
    def render(self, screen, font) -> None:
        """Render weapon display"""
        if not self.visible or not pygame:
            return
        
        weapon_text = f"Weapon: {self.weapon_name}"
        text_surface = font.render(weapon_text, True, self.text_color)
        screen.blit(text_surface, (self.x, self.y))


class FPSCounter(UIElement):
    """FPS counter UI element"""
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 80, 20)
        self.fps = 0
        self.text_color = (255, 255, 255)
    
    def set_fps(self, fps: float) -> None:
        """Set FPS value"""
        self.fps = fps
    
    def render(self, screen, font) -> None:
        """Render FPS display"""
        if not self.visible or not pygame:
            return
        
        text = f"FPS: {self.fps:.1f}"
        text_surface = font.render(text, True, self.text_color)
        screen.blit(text_surface, (self.x, self.y))


class GameUI:
    """Game UI Manager"""
    
    def __init__(self, config: GameConfig, event_manager: EventManager):
        self.config = config
        self.event_manager = event_manager
        self.logger = logging.getLogger(__name__)
        
        # Fonts
        self.font = None
        self.large_font = None
        self._init_fonts()
        
        # UI Elements
        self.health_bar = HealthBar(10, 10, config.health_bar_width, config.health_bar_height)
        self.ammo_display = AmmoDisplay(10, 40)
        self.weapon_display = WeaponDisplay(10, 70)
        self.fps_counter = FPSCounter(config.window_width - 100, 10)
        
        # All UI elements list
        self.ui_elements: List[UIElement] = [
            self.health_bar,
            self.ammo_display,
            self.weapon_display,
            self.fps_counter
        ]
        
        # Subscribe to UI events
        self.event_manager.subscribe(EventType.UI_UPDATE_HEALTH, self._handle_health_update)
        self.event_manager.subscribe(EventType.UI_UPDATE_AMMO, self._handle_ammo_update)
        self.event_manager.subscribe(EventType.UI_UPDATE_WEAPON, self._handle_weapon_update)
        
        self.logger.info("Game UI system initialized")
    
    def _init_fonts(self) -> None:
        """Initialize fonts with English support"""
        if pygame:
            try:
                # Use default system font which works well for English
                self.font = pygame.font.Font(None, 24)
                self.large_font = pygame.font.Font(None, 36)
                self.logger.info("Fonts initialized successfully")
            except Exception as e:
                self.logger.warning(f"Font initialization failed: {e}")
                self.font = None
                self.large_font = None
        else:
            self.font = None
            self.large_font = None
    
    def update(self, dt: float, fps: float) -> None:
        """Update UI system"""
        # Update FPS display
        self.fps_counter.set_fps(fps)
        
        # Update all UI elements
        for element in self.ui_elements:
            element.update(dt)
    
    def render(self, screen) -> None:
        """Render all UI elements"""
        if not pygame or not self.font:
            return
        
        # Render all UI elements
        for element in self.ui_elements:
            if element.visible:
                element.render(screen, self.font)
    
    def _handle_health_update(self, event) -> None:
        """Handle health update event"""
        data = event.data
        current_health = data.get('current_health', 100)
        max_health = data.get('max_health', 100)
        
        self.health_bar.set_health(current_health, max_health)
    
    def _handle_ammo_update(self, event) -> None:
        """Handle ammo update event"""
        data = event.data
        current_ammo = data.get('current_ammo', 0)
        max_ammo = data.get('max_ammo', 0)
        is_reloading = data.get('is_reloading', False)
        reload_progress = data.get('reload_progress', 0.0)
        
        self.ammo_display.set_ammo(current_ammo, max_ammo, is_reloading, reload_progress)
    
    def _handle_weapon_update(self, event) -> None:
        """Handle weapon update event"""
        data = event.data
        weapon_name = data.get('weapon_name', 'Unknown Weapon')
        
        self.weapon_display.set_weapon(weapon_name)
    
    def show_message(self, message: str, duration: float = 3.0) -> None:
        """Show temporary message"""
        # TODO: Implement temporary message display
        self.logger.info(f"UI Message: {message}")
    
    def toggle_debug_info(self) -> None:
        """Toggle debug info display"""
        self.fps_counter.visible = not self.fps_counter.visible
    
    def set_ui_scale(self, scale: float) -> None:
        """Set UI scale"""
        self.config.ui_scale = scale
        # TODO: Recalculate all UI element sizes and positions
    
    def cleanup(self) -> None:
        """Cleanup UI system"""
        self.logger.info("UI system cleaned up")
