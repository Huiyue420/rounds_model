"""
音效系統
處理遊戲中的所有音效播放
"""

import pygame
import os
from typing import Dict, Optional
import logging

from ..core.config import GameConfig
from ..core.event_manager import EventManager, EventType


class SoundSystem:
    """音效系統"""
    
    def __init__(self, config: GameConfig, event_manager: EventManager):
        self.config = config
        self.event_manager = event_manager
        self.logger = logging.getLogger(__name__)
        
        # 音效字典
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.sound_enabled = config.sound_enabled
        
        # 初始化 pygame 音效
        if self.sound_enabled:
            try:
                pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
                pygame.mixer.init()
                self._load_sounds()
                self.logger.info("音效系統初始化完成")
            except Exception as e:
                self.logger.warning(f"音效系統初始化失敗: {e}")
                self.sound_enabled = False
        else:
            self.logger.info("音效已禁用")
        
        # 訂閱音效事件
        self.event_manager.subscribe(EventType.SOUND_PLAY, self._handle_play_sound)
    
    def _load_sounds(self) -> None:
        """載入所有音效檔案"""
        # 定義音效文件映射（如果文件存在則載入，否則跳過）
        sound_files = {
            # 武器音效
            'pistol_shoot': 'pistol_shot.wav',
            'shotgun_shoot': 'shotgun_shot.wav',
            'smg_shoot': 'smg_shot.wav',
            'sniper_shoot': 'sniper_shot.wav',
            'pistol_reload': 'pistol_reload.wav',
            'shotgun_reload': 'shotgun_reload.wav',
            'smg_reload': 'smg_reload.wav',
            'sniper_reload': 'sniper_reload.wav',
            
            # 玩家音效
            'jump': 'jump.wav',
            'land': 'land.wav',
            'footstep': 'footstep.wav',
            'hurt': 'hurt.wav',
            'death': 'death.wav',
            
            # 子彈音效
            'bullet_hit': 'bullet_hit.wav',
            'bullet_wall_hit': 'bullet_wall_hit.wav',
            
            # UI 音效
            'weapon_switch': 'weapon_switch.wav',
            'card_select': 'card_select.wav',
            'card_appear': 'card_appear.wav',
            
            # 環境音效
            'ambient': 'ambient.wav'
        }
        
        assets_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'sounds')
        
        for sound_name, filename in sound_files.items():
            file_path = os.path.join(assets_path, filename)
            try:
                if os.path.exists(file_path):
                    sound = pygame.mixer.Sound(file_path)
                    sound.set_volume(self.config.sound_volume)
                    self.sounds[sound_name] = sound
                    self.logger.debug(f"音效已載入: {sound_name}")
                else:
                    # 如果文件不存在，創建一個靜音的佔位音效
                    self._create_placeholder_sound(sound_name)
            except Exception as e:
                self.logger.warning(f"無法載入音效 {sound_name}: {e}")
                self._create_placeholder_sound(sound_name)
    
    def _create_placeholder_sound(self, sound_name: str) -> None:
        """創建佔位音效（靜音）"""
        try:
            # 創建一個非常短的靜音音效
            import numpy as np
            duration = 0.1  # 0.1 秒
            sample_rate = 22050
            samples = int(duration * sample_rate)
            wave_array = np.zeros((samples, 2), dtype=np.int16)
            
            sound = pygame.sndarray.make_sound(wave_array)
            sound.set_volume(0.0)  # 靜音
            self.sounds[sound_name] = sound
            self.logger.debug(f"創建佔位音效: {sound_name}")
        except Exception as e:
            self.logger.debug(f"無法創建佔位音效 {sound_name}: {e}")
    
    def play_sound(self, sound_name: str, volume: Optional[float] = None) -> None:
        """播放音效"""
        if not self.sound_enabled:
            return
        
        if sound_name in self.sounds:
            try:
                sound = self.sounds[sound_name]
                if volume is not None:
                    sound.set_volume(volume * self.config.sound_volume)
                sound.play()
                self.logger.debug(f"播放音效: {sound_name}")
            except Exception as e:
                self.logger.warning(f"播放音效失敗 {sound_name}: {e}")
        else:
            self.logger.debug(f"未找到音效: {sound_name}")
    
    def stop_sound(self, sound_name: str) -> None:
        """停止音效"""
        if not self.sound_enabled:
            return
        
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].stop()
                self.logger.debug(f"停止音效: {sound_name}")
            except Exception as e:
                self.logger.warning(f"停止音效失敗 {sound_name}: {e}")
    
    def set_volume(self, volume: float) -> None:
        """設置音效音量"""
        self.config.sound_volume = max(0.0, min(1.0, volume))
        
        if self.sound_enabled:
            for sound in self.sounds.values():
                sound.set_volume(self.config.sound_volume)
    
    def enable_sound(self) -> None:
        """啟用音效"""
        self.sound_enabled = True
        self.config.sound_enabled = True
        self.logger.info("音效已啟用")
    
    def disable_sound(self) -> None:
        """禁用音效"""
        self.sound_enabled = False
        self.config.sound_enabled = False
        
        # 停止所有正在播放的音效
        if pygame.mixer.get_init():
            pygame.mixer.stop()
        
        self.logger.info("音效已禁用")
    
    def _handle_play_sound(self, event) -> None:
        """處理播放音效事件"""
        sound_name = event.data.get('sound')
        volume = event.data.get('volume')
        
        if sound_name:
            self.play_sound(sound_name, volume)
    
    def cleanup(self) -> None:
        """清理音效系統"""
        if self.sound_enabled and pygame.mixer.get_init():
            pygame.mixer.quit()
        self.logger.info("音效系統已清理")
