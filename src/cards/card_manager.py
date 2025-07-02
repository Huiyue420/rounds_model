"""
Card Manager
Manages card creation, selection and application
"""

import random
from typing import List, Dict, Optional, Type
import logging

from .card_base import CardBase, CardRarity
from .card_effects import (
    DamageBoostCard, FireRateBoostCard, LargeMagazineCard,
    ArmorCard, FastHealingCard, ExtraHealthCard,
    SpeedBoostCard, DoubleJumpCard, HighJumpCard,
    ReloadSpeedCard, BigBulletsCard
)
from ..core.event_manager import EventManager, EventType


class CardManager:
    """Card manager"""
    
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager
        self.logger = logging.getLogger(__name__)
        
        # All available card types
        self.card_types: Dict[str, Type[CardBase]] = {
            'damage_boost': DamageBoostCard,
            'fire_rate_boost': FireRateBoostCard,
            'large_magazine': LargeMagazineCard,
            'armor': ArmorCard,
            'fast_healing': FastHealingCard,
            'extra_health': ExtraHealthCard,
            'speed_boost': SpeedBoostCard,
            'double_jump': DoubleJumpCard,
            'high_jump': HighJumpCard,
            'reload_speed': ReloadSpeedCard,
            'big_bullets': BigBulletsCard
        }
        
        # Weights based on rarity
        self.rarity_weights = {
            CardRarity.COMMON: 50,
            CardRarity.RARE: 30,
            CardRarity.EPIC: 15,
            CardRarity.LEGENDARY: 5
        }
        
        # Cards owned by players
        self.player_cards: Dict[int, List[CardBase]] = {}
        
        self.logger.info("Card manager initialization completed")
    
    def create_card(self, card_id: str) -> Optional[CardBase]:
        """Create specified card"""
        if card_id in self.card_types:
            try:
                return self.card_types[card_id]()
            except Exception as e:
                self.logger.error(f"Failed to create card {card_id}: {e}")
                return None
        return None
    
    def get_random_cards(self, count: int = 3, exclude_cards: Optional[List[str]] = None) -> List[CardBase]:
        """Get random card options"""
        if exclude_cards is None:
            exclude_cards = []
        
        available_cards = [card_id for card_id in self.card_types.keys() 
                          if card_id not in exclude_cards]
        
        if len(available_cards) < count:
            count = len(available_cards)
        
        selected_card_ids = random.sample(available_cards, count)
        cards = []
        
        for card_id in selected_card_ids:
            card = self.create_card(card_id)
            if card:
                cards.append(card)
        
        # Sort by rarity (rare ones first)
        cards.sort(key=lambda c: list(self.rarity_weights.keys()).index(c.rarity))
        
        return cards
    
    def add_card_to_player(self, player_id: int, card: CardBase) -> bool:
        """Add card to player"""
        if player_id not in self.player_cards:
            self.player_cards[player_id] = []
        
        # Check if the same card already exists
        existing_card = self.find_player_card(player_id, card.card_id)
        
        if existing_card and existing_card.can_stack():
            # Stack existing card
            existing_card.add_stack()
            self.logger.info(f"Player {player_id} stacked card: {card.name} (stacks: {existing_card.current_stacks})")
            return True
        elif not existing_card:
            # Add new card
            self.player_cards[player_id].append(card)
            card.current_stacks = 1
            self.logger.info(f"Player {player_id} received new card: {card.name}")
            return True
        else:
            # Cannot stack and already exists
            self.logger.warning(f"Player {player_id} already owns card {card.name} and cannot stack")
            return False
    
    def find_player_card(self, player_id: int, card_id: str) -> Optional[CardBase]:
        """Find player's specified card"""
        if player_id in self.player_cards:
            for card in self.player_cards[player_id]:
                if card.card_id == card_id:
                    return card
        return None
    
    def get_player_cards(self, player_id: int) -> List[CardBase]:
        """Get all cards of player"""
        return self.player_cards.get(player_id, [])
    
    def apply_card_to_player(self, player_id: int, card: CardBase, player_obj) -> bool:
        """Apply card effect to player object"""
        try:
            card.apply_effect(player_obj)
            
            # Send card apply event
            self.event_manager.emit(EventType.CARD_APPLY, {
                'player_id': player_id,
                'card': card.to_dict(),
                'player_cards_count': len(self.get_player_cards(player_id))
            })
            
            self.logger.info(f"Card effect applied: {card.name} -> Player {player_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to apply card effect: {card.name} -> Player {player_id}, Error: {e}")
            return False
    
    def remove_all_cards_from_player(self, player_id: int, player_obj) -> None:
        """Remove all card effects from player"""
        cards = self.get_player_cards(player_id)
        for card in cards:
            try:
                card.remove_effect(player_obj)
            except Exception as e:
                self.logger.error(f"Failed to remove card effect: {card.name} -> Player {player_id}, Error: {e}")
        
        # Clear player card list
        if player_id in self.player_cards:
            del self.player_cards[player_id]
        
        self.logger.info(f"All card effects removed from player {player_id}")
    
    def show_card_selection(self, player_id: int, cards: List[CardBase]) -> None:
        """Show card selection interface"""
        card_data = [card.to_dict() for card in cards]
        
        self.event_manager.emit(EventType.CARD_SHOW_SELECTION, {
            'player_id': player_id,
            'cards': card_data
        })
        
        self.logger.info(f"Show card selection interface - Player {player_id}, {len(cards)} cards")
    
    def hide_card_selection(self) -> None:
        """Hide card selection interface"""
        self.event_manager.emit(EventType.CARD_HIDE_SELECTION, {})
    
    def get_weighted_random_cards(self, count: int = 3) -> List[CardBase]:
        """Get random cards based on rarity weights"""
        cards = []
        
        # Pre-build card ID to rarity mapping to avoid repeatedly creating temporary cards
        if not hasattr(self, '_card_rarity_map'):
            self._build_card_rarity_map()
        
        for _ in range(count):
            # First randomly select rarity
            rarity = self._get_random_rarity()
            
            # Get all cards of that rarity
            rarity_cards = [card_id for card_id, card_rarity in self._card_rarity_map.items() 
                           if card_rarity == rarity]
            
            if rarity_cards:
                card_id = random.choice(rarity_cards)
                card = self.create_card(card_id)
                if card:
                    cards.append(card)
        
        return cards
    
    def _build_card_rarity_map(self) -> None:
        """Build mapping from card ID to rarity"""
        self._card_rarity_map = {}
        
        for card_id, card_type in self.card_types.items():
            try:
                temp_card = card_type()
                self._card_rarity_map[card_id] = temp_card.rarity
            except Exception as e:
                self.logger.warning(f"Cannot create card {card_id} to get rarity: {e}")
                # Set default rarity
                from .card_base import CardRarity
                self._card_rarity_map[card_id] = CardRarity.COMMON
    
    def _get_random_rarity(self) -> CardRarity:
        """Randomly select rarity based on weights"""
        rarities = list(self.rarity_weights.keys())
        weights = list(self.rarity_weights.values())
        
        return random.choices(rarities, weights=weights)[0]
    
    def get_card_statistics(self) -> Dict:
        """Get card statistics"""
        total_cards = len(self.card_types)
        
        # Use pre-built rarity mapping
        if not hasattr(self, '_card_rarity_map'):
            self._build_card_rarity_map()
        
        rarity_counts = {}
        for card_id, rarity in self._card_rarity_map.items():
            rarity_counts[rarity.value] = rarity_counts.get(rarity.value, 0) + 1
        
        return {
            'total_cards': total_cards,
            'rarity_distribution': rarity_counts,
            'active_players': len(self.player_cards)
        }
