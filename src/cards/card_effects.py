"""
具體卡牌效果實現
定義各種卡牌的具體效果
"""

from .card_base import CardBase, CardType, CardRarity


class DamageBoostCard(CardBase):
    """傷害提升卡牌"""
    
    def __init__(self):
        super().__init__(
            card_id="damage_boost",
            name="傷害強化",
            description="武器傷害增加 25%",
            card_type=CardType.OFFENSIVE,
            rarity=CardRarity.COMMON
        )
        self.is_stackable = True
        self.max_stacks = 3
        self.damage_boost = 0.25
    
    def apply_effect(self, player) -> None:
        """應用傷害提升效果"""
        if hasattr(player, 'weapon_manager'):
            player.weapon_manager.apply_card_effect('damage_boost', self.damage_boost)
        self.current_stacks += 1
    
    def remove_effect(self, player) -> None:
        """移除傷害提升效果"""
        if hasattr(player, 'weapon_manager'):
            player.weapon_manager.apply_card_effect('damage_boost', -self.damage_boost * self.current_stacks)
        self.current_stacks = 0


class FireRateBoostCard(CardBase):
    """射速提升卡牌"""
    
    def __init__(self):
        super().__init__(
            card_id="fire_rate_boost",
            name="快速射擊",
            description="射擊速度增加 50%",
            card_type=CardType.OFFENSIVE,
            rarity=CardRarity.RARE
        )
        self.fire_rate_boost = 0.5
    
    def apply_effect(self, player) -> None:
        """應用射速提升效果"""
        if hasattr(player, 'weapon_manager'):
            player.weapon_manager.apply_card_effect('fire_rate_boost', self.fire_rate_boost)
        self.current_stacks = 1
    
    def remove_effect(self, player) -> None:
        """移除射速提升效果"""
        if hasattr(player, 'weapon_manager'):
            player.weapon_manager.apply_card_effect('fire_rate_boost', -self.fire_rate_boost)
        self.current_stacks = 0


class LargeMagazineCard(CardBase):
    """大型彈匣卡牌"""
    
    def __init__(self):
        super().__init__(
            card_id="large_magazine",
            name="大型彈匣",
            description="彈匣容量增加 50%",
            card_type=CardType.UTILITY,
            rarity=CardRarity.COMMON
        )
        self.is_stackable = True
        self.max_stacks = 2
        self.magazine_boost = 0.5
    
    def apply_effect(self, player) -> None:
        """應用彈匣容量提升效果"""
        if hasattr(player, 'weapon_manager'):
            # 計算增加的彈匣容量
            for weapon in player.weapon_manager.weapons.values():
                bonus = int(weapon.magazine_size * self.magazine_boost)
                weapon.magazine_size_bonus += bonus
        self.current_stacks += 1
    
    def remove_effect(self, player) -> None:
        """移除彈匣容量提升效果"""
        if hasattr(player, 'weapon_manager'):
            for weapon in player.weapon_manager.weapons.values():
                bonus = int(weapon.magazine_size * self.magazine_boost) * self.current_stacks
                weapon.magazine_size_bonus -= bonus
        self.current_stacks = 0


class ArmorCard(CardBase):
    """護甲卡牌"""
    
    def __init__(self):
        super().__init__(
            card_id="armor",
            name="護甲",
            description="減少 20% 受到的傷害",
            card_type=CardType.DEFENSIVE,
            rarity=CardRarity.COMMON
        )
        self.is_stackable = True
        self.max_stacks = 3
        self.damage_reduction = 0.20
    
    def apply_effect(self, player) -> None:
        """應用護甲效果"""
        if hasattr(player, 'damage_reduction'):
            player.damage_reduction += self.damage_reduction
        else:
            player.damage_reduction = self.damage_reduction
        self.current_stacks += 1
    
    def remove_effect(self, player) -> None:
        """移除護甲效果"""
        if hasattr(player, 'damage_reduction'):
            player.damage_reduction -= self.damage_reduction * self.current_stacks
        self.current_stacks = 0


class FastHealingCard(CardBase):
    """快速治療卡牌"""
    
    def __init__(self):
        super().__init__(
            card_id="fast_healing",
            name="快速治療",
            description="每秒恢復 5 HP",
            card_type=CardType.DEFENSIVE,
            rarity=CardRarity.RARE
        )
        self.healing_rate = 5.0
    
    def apply_effect(self, player) -> None:
        """應用快速治療效果"""
        if hasattr(player, 'healing_rate'):
            player.healing_rate += self.healing_rate
        else:
            player.healing_rate = self.healing_rate
        self.current_stacks = 1
    
    def remove_effect(self, player) -> None:
        """移除快速治療效果"""
        if hasattr(player, 'healing_rate'):
            player.healing_rate -= self.healing_rate
        self.current_stacks = 0


