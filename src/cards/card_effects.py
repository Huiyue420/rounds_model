"""
Specific card effect implementations
Defines the specific effects of various cards
"""

from .card_base import CardBase, CardType, CardRarity


class DamageBoostCard(CardBase):
    """Damage boost card"""
    
    def __init__(self):
        super().__init__(
            card_id="damage_boost",
            name="Damage Enhancement",
            description="Weapon damage increased by 25%",
            card_type=CardType.OFFENSIVE,
            rarity=CardRarity.COMMON
        )
        self.is_stackable = True
        self.max_stacks = 3
        self.damage_boost = 0.25
    
    def apply_effect(self, player) -> None:
        """Apply damage boost effect"""
        if hasattr(player, 'weapon_manager'):
            player.weapon_manager.apply_card_effect('damage_boost', self.damage_boost)
        self.current_stacks += 1
    
    def remove_effect(self, player) -> None:
        """Remove damage boost effect"""
        if hasattr(player, 'weapon_manager'):
            player.weapon_manager.apply_card_effect('damage_boost', -self.damage_boost * self.current_stacks)
        self.current_stacks = 0


class FireRateBoostCard(CardBase):
    """Fire rate boost card"""
    
    def __init__(self):
        super().__init__(
            card_id="fire_rate_boost",
            name="Rapid Fire",
            description="Fire rate increased by 50%",
            card_type=CardType.OFFENSIVE,
            rarity=CardRarity.RARE
        )
        self.fire_rate_boost = 0.5
    
    def apply_effect(self, player) -> None:
        """Apply fire rate boost effect"""
        if hasattr(player, 'weapon_manager'):
            player.weapon_manager.apply_card_effect('fire_rate_boost', self.fire_rate_boost)
        self.current_stacks = 1
    
    def remove_effect(self, player) -> None:
        """Remove fire rate boost effect"""
        if hasattr(player, 'weapon_manager'):
            player.weapon_manager.apply_card_effect('fire_rate_boost', -self.fire_rate_boost)
        self.current_stacks = 0


class LargeMagazineCard(CardBase):
    """Large magazine card"""
    
    def __init__(self):
        super().__init__(
            card_id="large_magazine",
            name="Large Magazine",
            description="Magazine capacity increased by 50%",
            card_type=CardType.UTILITY,
            rarity=CardRarity.COMMON
        )
        self.is_stackable = True
        self.max_stacks = 2
        self.magazine_boost = 0.5
    
    def apply_effect(self, player) -> None:
        """Apply magazine capacity boost effect"""
        if hasattr(player, 'weapon_manager'):
            # Calculate increased magazine capacity
            for weapon in player.weapon_manager.weapons.values():
                bonus = int(weapon.magazine_size * self.magazine_boost)
                weapon.magazine_size_bonus += bonus
        self.current_stacks += 1
    
    def remove_effect(self, player) -> None:
        """Remove magazine capacity boost effect"""
        if hasattr(player, 'weapon_manager'):
            for weapon in player.weapon_manager.weapons.values():
                bonus = int(weapon.magazine_size * self.magazine_boost) * self.current_stacks
                weapon.magazine_size_bonus -= bonus
        self.current_stacks = 0


class ArmorCard(CardBase):
    """Armor card"""
    
    def __init__(self):
        super().__init__(
            card_id="armor",
            name="Armor",
            description="Reduce 20% damage taken",
            card_type=CardType.DEFENSIVE,
            rarity=CardRarity.COMMON
        )
        self.is_stackable = True
        self.max_stacks = 3
        self.damage_reduction = 0.20
    
    def apply_effect(self, player) -> None:
        """Apply armor effect"""
        if hasattr(player, 'damage_reduction'):
            player.damage_reduction += self.damage_reduction
        else:
            player.damage_reduction = self.damage_reduction
        self.current_stacks += 1
    
    def remove_effect(self, player) -> None:
        """Remove armor effect"""
        if hasattr(player, 'damage_reduction'):
            player.damage_reduction -= self.damage_reduction * self.current_stacks
        self.current_stacks = 0


class FastHealingCard(CardBase):
    """Fast healing card"""
    
    def __init__(self):
        super().__init__(
            card_id="fast_healing",
            name="Fast Healing",
            description="Recover 5 HP per second",
            card_type=CardType.DEFENSIVE,
            rarity=CardRarity.RARE
        )
        self.healing_rate = 5.0
    
    def apply_effect(self, player) -> None:
        """Apply fast healing effect"""
        if hasattr(player, 'healing_rate'):
            player.healing_rate += self.healing_rate
        else:
            player.healing_rate = self.healing_rate
        self.current_stacks = 1
    
    def remove_effect(self, player) -> None:
        """Remove fast healing effect"""
        if hasattr(player, 'healing_rate'):
            player.healing_rate -= self.healing_rate
        self.current_stacks = 0


