"""
Card Base Class
Defines the basic structure and interface for cards
"""

from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from enum import Enum


class CardType(Enum):
    """Card type"""
    OFFENSIVE = "offensive"   # Attack type
    DEFENSIVE = "defensive"   # Defense type
    UTILITY = "utility"       # Utility type
    MOVEMENT = "movement"     # Movement type


class CardRarity(Enum):
    """Card rarity"""
    COMMON = "common"         # Common (white)
    RARE = "rare"            # Rare (blue)
    EPIC = "epic"            # Epic (purple)
    LEGENDARY = "legendary"   # Legendary (orange)


class CardBase(ABC):
    """Card base abstract class"""
    
    def __init__(self, card_id: str, name: str, description: str, 
                 card_type: CardType, rarity: CardRarity):
        self.card_id = card_id
        self.name = name
        self.description = description
        self.card_type = card_type
        self.rarity = rarity
        self.is_stackable = False  # Whether it can be stacked
        self.max_stacks = 1        # Maximum stack count
        self.current_stacks = 0    # Current stack count
    
    @abstractmethod
    def apply_effect(self, player) -> None:
        """Apply card effect to player"""
        pass
    
    @abstractmethod
    def remove_effect(self, player) -> None:
        """Remove card effect from player"""
        pass
    
    def can_stack(self) -> bool:
        """Check if card can be stacked"""
        return self.is_stackable and self.current_stacks < self.max_stacks
    
    def add_stack(self) -> bool:
        """Add stack count"""
        if self.can_stack():
            self.current_stacks += 1
            return True
        return False
    
    def get_color(self) -> tuple:
        """Get color based on rarity"""
        colors = {
            CardRarity.COMMON: (200, 200, 200),      # Gray
            CardRarity.RARE: (100, 150, 255),        # Blue
            CardRarity.EPIC: (150, 100, 255),        # Purple
            CardRarity.LEGENDARY: (255, 200, 50)     # Orange
        }
        return colors.get(self.rarity, (255, 255, 255))
    
    def get_icon(self) -> str:
        """Get card icon"""
        icons = {
            CardType.OFFENSIVE: "⚔️",
            CardType.DEFENSIVE: "🛡️",
            CardType.UTILITY: "🔧",
            CardType.MOVEMENT: "👟"
        }
        return icons.get(self.card_type, "❓")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
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
