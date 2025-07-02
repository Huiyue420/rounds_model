"""
SMG Weapon Class
High fire rate, low damage weapon
"""

from .weapon_base import WeaponBase
from ..core.config import GameConfig
from ..core.event_manager import EventManager


class SMG(WeaponBase):
    """SMG class"""
    
    def __init__(self, config: GameConfig, event_manager: EventManager):
        super().__init__('smg', config, event_manager)
    
    def get_display_name(self) -> str:
        """Get display name"""
        return "🔥 SMG"
