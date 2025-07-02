"""
手槍武器類
平衡的基礎武器
"""

from .weapon_base import WeaponBase
from ..core.config import GameConfig
from ..core.event_manager import EventManager


class Pistol(WeaponBase):
    """手槍類"""
    
    def __init__(self, config: GameConfig, event_manager: EventManager):
        super().__init__('pistol', config, event_manager)
    
    def get_display_name(self) -> str:
        """獲取顯示名稱"""
        return "🔫 手槍"
