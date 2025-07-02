"""
散彈槍武器類
近距離高傷害武器
"""

from .weapon_base import WeaponBase
from ..core.config import GameConfig
from ..core.event_manager import EventManager


class Shotgun(WeaponBase):
    """散彈槍類"""
    
    def __init__(self, config: GameConfig, event_manager: EventManager):
        super().__init__('shotgun', config, event_manager)
    
    def get_display_name(self) -> str:
        """獲取顯示名稱"""
        return "💥 散彈槍"
