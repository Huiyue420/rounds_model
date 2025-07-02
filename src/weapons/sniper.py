"""
狙擊槍武器類
高傷害低射速武器
"""

from .weapon_base import WeaponBase
from ..core.config import GameConfig
from ..core.event_manager import EventManager


class Sniper(WeaponBase):
    """狙擊槍類"""
    
    def __init__(self, config: GameConfig, event_manager: EventManager):
        super().__init__('sniper', config, event_manager)
    
    def get_display_name(self) -> str:
        """獲取顯示名稱"""
        return "🎯 狙擊槍"
