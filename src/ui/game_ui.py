"""
UI 系統 - 優化版本
處理遊戲內用戶界面顯示，包括血量條、彈藥顯示、武器信息等
"""

try:
    import pygame
except ImportError:
    pygame = None

from typing import Dict, List, Optional, Tuple, Any
import logging

from ..core.config import GameConfig
from ..core.event_manager import EventManager, EventType


class UIElement:
    """UI 元素基礎類"""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
        self.enabled = True
    
    def render(self, screen, font) -> None:
        """渲染 UI 元素"""
        pass
    
    def update(self, dt: float) -> None:
        """更新 UI 元素"""
        pass


class HealthBar(UIElement):
    """血量條"""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.current_health = 100
        self.max_health = 100
        self.background_color = (100, 100, 100)
        self.health_color = (100, 200, 100)
        self.low_health_color = (200, 100, 100)
        self.border_color = (255, 255, 255)
        self.low_health_threshold = 0.3
    
    def set_health(self, current: int, maximum: int) -> None:
        """設置血量"""
        self.current_health = max(0, current)
        self.max_health = max(1, maximum)
    
    def render(self, screen, font) -> None:
        """渲染血量條"""
        if not self.visible or not pygame:
            return
        
        # 背景
        bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.background_color, bg_rect)
        
        # 血量條
        health_ratio = self.current_health / self.max_health
        health_width = int(self.width * health_ratio)
        
        if health_width > 0:
            # 根據血量選擇顏色
            color = self.low_health_color if health_ratio < self.low_health_threshold else self.health_color
            health_rect = pygame.Rect(self.x, self.y, health_width, self.height)
            pygame.draw.rect(screen, color, health_rect)
        
        # 邊框
        pygame.draw.rect(screen, self.border_color, bg_rect, 2)
        
        # 血量文字
        health_text = f"{self.current_health}/{self.max_health}"
        text_surface = font.render(health_text, True, (255, 255, 255))
        text_x = self.x + (self.width - text_surface.get_width()) // 2
        text_y = self.y + (self.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))


class AmmoDisplay(UIElement):
    """彈藥顯示"""
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 120, 30)
        self.current_ammo = 0
        self.max_ammo = 0
        self.is_reloading = False
        self.reload_progress = 0.0
        self.text_color = (255, 255, 255)
        self.reload_color = (255, 255, 0)
    
    def set_ammo(self, current: int, maximum: int, reloading: bool = False, reload_progress: float = 0.0) -> None:
        """設置彈藥信息"""
        self.current_ammo = current
        self.max_ammo = maximum
        self.is_reloading = reloading
        self.reload_progress = reload_progress
    
    def render(self, screen, font) -> None:
        """渲染彈藥顯示"""
        if not self.visible or not pygame:
            return
        
        if self.is_reloading:
            # 顯示重裝進度
            text = f"重裝中... {self.reload_progress:.0%}"
            color = self.reload_color
        else:
            # 顯示彈藥數量
            text = f"彈藥: {self.current_ammo}/{self.max_ammo}"
            color = self.text_color
        
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (self.x, self.y))


class WeaponDisplay(UIElement):
    """武器顯示"""
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 200, 30)
        self.weapon_name = "手槍"
        self.text_color = (255, 255, 255)
    
    def set_weapon(self, weapon_name: str) -> None:
        """設置武器名稱"""
        self.weapon_name = weapon_name
    
    def render(self, screen, font) -> None:
        """渲染武器顯示"""
        if not self.visible or not pygame:
            return
        
        text = f"武器: {self.weapon_name}"
        text_surface = font.render(text, True, self.text_color)
        screen.blit(text_surface, (self.x, self.y))


class FPSCounter(UIElement):
    """FPS 計數器"""
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 100, 30)
        self.fps = 0
        self.text_color = (255, 255, 255)
    
    def set_fps(self, fps: float) -> None:
        """設置 FPS"""
        self.fps = fps
    
    def render(self, screen, font) -> None:
        """渲染 FPS 顯示"""
        if not self.visible or not pygame:
            return
        
        text = f"FPS: {self.fps:.1f}"
        text_surface = font.render(text, True, self.text_color)
        screen.blit(text_surface, (self.x, self.y))


