"""
Pistol Weapon Class
Balanced basic weapon
"""

from .weapon_base import WeaponBase
from ..core.config import GameConfig
from ..core.event_manager import EventManager


class Pistol(WeaponBase):
    """Pistol class"""
    
    def __init__(self, config: GameConfig, event_manager: EventManager):
        super().__init__('pistol', config, event_manager)
    
    def get_display_name(self) -> str:
        """Get display name"""
        return "🔫 Pistol"
