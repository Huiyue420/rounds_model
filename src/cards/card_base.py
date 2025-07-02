"""
卡牌基礎類
定義卡牌的基礎結構和接口
"""

from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from enum import Enum


class CardType(Enum):
    """卡牌類型"""
    OFFENSIVE = "offensive"   # 攻擊型
    DEFENSIVE = "defensive"   # 防禦型
    UTILITY = "utility"       # 功能型
    MOVEMENT = "movement"     # 移動型


class CardRarity(Enum):
    """卡牌稀有度"""
    COMMON = "common"         # 普通（白色）
    RARE = "rare"            # 稀有（藍色）
    EPIC = "epic"            # 史詩（紫色）
    LEGENDARY = "legendary"   # 傳說（橙色）


class CardBase(ABC):
    """卡牌基礎抽象類"""
    
    def __init__(self, card_id: str, name: str, description: str, 
                 card_type: CardType, rarity: CardRarity):
        self.card_id = card_id
        self.name = name
        self.description = description
        self.card_type = card_type
        self.rarity = rarity
        self.is_stackable = False  # 是否可疊加
        self.max_stacks = 1        # 最大疊加層數
        self.current_stacks = 0    # 當前疊加層數
    
    @abstractmethod
    def apply_effect(self, player) -> None:
        """應用卡牌效果到玩家"""
        pass
    
    @abstractmethod
    def remove_effect(self, player) -> None:
        """從玩家身上移除卡牌效果"""
        pass
    
    def can_stack(self) -> bool:
        """檢查是否可以疊加"""
        return self.is_stackable and self.current_stacks < self.max_stacks
    
    def add_stack(self) -> bool:
        """增加疊加層數"""
        if self.can_stack():
            self.current_stacks += 1
            return True
        return False
    
    def get_color(self) -> tuple:
        """根據稀有度獲取顏色"""
        colors = {
            CardRarity.COMMON: (200, 200, 200),      # 灰色
            CardRarity.RARE: (100, 150, 255),        # 藍色
            CardRarity.EPIC: (150, 100, 255),        # 紫色
            CardRarity.LEGENDARY: (255, 200, 50)     # 橙色
        }
        return colors.get(self.rarity, (255, 255, 255))
    
    def get_icon(self) -> str:
        """獲取卡牌圖標"""
        icons = {
            CardType.OFFENSIVE: "⚔️",
            CardType.DEFENSIVE: "🛡️",
            CardType.UTILITY: "🔧",
            CardType.MOVEMENT: "👟"
        }
        return icons.get(self.card_type, "❓")
    
    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典格式"""
        return {
            'id': self.card_id,
            'name': self.name,
            'description': self.description,
            'type': self.card_type.value,
            'rarity': self.rarity.value,
            'icon': self.get_icon(),
            'color': self.get_color(),
            'stacks': self.current_stacks,
            'max_stacks': self.max_stacks
        }
