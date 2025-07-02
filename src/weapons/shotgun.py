"""
Shotgun Weapon Class
High damage, close-range weapon
"""

from .weapon_base import WeaponBase
from ..core.config import GameConfig
from ..core.event_manager import EventManager


class Shotgun(WeaponBase):
    """Shotgun class"""
    
    def __init__(self, config: GameConfig, event_manager: EventManager):
        super().__init__('shotgun', config, event_manager)
    
    def get_display_name(self) -> str:
        """Get display name"""
        return "💥 Shotgun"
