"""
主遊戲類 - 優化版本
管理遊戲的主循環和核心系統，整合所有新功能
"""

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    pygame = None

import sys
from typing import Optional, List
import logging
import time

from .config import GameConfig
from .event_manager import EventManager, EventType
from ..systems.physics_system import PhysicsSystem
from ..systems.sound_system import SoundSystem
from ..ui.game_ui import GameUI
from ..ui.card_selection_ui import CardSelectionUI
from ..weapons.weapon_manager import WeaponManager
from ..cards.card_manager import CardManager


# 為了避免循環導入，我們需要創建簡化版的實體類
class SimplePlayer:
    """簡化的玩家類用於演示"""
    
    def __init__(self, x: float, y: float, config: GameConfig, player_id: int = 0):
        self.player_id = player_id
        self.health = config.player_max_health
        self.max_health = config.player_max_health
        self.alive = True
        
        # 卡牌效果修正值
        self.damage_reduction = 0.0
        self.healing_rate = 0.0
        self.speed_multiplier = 1.0
        self.jump_force_multiplier = 1.0
        self.max_jumps = 1
        self.current_jumps = 0
        
        # 簡化的物理體（會在完整版本中使用真正的物理體）
        self.position = {'x': x, 'y': y}
        self.velocity = {'x': 0, 'y': 0}
        
        # 武器管理器
        self.weapon_manager = None  # 將在遊戲中設置
    
    def take_damage(self, damage: int) -> None:
        """受到傷害"""
        actual_damage = int(damage * (1.0 - self.damage_reduction))
        self.health = max(0, self.health - actual_damage)
        
        if self.health <= 0:
            self.alive = False
    
    def heal(self, amount: int) -> None:
        """恢復血量"""
        self.health = min(self.max_health, self.health + amount)
    
    def update(self, dt: float) -> None:
        """更新玩家狀態"""
        # 快速治療效果
        if self.healing_rate > 0:
            self.heal(int(self.healing_rate * dt))


class SimpleWorld:
    """簡化的世界類"""
    
    def __init__(self, config: GameConfig):
        self.config = config
        self.platforms = []
        self._create_basic_world()
    
    def _create_basic_world(self) -> None:
        """創建基礎世界"""
        # 創建地面平台
        ground_platform = {
            'x': self.config.window_width // 2,
            'y': self.config.window_height - 25,
            'width': self.config.window_width,
            'height': 50
        }
        self.platforms.append(ground_platform)
        
        # 創建一些浮動平台
        platforms_data = [
            (200, 500, 200, 20),
            (600, 400, 200, 20),
            (1000, 350, 200, 20),
            (400, 250, 150, 20)
        ]
        
        for x, y, width, height in platforms_data:
            platform = {
                'x': x + width // 2,
                'y': y + height // 2,
                'width': width,
                'height': height
            }
            self.platforms.append(platform)
    
    def render(self, screen) -> None:
        """渲染世界"""
        if not pygame:
            return
        
        # 渲染所有平台
        for platform in self.platforms:
            rect = pygame.Rect(
                platform['x'] - platform['width'] // 2,
                platform['y'] - platform['height'] // 2,
                platform['width'],
                platform['height']
            )
            pygame.draw.rect(screen, self.config.platform_color, rect)


