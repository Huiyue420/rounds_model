"""
遊戲配置類 - 優化版本
管理遊戲的所有配置參數，包含新增的武器和卡牌配置
"""

from dataclasses import dataclass
from typing import Tuple, Dict, Any


@dataclass
class GameConfig:
    """遊戲配置類 - 優化版本"""
    
    # 視窗設置
    window_width: int = 1280
    window_height: int = 720
    window_title: str = "ROUNDS Python - 優化版本"
    fullscreen: bool = False
    
    # 遊戲設置
    target_fps: int = 60
    debug: bool = False
    
    # 音效設置
    sound_enabled: bool = True
    sound_volume: float = 0.7
    music_volume: float = 0.5
    
    # 網路設置
    server_mode: bool = False
    server_port: int = 8765
    server_host: str = "localhost"
    
    # 物理設置
    gravity: float = 980.0  # 像素/秒^2
    physics_timestep: float = 1.0 / 60.0  # 物理更新頻率
    
    # 玩家設置
    player_speed: float = 300.0  # 像素/秒
    player_jump_force: float = 500.0
    player_size: Tuple[int, int] = (32, 48)
    player_max_health: int = 100
    
    # 武器基礎設置
    base_bullet_speed: float = 800.0
    base_bullet_size: Tuple[int, int] = (8, 8)
    
    # 武器配置
    weapon_configs: Dict[str, Dict[str, Any]] = None  # type: ignore
    
    # UI 設置
    ui_scale: float = 1.0
    health_bar_width: int = 200
    health_bar_height: int = 20
    
    # 卡牌設置
    cards_per_selection: int = 3
    max_cards_per_player: int = 10
    
    # 顏色設置 (RGB)
    background_color: Tuple[int, int, int] = (30, 30, 40)
    player_color: Tuple[int, int, int] = (100, 150, 255)
    enemy_color: Tuple[int, int, int] = (255, 100, 100)
    bullet_color: Tuple[int, int, int] = (255, 255, 100)
    platform_color: Tuple[int, int, int] = (100, 100, 100)
    ui_color: Tuple[int, int, int] = (70, 70, 80)
    text_color: Tuple[int, int, int] = (255, 255, 255)
    
    def __post_init__(self):
        """初始化後處理，設置武器配置"""
        if self.weapon_configs is None:
            self.weapon_configs = {
                'pistol': {
                    'name': '手槍',
                    'damage': 25,
                    'fire_rate': 2.0,  # 每秒射擊次數
                    'magazine_size': 8,
                    'reload_time': 1.5,
                    'bullet_speed': 800.0,
                    'bullet_size': (8, 8),
                    'spread': 0,  # 散佈角度（度）
                    'bullets_per_shot': 1,
                },
                'shotgun': {
                    'name': '散彈槍',
                    'damage': 15,
                    'fire_rate': 1.0,
                    'magazine_size': 4,
                    'reload_time': 2.5,
                    'bullet_speed': 600.0,
                    'bullet_size': (6, 6),
                    'spread': 25,  # 散佈角度
                    'bullets_per_shot': 5,  # 每次射擊的子彈數
                },
                'smg': {
                    'name': '衝鋒槍',
                    'damage': 15,
                    'fire_rate': 8.0,
                    'magazine_size': 24,
                    'reload_time': 2.0,
                    'bullet_speed': 700.0,
                    'bullet_size': (6, 6),
                    'spread': 5,
                    'bullets_per_shot': 1,
                },
                'sniper': {
                    'name': '狙擊槍',
                    'damage': 75,
                    'fire_rate': 0.5,
                    'magazine_size': 3,
                    'reload_time': 3.0,
                    'bullet_speed': 1200.0,
                    'bullet_size': (10, 10),
                    'spread': 0,
                    'bullets_per_shot': 1,
                }
            }
    
    @property
    def window_size(self) -> Tuple[int, int]:
        """獲取視窗大小"""
        return (self.window_width, self.window_height)
