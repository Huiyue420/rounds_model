"""
Card Selection UI
Displays card selection interface, allows players to choose from multiple cards
"""

try:
    import pygame
except ImportError:
    pygame = None

from typing import List, Dict, Optional, Callable
import logging

from ..core.config import GameConfig
from ..core.event_manager import EventManager, EventType


class CardUI:
    """UI representation of a single card"""
    
    def __init__(self, card_data: Dict, x: int, y: int, width: int, height: int):
        self.card_data = card_data
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hovered = False
        self.selected = False
        
        # Colors
        self.background_color = card_data.get('color', (100, 100, 100))
        self.border_color = (255, 255, 255)
        self.hover_color = (255, 255, 200)
        self.text_color = (255, 255, 255)
        
        # Animation
        self.hover_animation = 0.0
        self.target_hover = 0.0
        self.animation_speed = 8.0
    
    def update(self, dt: float, mouse_pos: tuple) -> None:
        """Update card status"""
        # Check mouse hover
        if pygame:
            mouse_x, mouse_y = mouse_pos
            self.hovered = (self.x <= mouse_x <= self.x + self.width and 
                           self.y <= mouse_y <= self.y + self.height)
        
        # Update hover animation
        self.target_hover = 1.0 if self.hovered else 0.0
        if self.hover_animation != self.target_hover:
            diff = self.target_hover - self.hover_animation
            self.hover_animation += diff * self.animation_speed * dt
            self.hover_animation = max(0.0, min(1.0, self.hover_animation))
    
    def render(self, screen, font, small_font) -> None:
        """Render card"""
        if not pygame:
            return
        
        # Calculate hover effect
        hover_offset = int(self.hover_animation * 5)
        card_y = self.y - hover_offset
        
        # Card background
        card_rect = pygame.Rect(self.x, card_y, self.width, self.height)
        
        # Blend colors (brighten when hovered)
        bg_color = self._blend_colors(self.background_color, self.hover_color, self.hover_animation * 0.3)
        pygame.draw.rect(screen, bg_color, card_rect)
        
        # Border
        border_width = 3 if self.hovered else 2
        pygame.draw.rect(screen, self.border_color, card_rect, border_width)
        
        # Card icon
        icon = self.card_data.get('icon', '❓')
        icon_surface = font.render(icon, True, self.text_color)
        icon_x = self.x + (self.width - icon_surface.get_width()) // 2
        icon_y = card_y + 10
        screen.blit(icon_surface, (icon_x, icon_y))
        
        # Card name
        name = self.card_data.get('name', 'Unknown Card')
        name_surface = small_font.render(name, True, self.text_color)
        name_x = self.x + (self.width - name_surface.get_width()) // 2
        name_y = icon_y + icon_surface.get_height() + 5
        screen.blit(name_surface, (name_x, name_y))
        
        # Card description (multiline display)
        description = self.card_data.get('description', '')
        self._render_multiline_text(screen, small_font, description, 
                                  self.x + 5, name_y + 25, 
                                  self.width - 10, self.text_color)
        
        # Rarity indicator
        rarity = self.card_data.get('rarity', 'common')
        rarity_color = self._get_rarity_color(rarity)
        rarity_rect = pygame.Rect(self.x, card_y, self.width, 5)
        pygame.draw.rect(screen, rarity_color, rarity_rect)
    
    def _blend_colors(self, color1: tuple, color2: tuple, factor: float) -> tuple:
        """Blend two colors"""
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        
        return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    
    def _render_multiline_text(self, screen, font, text: str, x: int, y: int, 
                              max_width: int, color: tuple) -> None:
        """Render multiline text"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Render each line
        line_height = font.get_height()
        for i, line in enumerate(lines):
            if y + i * line_height < self.y + self.height - 10:  # Ensure it doesn't exceed card boundaries
                line_surface = font.render(line, True, color)
                screen.blit(line_surface, (x, y + i * line_height))
    
    def _get_rarity_color(self, rarity: str) -> tuple:
        """Get color based on rarity"""
        colors = {
            'common': (200, 200, 200),      # Gray
            'rare': (100, 150, 255),        # Blue
            'epic': (150, 100, 255),        # Purple
            'legendary': (255, 200, 50)     # Orange
        }
        return colors.get(rarity, (255, 255, 255))
    
    def is_clicked(self, mouse_pos: tuple) -> bool:
        """Check if clicked"""
        if not pygame:
            return False
        
        mouse_x, mouse_y = mouse_pos
        return (self.x <= mouse_x <= self.x + self.width and 
                self.y <= mouse_y <= self.y + self.height)


class CardSelectionUI:
    """Card selection interface"""
    
    def __init__(self, config: GameConfig, event_manager: EventManager):
        self.config = config
        self.event_manager = event_manager
        self.logger = logging.getLogger(__name__)
        
        # 界面狀態
        self.visible = False
        self.cards: List[CardUI] = []
        self.player_id = 0
        self.selection_callback: Optional[Callable] = None
        
        # 界面設置
        self.card_width = 180
        self.card_height = 240
        self.card_spacing = 20
        self.background_alpha = 180
        
        # 字體
        self.font = None
        self.small_font = None
        self._init_fonts()
        
        # 顏色
        self.background_color = (0, 0, 0)
        self.title_color = (255, 255, 255)
        self.instruction_color = (200, 200, 200)
        
        # 訂閱事件
        self.event_manager.subscribe(EventType.CARD_SHOW_SELECTION, self._handle_show_selection)
        self.event_manager.subscribe(EventType.CARD_HIDE_SELECTION, self._handle_hide_selection)
        
        self.logger.info("Card selection UI initialization completed")
    
    def _init_fonts(self) -> None:
        """Initialize fonts"""
        if pygame:
            try:
                self.font = pygame.font.Font(None, 36)
                self.small_font = pygame.font.Font(None, 20)
            except Exception as e:
                self.logger.warning(f"Card UI font initialization failed: {e}")
                self.font = None
                self.small_font = None
    
    def show_selection(self, player_id: int, cards_data: List[Dict], 
                      callback: Optional[Callable] = None) -> None:
        """Show card selection interface"""
        self.visible = True
        self.player_id = player_id
        self.selection_callback = callback
        self.cards.clear()
        
        # Calculate card positions
        total_width = len(cards_data) * self.card_width + (len(cards_data) - 1) * self.card_spacing
        start_x = (self.config.window_width - total_width) // 2
        start_y = (self.config.window_height - self.card_height) // 2
        
        # 創建卡牌 UI
        for i, card_data in enumerate(cards_data):
            x = start_x + i * (self.card_width + self.card_spacing)
            card_ui = CardUI(card_data, x, start_y, self.card_width, self.card_height)
            self.cards.append(card_ui)
        
        self.logger.info(f"顯示卡牌選擇界面 - 玩家 {player_id}, {len(cards_data)} 張卡牌")
    
    def hide_selection(self) -> None:
        """隱藏卡牌選擇界面"""
        self.visible = False
        self.cards.clear()
        self.selection_callback = None
        self.logger.info("隱藏卡牌選擇界面")
    
    def update(self, dt: float) -> None:
        """更新卡牌選擇界面"""
        if not self.visible or not pygame:
            return
        
        mouse_pos = pygame.mouse.get_pos()
        
        # 更新所有卡牌
        for card in self.cards:
            card.update(dt, mouse_pos)
    
    def handle_click(self, mouse_pos: tuple) -> None:
        """處理滑鼠點擊"""
        if not self.visible:
            return
        
        for i, card in enumerate(self.cards):
            if card.is_clicked(mouse_pos):
                self._select_card(i, card.card_data)
                break
    
    def _select_card(self, card_index: int, card_data: Dict) -> None:
        """選擇卡牌"""
        # 發送卡牌選擇事件
        self.event_manager.emit(EventType.CARD_SELECT, {
            'player_id': self.player_id,
            'card_index': card_index,
            'card_data': card_data
        })
        
        # 播放選擇音效
        self.event_manager.emit(EventType.SOUND_PLAY, {
            'sound': 'card_select'
        })
        
        # 執行回調
        if self.selection_callback:
            self.selection_callback(self.player_id, card_data)
        
        # 隱藏界面
        self.hide_selection()
        
        self.logger.info(f"玩家 {self.player_id} 選擇了卡牌: {card_data.get('name', '未知')}")
    
    def render(self, screen) -> None:
        """渲染卡牌選擇界面"""
        if not self.visible or not pygame or not self.font:
            return
        
        # 半透明背景
        overlay = pygame.Surface((self.config.window_width, self.config.window_height))
        overlay.set_alpha(self.background_alpha)
        overlay.fill(self.background_color)
        screen.blit(overlay, (0, 0))
        
        # 標題
        title_text = "選擇一張卡牌"
        title_surface = self.font.render(title_text, True, self.title_color)
        title_x = (self.config.window_width - title_surface.get_width()) // 2
        title_y = self.config.window_height // 2 - self.card_height // 2 - 60
        screen.blit(title_surface, (title_x, title_y))
        
        # 說明文字
        instruction_text = "點擊卡牌來選擇"
        instruction_surface = self.small_font.render(instruction_text, True, self.instruction_color)
        instruction_x = (self.config.window_width - instruction_surface.get_width()) // 2
        instruction_y = title_y + title_surface.get_height() + 10
        screen.blit(instruction_surface, (instruction_x, instruction_y))
        
        # 渲染所有卡牌
        for card in self.cards:
            card.render(screen, self.font, self.small_font)
    
    def _handle_show_selection(self, event) -> None:
        """處理顯示選擇事件"""
        data = event.data
        player_id = data.get('player_id', 0)
        cards_data = data.get('cards', [])
        
        self.show_selection(player_id, cards_data)
    
    def _handle_hide_selection(self, event) -> None:
        """處理隱藏選擇事件"""
        self.hide_selection()
