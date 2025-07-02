"""
卡牌管理器
管理卡牌的創建、選擇和應用
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
    """卡牌管理器"""
    
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager
        self.logger = logging.getLogger(__name__)
        
        # 所有可用的卡牌類型
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
        
        # 根據稀有度的權重
        self.rarity_weights = {
            CardRarity.COMMON: 50,
            CardRarity.RARE: 30,
            CardRarity.EPIC: 15,
            CardRarity.LEGENDARY: 5
        }
        
        # 玩家擁有的卡牌
        self.player_cards: Dict[int, List[CardBase]] = {}
        
        self.logger.info("卡牌管理器初始化完成")
    
    def create_card(self, card_id: str) -> Optional[CardBase]:
        """創建指定的卡牌"""
        if card_id in self.card_types:
            try:
                return self.card_types[card_id]()
            except Exception as e:
                self.logger.error(f"創建卡牌失敗 {card_id}: {e}")
                return None
        return None
    
    def get_random_cards(self, count: int = 3, exclude_cards: Optional[List[str]] = None) -> List[CardBase]:
        """獲取隨機卡牌選項"""
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
        
        # 根據稀有度排序（稀有的在前面）
        cards.sort(key=lambda c: list(self.rarity_weights.keys()).index(c.rarity))
        
        return cards
    
    def add_card_to_player(self, player_id: int, card: CardBase) -> bool:
        """將卡牌添加到玩家"""
        if player_id not in self.player_cards:
            self.player_cards[player_id] = []
        
        # 檢查是否已經有同樣的卡牌
        existing_card = self.find_player_card(player_id, card.card_id)
        
        if existing_card and existing_card.can_stack():
            # 疊加現有卡牌
            existing_card.add_stack()
            self.logger.info(f"玩家 {player_id} 疊加卡牌: {card.name} (層數: {existing_card.current_stacks})")
            return True
        elif not existing_card:
            # 添加新卡牌
            self.player_cards[player_id].append(card)
            card.current_stacks = 1
            self.logger.info(f"玩家 {player_id} 獲得新卡牌: {card.name}")
            return True
        else:
            # 不能疊加且已存在
            self.logger.warning(f"玩家 {player_id} 已擁有卡牌 {card.name} 且不能疊加")
            return False
    
    def find_player_card(self, player_id: int, card_id: str) -> Optional[CardBase]:
        """查找玩家的指定卡牌"""
        if player_id in self.player_cards:
            for card in self.player_cards[player_id]:
                if card.card_id == card_id:
                    return card
        return None
    
    def get_player_cards(self, player_id: int) -> List[CardBase]:
        """獲取玩家的所有卡牌"""
        return self.player_cards.get(player_id, [])
    
    def apply_card_to_player(self, player_id: int, card: CardBase, player_obj) -> bool:
        """應用卡牌效果到玩家對象"""
        try:
            card.apply_effect(player_obj)
            
            # 發送卡牌應用事件
            self.event_manager.emit(EventType.CARD_APPLY, {
                'player_id': player_id,
                'card': card.to_dict(),
                'player_cards_count': len(self.get_player_cards(player_id))
            })
            
            self.logger.info(f"卡牌效果已應用: {card.name} -> 玩家 {player_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"應用卡牌效果失敗: {card.name} -> 玩家 {player_id}, 錯誤: {e}")
            return False
    
    def remove_all_cards_from_player(self, player_id: int, player_obj) -> None:
        """移除玩家的所有卡牌效果"""
        cards = self.get_player_cards(player_id)
        for card in cards:
            try:
                card.remove_effect(player_obj)
            except Exception as e:
                self.logger.error(f"移除卡牌效果失敗: {card.name} -> 玩家 {player_id}, 錯誤: {e}")
        
        # 清空玩家卡牌列表
        if player_id in self.player_cards:
            del self.player_cards[player_id]
        
        self.logger.info(f"玩家 {player_id} 的所有卡牌效果已移除")
    
    def show_card_selection(self, player_id: int, cards: List[CardBase]) -> None:
        """顯示卡牌選擇界面"""
        card_data = [card.to_dict() for card in cards]
        
        self.event_manager.emit(EventType.CARD_SHOW_SELECTION, {
            'player_id': player_id,
            'cards': card_data
        })
        
        self.logger.info(f"顯示卡牌選擇界面 - 玩家 {player_id}, {len(cards)} 張卡牌")
    
    def hide_card_selection(self) -> None:
        """隱藏卡牌選擇界面"""
        self.event_manager.emit(EventType.CARD_HIDE_SELECTION, {})
    
    def get_weighted_random_cards(self, count: int = 3) -> List[CardBase]:
        """根據稀有度權重獲取隨機卡牌"""
        cards = []
        
        # 預先建立卡牌ID到稀有度的映射，避免重複創建臨時卡牌
        if not hasattr(self, '_card_rarity_map'):
            self._build_card_rarity_map()
        
        for _ in range(count):
            # 先隨機選擇稀有度
            rarity = self._get_random_rarity()
            
            # 獲取該稀有度的所有卡牌
            rarity_cards = [card_id for card_id, card_rarity in self._card_rarity_map.items() 
                           if card_rarity == rarity]
            
            if rarity_cards:
                card_id = random.choice(rarity_cards)
                card = self.create_card(card_id)
                if card:
                    cards.append(card)
        
        return cards
    
    def _build_card_rarity_map(self) -> None:
        """建立卡牌ID到稀有度的映射"""
        self._card_rarity_map = {}
        
        for card_id, card_type in self.card_types.items():
            try:
                temp_card = card_type()
                self._card_rarity_map[card_id] = temp_card.rarity
            except Exception as e:
                self.logger.warning(f"無法創建卡牌 {card_id} 來獲取稀有度: {e}")
                # 設定預設稀有度
                from .card_base import CardRarity
                self._card_rarity_map[card_id] = CardRarity.COMMON
    
    def _get_random_rarity(self) -> CardRarity:
        """根據權重隨機選擇稀有度"""
        rarities = list(self.rarity_weights.keys())
        weights = list(self.rarity_weights.values())
        
        return random.choices(rarities, weights=weights)[0]
    
    def get_card_statistics(self) -> Dict:
        """獲取卡牌統計信息"""
        total_cards = len(self.card_types)
        
        # 使用預建的稀有度映射
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
