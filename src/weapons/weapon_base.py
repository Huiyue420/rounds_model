"""
武器基礎類
定義所有武器的基礎接口和共同行為
"""

import math
import time
from typing import Tuple, List, Optional, Dict, Any
from abc import ABC, abstractmethod

from ..core.config import GameConfig
from ..core.event_manager import EventManager, EventType


class WeaponBase(ABC):
    """武器基礎抽象類"""
    
    def __init__(self, weapon_type: str, config: GameConfig, event_manager: EventManager):
        self.weapon_type = weapon_type
        self.config = config
        self.event_manager = event_manager
        
        # 從配置中獲取武器數據
        weapon_data = config.weapon_configs[weapon_type]
        
        self.name = weapon_data['name']
        self.damage = weapon_data['damage']
        self.fire_rate = weapon_data['fire_rate']  # 每秒射擊次數
        self.magazine_size = weapon_data['magazine_size']
        self.reload_time = weapon_data['reload_time']
        self.bullet_speed = weapon_data['bullet_speed']
        self.bullet_size = weapon_data['bullet_size']
        self.spread = weapon_data['spread']  # 散佈角度
        self.bullets_per_shot = weapon_data['bullets_per_shot']
        
        # 狀態
        self.current_ammo = self.magazine_size
        self.is_reloading = False
        self.reload_start_time = 0.0
        self.last_shot_time = 0.0
        
        # 修正值（可被卡牌影響）
        self.damage_multiplier = 1.0
        self.fire_rate_multiplier = 1.0
        self.reload_time_multiplier = 1.0
        self.magazine_size_bonus = 0
        self.bullet_size_multiplier = 1.0
    
    def can_shoot(self) -> bool:
        """檢查是否可以射擊"""
        current_time = time.time()
        fire_interval = 1.0 / (self.fire_rate * self.fire_rate_multiplier)
        
        return (not self.is_reloading and 
                self.current_ammo > 0 and 
                current_time - self.last_shot_time >= fire_interval)
    
    def shoot(self, start_pos: Tuple[float, float], target_pos: Tuple[float, float]) -> bool:
        """射擊"""
        if not self.can_shoot():
            return False
        
        # 記錄射擊時間
        self.last_shot_time = time.time()
        self.current_ammo -= 1
        
        # 創建子彈
        bullets_data = self._create_bullets(start_pos, target_pos)
        
        # 發送射擊事件
        self.event_manager.emit(EventType.WEAPON_FIRE, {
            'weapon_type': self.weapon_type,
            'bullets': bullets_data,
            'ammo_remaining': self.current_ammo
        })
        
        # 播放射擊音效
        self.event_manager.emit(EventType.SOUND_PLAY, {
            'sound': f'{self.weapon_type}_shoot'
        })
        
        return True
    
    def reload(self) -> bool:
        """重裝彈"""
        if self.is_reloading or self.current_ammo == self.get_max_magazine_size():
            return False
        
        self.is_reloading = True
        self.reload_start_time = time.time()
        
        # 發送重裝開始事件
        self.event_manager.emit(EventType.WEAPON_RELOAD_START, {
            'weapon_type': self.weapon_type,
            'reload_time': self.get_reload_time()
        })
        
        # 播放重裝音效
        self.event_manager.emit(EventType.SOUND_PLAY, {
            'sound': f'{self.weapon_type}_reload'
        })
        
        return True
    
    def update(self, dt: float) -> None:
        """更新武器狀態"""
        if self.is_reloading:
            current_time = time.time()
            if current_time - self.reload_start_time >= self.get_reload_time():
                self._complete_reload()
    
    def _complete_reload(self) -> None:
        """完成重裝"""
        self.is_reloading = False
        self.current_ammo = self.get_max_magazine_size()
        
        # 發送重裝完成事件
        self.event_manager.emit(EventType.WEAPON_RELOAD_COMPLETE, {
            'weapon_type': self.weapon_type,
            'ammo': self.current_ammo
        })
    
    def _create_bullets(self, start_pos: Tuple[float, float], target_pos: Tuple[float, float]) -> List[Dict[str, Any]]:
        """創建子彈數據"""
        bullets = []
        
        # 計算基礎方向
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance == 0:
            base_angle = 0
        else:
            base_angle = math.atan2(dy, dx)
        
        # 創建多顆子彈（散彈槍會有多顆）
        for i in range(self.bullets_per_shot):
            # 計算散佈角度
            if self.bullets_per_shot > 1:
                # 均勻分布散佈
                spread_range = math.radians(self.spread)
                angle_offset = (i - (self.bullets_per_shot - 1) / 2) * (spread_range / (self.bullets_per_shot - 1))
            else:
                # 單發武器的隨機散佈
                spread_range = math.radians(self.spread)
                angle_offset = (math.random() - 0.5) * spread_range
            
            bullet_angle = base_angle + angle_offset
            
            # 計算子彈速度
            bullet_vx = math.cos(bullet_angle) * self.bullet_speed
            bullet_vy = math.sin(bullet_angle) * self.bullet_speed
            
            # 計算實際大小
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
        """獲取實際重裝時間"""
        return self.reload_time * self.reload_time_multiplier
    
    def get_max_magazine_size(self) -> int:
        """獲取實際彈匣大小"""
        return self.magazine_size + self.magazine_size_bonus
    
    def get_reload_progress(self) -> float:
        """獲取重裝進度 (0.0 - 1.0)"""
        if not self.is_reloading:
            return 1.0
        
        current_time = time.time()
        elapsed = current_time - self.reload_start_time
        total_time = self.get_reload_time()
        
        return min(elapsed / total_time, 1.0)
    
    @abstractmethod
    def get_display_name(self) -> str:
        """獲取顯示名稱"""
        pass
