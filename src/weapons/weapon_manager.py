"""
武器管理器
管理玩家的武器切換和武器狀態
"""

from typing import List, Optional, Dict
import logging

from .weapon_base import WeaponBase
from .pistol import Pistol
from .shotgun import Shotgun
from .smg import SMG
from .sniper import Sniper
from ..core.config import GameConfig
from ..core.event_manager import EventManager, EventType


class WeaponManager:
    """武器管理器"""
    
    def __init__(self, config: GameConfig, event_manager: EventManager):
        self.config = config
        self.event_manager = event_manager
        self.logger = logging.getLogger(__name__)
        
        # 初始化所有武器
        self.weapons: Dict[str, WeaponBase] = {
            'pistol': Pistol(config, event_manager),
            'shotgun': Shotgun(config, event_manager),
            'smg': SMG(config, event_manager),
            'sniper': Sniper(config, event_manager)
        }
        
        # 當前武器
        self.current_weapon_type = 'pistol'
        self.weapon_order = ['pistol', 'shotgun', 'smg', 'sniper']
        
        self.logger.info("武器管理器初始化完成")
    
    @property
    def current_weapon(self) -> WeaponBase:
        """獲取當前武器"""
        return self.weapons[self.current_weapon_type]
    
    def switch_weapon(self, weapon_type: str) -> bool:
        """切換到指定武器"""
        if weapon_type in self.weapons and weapon_type != self.current_weapon_type:
            old_weapon = self.current_weapon_type
            self.current_weapon_type = weapon_type
            
            # 發送武器切換事件
            self.event_manager.emit(EventType.WEAPON_SWITCH, {
                'old_weapon': old_weapon,
                'new_weapon': weapon_type,
                'weapon_name': self.current_weapon.get_display_name()
            })
            
            self.logger.info(f"武器切換: {old_weapon} -> {weapon_type}")
            return True
        
        return False
    
    def next_weapon(self) -> bool:
        """切換到下一個武器"""
        current_index = self.weapon_order.index(self.current_weapon_type)
        next_index = (current_index + 1) % len(self.weapon_order)
        next_weapon = self.weapon_order[next_index]
        
        return self.switch_weapon(next_weapon)
    
    def previous_weapon(self) -> bool:
        """切換到上一個武器"""
        current_index = self.weapon_order.index(self.current_weapon_type)
        prev_index = (current_index - 1) % len(self.weapon_order)
        prev_weapon = self.weapon_order[prev_index]
        
        return self.switch_weapon(prev_weapon)
    
    def shoot(self, start_pos, target_pos) -> bool:
        """使用當前武器射擊"""
        return self.current_weapon.shoot(start_pos, target_pos)
    
    def reload(self) -> bool:
        """重裝當前武器"""
        return self.current_weapon.reload()
    
    def update(self, dt: float) -> None:
        """更新所有武器狀態"""
        for weapon in self.weapons.values():
            weapon.update(dt)
    
    def apply_card_effect(self, effect_type: str, value: float) -> None:
        """應用卡牌效果到所有武器"""
        for weapon in self.weapons.values():
            if effect_type == 'damage_boost':
                weapon.damage_multiplier += value
            elif effect_type == 'fire_rate_boost':
                weapon.fire_rate_multiplier += value
            elif effect_type == 'reload_speed_boost':
                weapon.reload_time_multiplier *= (1 - value)
            elif effect_type == 'magazine_size_boost':
                weapon.magazine_size_bonus += int(value)
            elif effect_type == 'bullet_size_boost':
                weapon.bullet_size_multiplier += value
        
        self.logger.info(f"卡牌效果已應用: {effect_type} = {value}")
    
    def get_weapon_info(self) -> Dict:
        """獲取當前武器信息"""
        weapon = self.current_weapon
        return {
            'type': self.current_weapon_type,
            'name': weapon.get_display_name(),
            'ammo': weapon.current_ammo,
            'max_ammo': weapon.get_max_magazine_size(),
            'is_reloading': weapon.is_reloading,
            'reload_progress': weapon.get_reload_progress()
        }
