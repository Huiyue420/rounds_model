"""
Weapon Base Class
Defines the base interface and common behavior for all weapons
"""

import math
import random
import time
from typing import Tuple, List, Optional, Dict, Any
from abc import ABC, abstractmethod

from ..core.config import GameConfig
from ..core.event_manager import EventManager, EventType


class WeaponBase(ABC):
    """Weapon base abstract class"""
    
    def __init__(self, weapon_type: str, config: GameConfig, event_manager: EventManager):
        self.weapon_type = weapon_type
        self.config = config
        self.event_manager = event_manager
        
        # Get weapon data from configuration
        weapon_data = config.weapon_configs[weapon_type]
        
        self.name = weapon_data['name']
        self.damage = weapon_data['damage']
        self.fire_rate = weapon_data['fire_rate']  # shots per second
        self.magazine_size = weapon_data['magazine_size']
        self.reload_time = weapon_data['reload_time']
        self.bullet_speed = weapon_data['bullet_speed']
        self.bullet_size = weapon_data['bullet_size']
        self.spread = weapon_data['spread']  # spread angle
        self.bullets_per_shot = weapon_data['bullets_per_shot']
        
        # Status
        self.current_ammo = self.magazine_size
        self.is_reloading = False
        self.reload_start_time = 0.0
        self.last_shot_time = 0.0
        
        # Modifier values (can be affected by cards)
        self.damage_multiplier = 1.0
        self.fire_rate_multiplier = 1.0
        self.reload_time_multiplier = 1.0
        self.magazine_size_bonus = 0
        self.bullet_size_multiplier = 1.0
    
    def can_shoot(self) -> bool:
        """Check if weapon can shoot"""
        current_time = time.time()
        fire_interval = 1.0 / (self.fire_rate * self.fire_rate_multiplier)
        
        return (not self.is_reloading and 
                self.current_ammo > 0 and 
                current_time - self.last_shot_time >= fire_interval)
    
    def shoot(self, start_pos: Tuple[float, float], target_pos: Tuple[float, float]) -> bool:
        """Shoot the weapon"""
        # Auto-reload if out of ammo
        if self.current_ammo == 0 and not self.is_reloading:
            self.reload()
            return False
        
        if not self.can_shoot():
            return False
        
        # Record shot time
        self.last_shot_time = time.time()
        self.current_ammo -= 1
        
        # Create bullets
        bullets_data = self._create_bullets(start_pos, target_pos)
        
        # Send fire event
        self.event_manager.emit(EventType.WEAPON_FIRE, {
            'weapon_type': self.weapon_type,
            'bullets': bullets_data,
            'ammo_remaining': self.current_ammo
        })
        
        # Play shoot sound
        self.event_manager.emit(EventType.SOUND_PLAY, {
            'sound': f'{self.weapon_type}_shoot'
        })
        
        # Auto-reload if this was the last bullet
        if self.current_ammo == 0:
            self.reload()
        
        return True
    
    def reload(self) -> bool:
        """Reload weapon"""
        if self.is_reloading or self.current_ammo == self.get_max_magazine_size():
            return False
        
        self.is_reloading = True
        self.reload_start_time = time.time()
        
        # Send reload start event
        self.event_manager.emit(EventType.WEAPON_RELOAD_START, {
            'weapon_type': self.weapon_type,
            'reload_time': self.get_reload_time()
        })
        
        # Play reload sound
        self.event_manager.emit(EventType.SOUND_PLAY, {
            'sound': f'{self.weapon_type}_reload'
        })
        
        return True
    
    def update(self, dt: float) -> None:
        """Update weapon status"""
        if self.is_reloading:
            current_time = time.time()
            if current_time - self.reload_start_time >= self.get_reload_time():
                self._complete_reload()
    
    def _complete_reload(self) -> None:
        """Complete reload"""
        self.is_reloading = False
        self.current_ammo = self.get_max_magazine_size()
        
        # Send reload complete event
        self.event_manager.emit(EventType.WEAPON_RELOAD_COMPLETE, {
            'weapon_type': self.weapon_type,
            'ammo': self.current_ammo
        })
    
    def _create_bullets(self, start_pos: Tuple[float, float], target_pos: Tuple[float, float]) -> List[Dict[str, Any]]:
        """Create bullet data"""
        bullets = []
        
        # Calculate base direction
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance == 0:
            base_angle = 0
        else:
            base_angle = math.atan2(dy, dx)
        
        # Create multiple bullets (shotgun will have multiple)
        for i in range(self.bullets_per_shot):
            # Calculate spread angle
            if self.bullets_per_shot > 1:
                # Uniform distribution spread
                spread_range = math.radians(self.spread)
                angle_offset = (i - (self.bullets_per_shot - 1) / 2) * (spread_range / (self.bullets_per_shot - 1))
            else:
                # Random spread for single shot weapons
                spread_range = math.radians(self.spread)
                angle_offset = (random.random() - 0.5) * spread_range
            
            bullet_angle = base_angle + angle_offset
            
            # Calculate bullet velocity
            bullet_vx = math.cos(bullet_angle) * self.bullet_speed
            bullet_vy = math.sin(bullet_angle) * self.bullet_speed
            
            # Calculate actual size
            actual_size = (
                int(self.bullet_size[0] * self.bullet_size_multiplier),
                int(self.bullet_size[1] * self.bullet_size_multiplier)
            )
            
            bullet_data = {
                'start_x': start_pos[0],
                'start_y': start_pos[1],
                'velocity_x': bullet_vx,
                'velocity_y': bullet_vy,
                'damage': int(self.damage * self.damage_multiplier),
                'size': actual_size,
                'weapon_type': self.weapon_type
            }
            
            bullets.append(bullet_data)
        
        return bullets
    
    def get_reload_time(self) -> float:
        """Get actual reload time"""
        return self.reload_time * self.reload_time_multiplier
    
    def get_max_magazine_size(self) -> int:
        """Get actual magazine size"""
        return self.magazine_size + self.magazine_size_bonus
    
    def get_damage(self) -> float:
        """Get actual damage value"""
        return self.damage * self.damage_multiplier
    
    def get_reload_progress(self) -> float:
        """Get reload progress (0.0 - 1.0)"""
        if not self.is_reloading:
            return 1.0
        
        current_time = time.time()
        elapsed = current_time - self.reload_start_time
        total_time = self.get_reload_time()
        
        return min(elapsed / total_time, 1.0)
    
    @abstractmethod
    def get_display_name(self) -> str:
        """Get display name"""
        pass
