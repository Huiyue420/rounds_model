"""
Sniper Rifle Weapon Class
High damage, low fire rate weapon
"""

from .weapon_base import WeaponBase
from ..core.config import GameConfig
from ..core.event_manager import EventManager


class Sniper(WeaponBase):
    """Sniper rifle class"""
    
    def __init__(self, config: GameConfig, event_manager: EventManager):
        super().__init__('sniper', config, event_manager)
    
    def get_display_name(self) -> str:
        """Get display name"""
        return "🎯 Sniper"
