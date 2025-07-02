"""
Game Configuration Class - Optimized Version
Manages all game configuration parameters, including new weapon and card configurations
"""

from dataclasses import dataclass
from typing import Tuple, Dict, Any


@dataclass
class GameConfig:
    """Game Configuration Class - Optimized Version"""
    
    # Window settings
    window_width: int = 1280
    window_height: int = 720
    window_title: str = "ROUNDS Python - Optimized Version"
    fullscreen: bool = False
    
    # Game settings
    target_fps: int = 60
    debug: bool = False
    
    # Sound settings
    sound_enabled: bool = True
    sound_volume: float = 0.7
    music_volume: float = 0.5
    
    # Network settings
    server_mode: bool = False
    server_port: int = 8765
    server_host: str = "localhost"
    
    # Physics settings
    gravity: float = 980.0  # pixels/second^2
    physics_timestep: float = 1.0 / 60.0  # physics update frequency
    
    # Player settings
    player_speed: float = 300.0  # pixels/second
    player_jump_force: float = 500.0
    player_size: int = 32  # width and height
    player_max_health: int = 100
    
    # Weapon base settings
    base_bullet_speed: float = 800.0
    base_bullet_size: Tuple[int, int] = (8, 8)
    
    # Weapon configurations
    weapon_configs: Dict[str, Dict[str, Any]] = None  # type: ignore
    
    # UI settings
    ui_scale: float = 1.0
    health_bar_width: int = 200
    health_bar_height: int = 20
    font_size: int = 24
    
    # Card settings
    cards_per_selection: int = 3
    max_cards_per_player: int = 10
    
    # Color settings (RGB)
    background_color: Tuple[int, int, int] = (30, 30, 40)
    player_color: Tuple[int, int, int] = (100, 150, 255)
    enemy_color: Tuple[int, int, int] = (255, 100, 100)
    bullet_color: Tuple[int, int, int] = (255, 255, 100)
    platform_color: Tuple[int, int, int] = (100, 100, 100)
    ui_color: Tuple[int, int, int] = (70, 70, 80)
    text_color: Tuple[int, int, int] = (255, 255, 255)
    
    @property
    def window_size(self) -> Tuple[int, int]:
        """Get window size as tuple"""
        return (self.window_width, self.window_height)
    
    def __post_init__(self):
        """Post-initialization processing, set weapon configurations"""
        if self.weapon_configs is None:
            self.weapon_configs = {
                'pistol': {
                    'name': 'Pistol',
                    'damage': 25,
                    'fire_rate': 2.0,  # shots per second
                    'magazine_size': 8,
                    'reload_time': 1.5,
                    'bullet_speed': 800.0,
                    'bullet_size': (8, 8),
                    'spread': 0,  # spread angle (degrees)
                    'bullets_per_shot': 1,
                },
                'shotgun': {
                    'name': 'Shotgun',
                    'damage': 15,
                    'fire_rate': 1.0,
                    'magazine_size': 4,
                    'reload_time': 2.5,
                    'bullet_speed': 600.0,
                    'bullet_size': (6, 6),
                    'spread': 25,  # spread angle
                    'bullets_per_shot': 5,  # bullets per shot
                },
                'smg': {
                    'name': 'SMG',
                    'damage': 15,
                    'fire_rate': 8.0,
                    'magazine_size': 24,
                    'reload_time': 2.0,
                    'bullet_speed': 750.0,
                    'bullet_size': (6, 6),
                    'spread': 5,
                    'bullets_per_shot': 1,
                },
                'sniper': {
                    'name': 'Sniper',
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
