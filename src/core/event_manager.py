"""
事件管理系統 - 優化版本
處理遊戲中的事件分發和處理，新增卡牌和武器相關事件
"""

from typing import Dict, List, Callable, Any, Optional
from enum import Enum
import logging


class EventType(Enum):
    """事件類型枚舉 - 優化版本"""
    # 玩家事件
    PLAYER_MOVE = "player_move"
    PLAYER_JUMP = "player_jump"
    PLAYER_SHOOT = "player_shoot"
    PLAYER_RELOAD = "player_reload"
    PLAYER_DEATH = "player_death"
    PLAYER_RESPAWN = "player_respawn"
    
    # 武器事件
    WEAPON_SWITCH = "weapon_switch"
    WEAPON_FIRE = "weapon_fire"
    WEAPON_SHOOT = "weapon_shoot"  # 射擊事件
    WEAPON_RELOAD_START = "weapon_reload_start"
    WEAPON_RELOAD_COMPLETE = "weapon_reload_complete"
    
    # 子彈事件
    BULLET_HIT = "bullet_hit"
    BULLET_CREATE = "bullet_create"
    BULLET_DESTROY = "bullet_destroy"
    
    # 卡牌事件
    CARD_SELECT = "card_select"
    CARD_APPLY = "card_apply"
    CARD_SHOW_SELECTION = "card_show_selection"
    CARD_HIDE_SELECTION = "card_hide_selection"
    
    # 假人事件
    DUMMY_SPAWN = "dummy_spawn"
    DUMMY_DAMAGE = "dummy_damage"
    DUMMY_DEATH = "dummy_death"
    DUMMY_RESPAWN = "dummy_respawn"
    
    # 遊戲事件
    GAME_START = "game_start"
    GAME_END = "game_end"
    GAME_PAUSE = "game_pause"
    GAME_RESUME = "game_resume"
    
    # UI 事件
    UI_UPDATE_HEALTH = "ui_update_health"
    UI_UPDATE_AMMO = "ui_update_ammo"
    UI_UPDATE_WEAPON = "ui_update_weapon"
    
    # 音效事件
    SOUND_PLAY = "sound_play"
    SOUND_STOP = "sound_stop"


class Event:
    """事件類 - 優化版本"""
    
    def __init__(self, event_type: EventType, data: Optional[Dict[str, Any]] = None, 
                 sender: Optional[Any] = None):
        self.type = event_type
        self.data = data or {}
        self.sender = sender
        self.handled = False
        self.timestamp = None  # 可以添加時間戳
    
    def mark_handled(self) -> None:
        """標記事件已處理"""
        self.handled = True
    
    def get_data(self, key: str, default: Any = None) -> Any:
        """安全獲取事件數據"""
        return self.data.get(key, default)


class EventManager:
    """事件管理器 - 優化版本"""
    
    def __init__(self):
        self.listeners: Dict[EventType, List[Callable]] = {}
        self.event_queue: List[Event] = []
        self.logger = logging.getLogger(__name__)
        self.enabled = True
    
    def subscribe(self, event_type: EventType, callback: Callable[[Event], None]) -> None:
        """訂閱事件"""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        
        if callback not in self.listeners[event_type]:
            self.listeners[event_type].append(callback)
            self.logger.debug(f"已訂閱事件: {event_type.value}")
    
    def unsubscribe(self, event_type: EventType, callback: Callable[[Event], None]) -> None:
        """取消訂閱事件"""
        if event_type in self.listeners and callback in self.listeners[event_type]:
            self.listeners[event_type].remove(callback)
            self.logger.debug(f"已取消訂閱事件: {event_type.value}")
    
    def emit(self, event_type: EventType, data: Optional[Dict[str, Any]] = None, 
             sender: Optional[Any] = None, immediate: bool = False) -> None:
        """發送事件"""
        if not self.enabled:
            return
        
        event = Event(event_type, data, sender)
        
        if immediate:
            self._dispatch_event(event)
        else:
            self.event_queue.append(event)
        
        self.logger.debug(f"事件已發送: {event_type.value}")
    
    def process_events(self) -> None:
        """處理事件隊列"""
        if not self.enabled:
            return
        
        # 複製隊列以避免在處理過程中修改
        events_to_process = self.event_queue.copy()
        self.event_queue.clear()
        
        for event in events_to_process:
            self._dispatch_event(event)
    
    def _dispatch_event(self, event: Event) -> None:
        """分發事件到監聽器"""
        if event.type in self.listeners:
            for listener in self.listeners[event.type]:
                try:
                    listener(event)
                    if event.handled:
                        break  # 如果事件被標記為已處理，停止傳播
                except Exception as e:
                    self.logger.error(f"事件處理錯誤 {event.type.value}: {e}")
    
    def clear_queue(self) -> None:
        """清空事件隊列"""
        self.event_queue.clear()
    
    def disable(self) -> None:
        """禁用事件系統"""
        self.enabled = False
    
    def enable(self) -> None:
        """啟用事件系統"""
        self.enabled = True