class ExtraHealthCard(CardBase):
    """Extra health card"""
    
    def __init__(self):
        super().__init__(
            card_id="extra_health",
            name="Extra Health",
            description="Max HP +50",
            card_type=CardType.DEFENSIVE,
            rarity=CardRarity.EPIC
        )
        self.is_stackable = True
        self.max_stacks = 2
        self.health_bonus = 50
    
    def apply_effect(self, player) -> None:
        """Apply extra health effect"""
        player.max_health += self.health_bonus
        player.health += self.health_bonus  # Also increase current health
        self.current_stacks += 1
    
    def remove_effect(self, player) -> None:
        """Remove extra health effect"""
        total_bonus = self.health_bonus * self.current_stacks
        player.max_health -= total_bonus
        player.health = min(player.health, player.max_health)
        self.current_stacks = 0


class SpeedBoostCard(CardBase):
    """Speed boost card"""
    
    def __init__(self):
        super().__init__(
            card_id="speed_boost",
            name="Speed Boost",
            description="Movement speed increased by 30%",
            card_type=CardType.MOVEMENT,
            rarity=CardRarity.COMMON
        )
        self.is_stackable = True
        self.max_stacks = 2
        self.speed_multiplier = 0.30
    
    def apply_effect(self, player) -> None:
        """Apply speed boost effect"""
        if hasattr(player, 'speed_multiplier'):
            player.speed_multiplier += self.speed_multiplier
        else:
            player.speed_multiplier = 1.0 + self.speed_multiplier
        self.current_stacks += 1
    
    def remove_effect(self, player) -> None:
        """Remove speed boost effect"""
        if hasattr(player, 'speed_multiplier'):
            player.speed_multiplier -= self.speed_multiplier * self.current_stacks
        self.current_stacks = 0


class DoubleJumpCard(CardBase):
    """Double jump card"""
    
    def __init__(self):
        super().__init__(
            card_id="double_jump",
            name="Double Jump",
            description="Can jump again in mid-air",
            card_type=CardType.MOVEMENT,
            rarity=CardRarity.EPIC
        )
    
    def apply_effect(self, player) -> None:
        """Apply double jump effect"""
        if hasattr(player, 'max_jumps'):
            player.max_jumps = 2
        self.current_stacks = 1
    
    def remove_effect(self, player) -> None:
        """Remove double jump effect"""
        if hasattr(player, 'max_jumps'):
            player.max_jumps = 1
        self.current_stacks = 0


class HighJumpCard(CardBase):
    """High jump card"""
    
    def __init__(self):
        super().__init__(
            card_id="high_jump",
            name="High Jump",
            description="Jump force increased by 40%",
            card_type=CardType.MOVEMENT,
            rarity=CardRarity.RARE
        )
        self.jump_boost = 0.40
    
    def apply_effect(self, player) -> None:
        """Apply high jump effect"""
        if hasattr(player, 'jump_force_multiplier'):
            player.jump_force_multiplier += self.jump_boost
        else:
            player.jump_force_multiplier = 1.0 + self.jump_boost
        self.current_stacks = 1
    
    def remove_effect(self, player) -> None:
        """Remove high jump effect"""
        if hasattr(player, 'jump_force_multiplier'):
            player.jump_force_multiplier -= self.jump_boost
        self.current_stacks = 0


class ReloadSpeedCard(CardBase):
    """Reload speed card"""
    
    def __init__(self):
        super().__init__(
            card_id="reload_speed",
            name="Reload Speed",
            description="Reload time reduced by 50%",
            card_type=CardType.UTILITY,
            rarity=CardRarity.RARE
        )
        self.reload_speed_boost = 0.50
    
    def apply_effect(self, player) -> None:
        """Apply reload speed effect"""
        if hasattr(player, 'weapon_manager'):
            player.weapon_manager.apply_card_effect('reload_speed_boost', self.reload_speed_boost)
        self.current_stacks = 1
    
    def remove_effect(self, player) -> None:
        """Remove reload speed effect"""
        if hasattr(player, 'weapon_manager'):
            # Reversing effect requires inverse calculation
            for weapon in player.weapon_manager.weapons.values():
                weapon.reload_time_multiplier /= (1 - self.reload_speed_boost)
        self.current_stacks = 0


class BigBulletsCard(CardBase):
    """Big bullets card"""
    
    def __init__(self):
        super().__init__(
            card_id="big_bullets",
            name="Big Bullets",
            description="Bullet size increased by 50%",
            card_type=CardType.OFFENSIVE,
            rarity=CardRarity.EPIC
        )
        self.bullet_size_boost = 0.50
    
    def apply_effect(self, player) -> None:
        """Apply big bullets effect"""
        if hasattr(player, 'weapon_manager'):
            player.weapon_manager.apply_card_effect('bullet_size_boost', self.bullet_size_boost)
        self.current_stacks = 1
    
    def remove_effect(self, player) -> None:
        """Remove big bullets effect"""
        if hasattr(player, 'weapon_manager'):
            player.weapon_manager.apply_card_effect('bullet_size_boost', -self.bullet_size_boost)
        self.current_stacks = 0