class Game:
    """主遊戲類 - 優化版本"""
    
    def __init__(self, config: GameConfig):
        self.config = config
        self.running = False
        self.clock = None
        self.screen = None
        
        # 設置日誌
        log_level = logging.DEBUG if config.debug else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # 檢查 pygame 可用性
        if not PYGAME_AVAILABLE:
            self.logger.error("Pygame 未安裝，無法運行遊戲")
            self.logger.info("請運行: pip install pygame")
            return
        
        # 初始化 pygame
        self._init_pygame()
        
        # 初始化系統
        self.event_manager = EventManager()
        self.physics_system = PhysicsSystem(config)
        self.sound_system = SoundSystem(config, self.event_manager)
        
        # 初始化 UI 系統
        self.game_ui = GameUI(config, self.event_manager)
        self.card_selection_ui = CardSelectionUI(config, self.event_manager)
        
        # 初始化遊戲管理器
        self.weapon_manager = WeaponManager(config, self.event_manager)
        self.card_manager = CardManager(self.event_manager)
        
        # 初始化遊戲世界和玩家
        self.world = SimpleWorld(config)
        self.players: List[SimplePlayer] = []
        self._create_players()
        
        # 遊戲狀態
        self.game_state = "playing"  # playing, card_selection, paused
        self.selected_player_for_cards = None
        
        # 註冊事件處理器
        self._register_event_handlers()
        
        # 統計信息
        self.frame_count = 0
        self.last_fps_update = time.time()
        self.current_fps = 0.0
        
        self.logger.info("遊戲初始化完成（優化版本）")
    
    def _init_pygame(self) -> None:
        """初始化 Pygame"""
        if not PYGAME_AVAILABLE:
            return
        
        pygame.init()
        
        # 創建視窗
        flags = pygame.FULLSCREEN if self.config.fullscreen else 0
        self.screen = pygame.display.set_mode(self.config.window_size, flags)
        pygame.display.set_caption(self.config.window_title)
        
        # 初始化時鐘
        self.clock = pygame.time.Clock()
        
        self.logger.info(f"Pygame 初始化完成 - 解析度: {self.config.window_size}")
    
    def _create_players(self) -> None:
        """創建玩家"""
        # 創建本地玩家
        start_x = self.config.window_width // 2
        start_y = self.config.window_height - 100
        
        player = SimplePlayer(start_x, start_y, self.config, player_id=1)
        player.weapon_manager = self.weapon_manager
        
        self.players.append(player)
        self.logger.info(f"玩家已創建 - 位置: ({start_x}, {start_y})")
    
    def _register_event_handlers(self) -> None:
        """註冊事件處理器"""
        self.event_manager.subscribe(EventType.WEAPON_SWITCH, self._handle_weapon_switch)
        self.event_manager.subscribe(EventType.CARD_SELECT, self._handle_card_select)
        self.event_manager.subscribe(EventType.PLAYER_DEATH, self._handle_player_death)
    
    def run(self) -> None:
        """運行遊戲主循環"""
        if not PYGAME_AVAILABLE:
            self.logger.error("無法啟動遊戲：Pygame 未可用")
            return
        
        self.running = True
        self.logger.info("遊戲開始運行")
        
        try:
            while self.running:
                # 計算 delta time
                dt = self.clock.tick(self.config.target_fps) / 1000.0
                
                # 處理事件
                self._handle_events()
                
                # 更新遊戲
                if self.game_state == "playing":
                    self._update(dt)
                elif self.game_state == "card_selection":
                    self._update_card_selection(dt)
                
                # 渲染
                self._render()
                
                # 更新顯示
                pygame.display.flip()
                
                # 更新統計信息
                self._update_statistics()
                
        except Exception as e:
            self.logger.error(f"遊戲運行錯誤: {e}")
            if self.config.debug:
                raise
        finally:
            self._cleanup()
    
    def _handle_events(self) -> None:
        """處理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event)
    
    def _handle_keydown(self, event) -> None:
        """處理按鍵事件"""
        if event.key == pygame.K_ESCAPE:
            self.running = False
        elif event.key == pygame.K_q:
            # 切換到上一個武器
            self.weapon_manager.previous_weapon()
        elif event.key == pygame.K_e:
            # 切換到下一個武器
            self.weapon_manager.next_weapon()
        elif event.key == pygame.K_r:
            # 重裝
            self.weapon_manager.reload()
        elif event.key == pygame.K_c:
            # 測試卡牌選擇
            self._show_card_selection_test()
        elif event.key == pygame.K_t:
            # 測試傷害
            if self.players:
                self.players[0].take_damage(20)
                self._update_ui()
        elif event.key == pygame.K_h:
            # 測試治療
            if self.players:
                self.players[0].heal(25)
                self._update_ui()
    
    def _handle_mouse_click(self, event) -> None:
        """處理滑鼠點擊"""
        if event.button == 1:  # 左鍵
            if self.game_state == "card_selection":
                # 卡牌選擇模式
                self.card_selection_ui.handle_click(event.pos)
            else:
                # 正常遊戲模式 - 射擊
                if self.players:
                    start_pos = (self.players[0].position['x'], self.players[0].position['y'])
                    target_pos = event.pos
                    self.weapon_manager.shoot(start_pos, target_pos)
                    self._update_ui()
    
    def _update(self, dt: float) -> None:
        """更新遊戲狀態"""
        # 處理事件隊列
        self.event_manager.process_events()
        
        # 更新武器系統
        self.weapon_manager.update(dt)
        
        # 更新玩家
        for player in self.players:
            player.update(dt)
        
        # 更新物理系統
        self.physics_system.update(dt)
        
        # 更新 UI
        self.game_ui.update(dt, self.current_fps)
        
        # 定期更新 UI 顯示
        self._update_ui()
    
    def _update_card_selection(self, dt: float) -> None:
        """更新卡牌選擇狀態"""
        self.card_selection_ui.update(dt)
    
    def _render(self) -> None:
        """渲染遊戲畫面"""
        # 清除畫面
        self.screen.fill(self.config.background_color)
        
        # 渲染世界
        self.world.render(self.screen)
        
        # 渲染玩家（簡化版本）
        self._render_players()
        
        # 渲染 UI
        self.game_ui.render(self.screen)
        
        # 渲染卡牌選擇界面
        if self.game_state == "card_selection":
            self.card_selection_ui.render(self.screen)
        
        # 渲染調試資訊
        if self.config.debug:
            self._render_debug_info()
    
    def _render_players(self) -> None:
        """渲染玩家（簡化版本）"""
        for player in self.players:
            if player.alive:
                # 簡單的玩家矩形
                player_rect = pygame.Rect(
                    int(player.position['x'] - 16),
                    int(player.position['y'] - 24),
                    32, 48
                )
                color = self.config.player_color
                pygame.draw.rect(self.screen, color, player_rect)
                
                # 玩家血量條
                self._render_player_health_bar(player, player_rect)
    
    def _render_player_health_bar(self, player: SimplePlayer, player_rect) -> None:
        """渲染玩家血量條"""
        bar_width = 40
        bar_height = 6
        bar_x = player_rect.centerx - bar_width // 2
        bar_y = player_rect.top - 10
        
        # 背景
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.screen, (100, 100, 100), bg_rect)
        
        # 血量
        health_ratio = player.health / player.max_health
        health_width = int(bar_width * health_ratio)
        if health_width > 0:
            health_color = (100, 200, 100) if health_ratio > 0.3 else (200, 100, 100)
            health_rect = pygame.Rect(bar_x, bar_y, health_width, bar_height)
            pygame.draw.rect(self.screen, health_color, health_rect)
    
    def _render_debug_info(self) -> None:
        """渲染調試資訊"""
        font = pygame.font.Font(None, 24)
        debug_info = [
            f"玩家數量: {len(self.players)}",
            f"物理體數量: {self.physics_system.get_bodies_count()}",
            f"活躍物理體: {self.physics_system.get_active_bodies_count()}",
            f"遊戲狀態: {self.game_state}",
            f"當前武器: {self.weapon_manager.current_weapon.get_display_name()}",
        ]
        
        y_offset = 200
        for info in debug_info:
            text_surface = font.render(info, True, (255, 255, 0))
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 25
    
    def _update_statistics(self) -> None:
        """更新統計信息"""
        self.frame_count += 1
        current_time = time.time()
        
        if current_time - self.last_fps_update >= 1.0:
            self.current_fps = self.frame_count / (current_time - self.last_fps_update)
            self.frame_count = 0
            self.last_fps_update = current_time
    
    def _update_ui(self) -> None:
        """更新 UI 顯示"""
        if not self.players:
            return
        
        player = self.players[0]
        
        # 更新血量顯示
        self.event_manager.emit(EventType.UI_UPDATE_HEALTH, {
            'current_health': player.health,
            'max_health': player.max_health
        })
        
        # 更新武器和彈藥顯示
        weapon_info = self.weapon_manager.get_weapon_info()
        self.event_manager.emit(EventType.UI_UPDATE_WEAPON, {
            'weapon_name': weapon_info['name']
        })
        
        self.event_manager.emit(EventType.UI_UPDATE_AMMO, {
            'current_ammo': weapon_info['ammo'],
            'max_ammo': weapon_info['max_ammo'],
            'is_reloading': weapon_info['is_reloading'],
            'reload_progress': weapon_info['reload_progress']
        })
    
    def _show_card_selection_test(self) -> None:
        """顯示測試卡牌選擇"""
        if self.players and self.game_state == "playing":
            # 獲取隨機卡牌
            cards = self.card_manager.get_random_cards(3)
            cards_data = [card.to_dict() for card in cards]
            
            # 顯示卡牌選擇界面
            self.card_selection_ui.show_selection(
                player_id=self.players[0].player_id,
                cards_data=cards_data,
                callback=self._on_card_selected
            )
            
            self.game_state = "card_selection"
            self.selected_player_for_cards = self.players[0]
    
    def _on_card_selected(self, player_id: int, card_data: dict) -> None:
        """卡牌選擇回調"""
        if self.selected_player_for_cards:
            # 創建卡牌實例
            card = self.card_manager.create_card(card_data['id'])
            if card:
                # 添加到玩家
                self.card_manager.add_card_to_player(player_id, card)
                # 應用效果
                self.card_manager.apply_card_to_player(player_id, card, self.selected_player_for_cards)
                
                self.logger.info(f"玩家 {player_id} 獲得卡牌: {card_data['name']}")
        
        # 返回遊戲模式
        self.game_state = "playing"
        self.selected_player_for_cards = None
        
        # 更新 UI
        self._update_ui()
    
    def _handle_weapon_switch(self, event) -> None:
        """處理武器切換事件"""
        data = event.data
        new_weapon = data.get('new_weapon', '')
        weapon_name = data.get('weapon_name', '')
        
        self.logger.info(f"武器已切換: {weapon_name}")
        
        # 播放切換音效
        self.event_manager.emit(EventType.SOUND_PLAY, {
            'sound': 'weapon_switch'
        })
        
        # 更新 UI
        self._update_ui()
    
    def _handle_card_select(self, event) -> None:
        """處理卡牌選擇事件"""
        data = event.data
        card_data = data.get('card_data', {})
        
        self.logger.info(f"卡牌已選擇: {card_data.get('name', '未知')}")
    
    def _handle_player_death(self, event) -> None:
        """處理玩家死亡事件"""
        data = event.data
        player_id = data.get('player_id', 0)
        
        self.logger.info(f"玩家 {player_id} 死亡")
        
        # TODO: 實現重生邏輯
    
    def _cleanup(self) -> None:
        """清理資源"""
        self.logger.info("正在清理遊戲資源...")
        
        # 清理各個系統
        if hasattr(self, 'sound_system'):
            self.sound_system.cleanup()
        
        if hasattr(self, 'physics_system'):
            self.physics_system.cleanup()
        
        if hasattr(self, 'game_ui'):
            self.game_ui.cleanup()
        
        # 清理 pygame
        if PYGAME_AVAILABLE:
            pygame.quit()
        
        self.logger.info("遊戲已關閉")
