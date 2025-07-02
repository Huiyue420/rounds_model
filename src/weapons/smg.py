"""
衝鋒槍武器類
高射速低傷害武器
"""

from .weapon_base import WeaponBase
from ..core.config import GameConfig
from ..core.event_manager import EventManager


class SMG(WeaponBase):
    """衝鋒槍類"""
    
    def __init__(self, config: GameConfig, event_manager: EventManager):
        super().__init__('smg', config, event_manager)
    
    def get_display_name(self) -> str:
        """獲取顯示名稱"""
        return "🔥 衝鋒槍"