class GameUI:
    """遊戲 UI 管理器"""
    
    def __init__(self, config: GameConfig, event_manager: EventManager):
        self.config = config
        self.event_manager = event_manager
        self.logger = logging.getLogger(__name__)
        
        # 字體
        self.font = None
        self.large_font = None
        self._init_fonts()
        
        # UI 元素
        self.health_bar = HealthBar(10, 10, config.health_bar_width, config.health_bar_height)
        self.ammo_display = AmmoDisplay(10, 40)
        self.weapon_display = WeaponDisplay(10, 70)
        self.fps_counter = FPSCounter(config.window_width - 100, 10)
        
        # 其他 UI 元素
        self.ui_elements: List[UIElement] = [
            self.health_bar,
            self.ammo_display,
            self.weapon_display,
            self.fps_counter
        ]
        
        # 訂閱 UI 相關事件
        self.event_manager.subscribe(EventType.UI_UPDATE_HEALTH, self._handle_health_update)
        self.event_manager.subscribe(EventType.UI_UPDATE_AMMO, self._handle_ammo_update)
        self.event_manager.subscribe(EventType.UI_UPDATE_WEAPON, self._handle_weapon_update)
        
        self.logger.info("遊戲 UI 系統初始化完成")
    
    def _init_fonts(self) -> None:
        """初始化字體"""
        if pygame:
            try:
                self.font = pygame.font.Font(None, 24)
                self.large_font = pygame.font.Font(None, 36)
            except Exception as e:
                self.logger.warning(f"字體初始化失敗: {e}")
                self.font = None
                self.large_font = None
        else:
            self.font = None
            self.large_font = None
    
    def update(self, dt: float, fps: float) -> None:
        """更新 UI 系統"""
        # 更新 FPS 顯示
        self.fps_counter.set_fps(fps)
        
        # 更新所有 UI 元素
        for element in self.ui_elements:
            element.update(dt)
    
    def render(self, screen) -> None:
        """渲染所有 UI 元素"""
        if not pygame or not self.font:
            return
        
        # 渲染所有 UI 元素
        for element in self.ui_elements:
            if element.visible:
                element.render(screen, self.font)
    
    def _handle_health_update(self, event) -> None:
        """處理血量更新事件"""
        data = event.data
        current_health = data.get('current_health', 100)
        max_health = data.get('max_health', 100)
        
        self.health_bar.set_health(current_health, max_health)
    
    def _handle_ammo_update(self, event) -> None:
        """處理彈藥更新事件"""
        data = event.data
        current_ammo = data.get('current_ammo', 0)
        max_ammo = data.get('max_ammo', 0)
        is_reloading = data.get('is_reloading', False)
        reload_progress = data.get('reload_progress', 0.0)
        
        self.ammo_display.set_ammo(current_ammo, max_ammo, is_reloading, reload_progress)
    
    def _handle_weapon_update(self, event) -> None:
        """處理武器更新事件"""
        data = event.data
        weapon_name = data.get('weapon_name', '未知武器')
        
        self.weapon_display.set_weapon(weapon_name)
    
    def show_message(self, message: str, duration: float = 3.0) -> None:
        """顯示臨時訊息"""
        # TODO: 實現臨時訊息顯示
        self.logger.info(f"UI 訊息: {message}")
    
    def toggle_debug_info(self) -> None:
        """切換調試信息顯示"""
        self.fps_counter.visible = not self.fps_counter.visible
    
    def set_ui_scale(self, scale: float) -> None:
        """設置 UI 縮放"""
        self.config.ui_scale = scale
        # TODO: 重新計算所有 UI 元素的大小和位置
    
    def cleanup(self) -> None:
        """清理 UI 系統"""
        self.logger.info("UI 系統已清理")