class ExtraHealthCard(CardBase):
    """額外生命卡牌"""
    
    def __init__(self):
        super().__init__(
            card_id="extra_health",
            name="額外生命",
            description="最大 HP +50",
            card_type=CardType.DEFENSIVE,
            rarity=CardRarity.EPIC
        )
        self.is_stackable = True
        self.max_stacks = 2
        self.health_bonus = 50
    
    def apply_effect(self, player) -> None:
        """應用額外生命效果"""
        player.max_health += self.health_bonus
        player.health += self.health_bonus  # 同時增加當前血量
        self.current_stacks += 1
    
    def remove_effect(self, player) -> None:
        """移除額外生命效果"""
        total_bonus = self.health_bonus * self.current_stacks
        player.max_health -= total_bonus
        player.health = min(player.health, player.max_health)
        self.current_stacks = 0


class SpeedBoostCard(CardBase):
    """速度提升卡牌"""
    
    def __init__(self):
        super().__init__(
            card_id="speed_boost",
            name="速度提升",
            description="移動速度增加 30%",
            card_type=CardType.MOVEMENT,
            rarity=CardRarity.COMMON
        )
        self.is_stackable = True
        self.max_stacks = 2
        self.speed_multiplier = 0.30
    
    def apply_effect(self, player) -> None:
        """應用速度提升效果"""
        if hasattr(player, 'speed_multiplier'):
            player.speed_multiplier += self.speed_multiplier
        else:
            player.speed_multiplier = 1.0 + self.speed_multiplier
        self.current_stacks += 1
    
    def remove_effect(self, player) -> None:
        """移除速度提升效果"""
        if hasattr(player, 'speed_multiplier'):
            player.speed_multiplier -= self.speed_multiplier * self.current_stacks
        self.current_stacks = 0


class DoubleJumpCard(CardBase):
    """二段跳卡牌"""
    
    def __init__(self):
        super().__init__(
            card_id="double_jump",
            name="二段跳",
            description="可以在空中再次跳躍",
            card_type=CardType.MOVEMENT,
            rarity=CardRarity.EPIC
        )
    
    def apply_effect(self, player) -> None:
        """應用二段跳效果"""
        if hasattr(player, 'max_jumps'):
            player.max_jumps = 2
        self.current_stacks = 1
    
    def remove_effect(self, player) -> None:
        """移除二段跳效果"""
        if hasattr(player, 'max_jumps'):
            player.max_jumps = 1
        self.current_stacks = 0


class HighJumpCard(CardBase):
    """高跳卡牌"""
    
    def __init__(self):
        super().__init__(
            card_id="high_jump",
            name="高跳",
            description="跳躍力增加 40%",
            card_type=CardType.MOVEMENT,
            rarity=CardRarity.RARE
        )
        self.jump_boost = 0.40
    
    def apply_effect(self, player) -> None:
        """應用高跳效果"""
        if hasattr(player, 'jump_force_multiplier'):
            player.jump_force_multiplier += self.jump_boost
        else:
            player.jump_force_multiplier = 1.0 + self.jump_boost
        self.current_stacks = 1
    
    def remove_effect(self, player) -> None:
        """移除高跳效果"""
        if hasattr(player, 'jump_force_multiplier'):
            player.jump_force_multiplier -= self.jump_boost
        self.current_stacks = 0


class ReloadSpeedCard(CardBase):
    """換彈加速卡牌"""
    
    def __init__(self):
        super().__init__(
            card_id="reload_speed",
            name="換彈加速",
            description="重裝時間減少 50%",
            card_type=CardType.UTILITY,
            rarity=CardRarity.RARE
        )
        self.reload_speed_boost = 0.50
    
    def apply_effect(self, player) -> None:
        """應用換彈加速效果"""
        if hasattr(player, 'weapon_manager'):
            player.weapon_manager.apply_card_effect('reload_speed_boost', self.reload_speed_boost)
        self.current_stacks = 1
    
    def remove_effect(self, player) -> None:
        """移除換彈加速效果"""
        if hasattr(player, 'weapon_manager'):
            # 還原效果需要計算反向操作
            for weapon in player.weapon_manager.weapons.values():
                weapon.reload_time_multiplier /= (1 - self.reload_speed_boost)
        self.current_stacks = 0


class BigBulletsCard(CardBase):
    """大型子彈卡牌"""
    
    def __init__(self):
        super().__init__(
            card_id="big_bullets",
            name="大型子彈",
            description="子彈尺寸增加 50%",
            card_type=CardType.OFFENSIVE,
            rarity=CardRarity.EPIC
        )
        self.bullet_size_boost = 0.50
    
    def apply_effect(self, player) -> None:
        """應用大型子彈效果"""
        if hasattr(player, 'weapon_manager'):
            player.weapon_manager.apply_card_effect('bullet_size_boost', self.bullet_size_boost)
        self.current_stacks = 1
    
    def remove_effect(self, player) -> None:
        """移除大型子彈效果"""
        if hasattr(player, 'weapon_manager'):
            player.weapon_manager.apply_card_effect('bullet_size_boost', -self.bullet_size_boost)
        self.current_stacks = 0
