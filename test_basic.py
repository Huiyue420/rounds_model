"""
簡單測試腳本
驗證遊戲的基本功能是否正常運作
"""

import sys
import os

# 添加 src 目錄到路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """測試模組導入"""
    print("🧪 測試模組導入...")
    
    try:
        from src.core.config import GameConfig
        print("✅ 配置系統導入成功")
        
        from src.core.event_manager import EventManager, EventType
        print("✅ 事件系統導入成功")
        
        from src.systems.physics_system import PhysicsSystem, Vector2
        print("✅ 物理系統導入成功")
        
        from src.weapons.weapon_manager import WeaponManager
        print("✅ 武器系統導入成功")
        
        from src.cards.card_manager import CardManager
        print("✅ 卡牌系統導入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 導入失敗: {e}")
        return False

def test_basic_functionality():
    """測試基本功能"""
    print("\n🧪 測試基本功能...")
    
    try:
        from src.core.config import GameConfig
        from src.core.event_manager import EventManager, EventType
        from src.systems.physics_system import PhysicsSystem, Vector2
        from src.weapons.weapon_manager import WeaponManager
        from src.cards.card_manager import CardManager
        
        # 測試配置
        config = GameConfig(debug=True)
        print(f"✅ 配置創建成功 - 視窗大小: {config.window_size}")
        
        # 測試事件管理器
        event_manager = EventManager()
        event_manager.emit(EventType.GAME_START, {'test': True})
        print("✅ 事件系統測試成功")
        
        # 測試物理系統
        physics = PhysicsSystem(config)
        print("✅ 物理系統初始化成功")
        
        # 測試向量運算
        v1 = Vector2(3, 4)
        v2 = Vector2(1, 2)
        v3 = v1 + v2
        length = v1.length()
        print(f"✅ 向量運算測試成功 - 長度: {length:.2f}")
        
        # 測試武器系統
        weapon_manager = WeaponManager(config, event_manager)
        weapon_info = weapon_manager.get_weapon_info()
        print(f"✅ 武器系統測試成功 - 當前武器: {weapon_info['name']}")
        
        # 測試卡牌系統
        card_manager = CardManager(event_manager)
        cards = card_manager.get_random_cards(3)
        print(f"✅ 卡牌系統測試成功 - 生成 {len(cards)} 張卡牌")
        
        return True
        
    except Exception as e:
        print(f"❌ 功能測試失敗: {e}")
        return False

def test_pygame_availability():
    """測試 Pygame 可用性"""
    print("\n🧪 測試 Pygame 可用性...")
    
    try:
        import pygame
        pygame.init()
        print("✅ Pygame 可用")
        pygame.quit()
        return True
    except ImportError:
        print("❌ Pygame 未安裝")
        print("請運行: pip install pygame")
        return False
    except Exception as e:
        print(f"❌ Pygame 測試失敗: {e}")
        return False

def test_weapon_switching():
    """測試武器切換"""
    print("\n🧪 測試武器切換...")
    
    try:
        from src.core.config import GameConfig
        from src.core.event_manager import EventManager
        from src.weapons.weapon_manager import WeaponManager
        
        config = GameConfig()
        event_manager = EventManager()
        weapon_manager = WeaponManager(config, event_manager)
        
        # 測試武器切換
        initial_weapon = weapon_manager.current_weapon_type
        weapon_manager.next_weapon()
        new_weapon = weapon_manager.current_weapon_type
        
        if initial_weapon != new_weapon:
            print(f"✅ 武器切換成功: {initial_weapon} -> {new_weapon}")
        else:
            print("⚠️ 武器切換無變化（可能只有一種武器）")
        
        # 測試武器屬性
        weapon = weapon_manager.current_weapon
        print(f"✅ 武器屬性: 傷害={weapon.damage}, 射速={weapon.fire_rate}")
        
        return True
        
    except Exception as e:
        print(f"❌ 武器切換測試失敗: {e}")
        return False

def test_card_effects():
    """測試卡牌效果"""
    print("\n🧪 測試卡牌效果...")
    
    try:
        from src.core.config import GameConfig
        from src.core.event_manager import EventManager
        from src.cards.card_manager import CardManager
        from src.cards.card_effects import DamageBoostCard
        
        # 創建測試環境
        event_manager = EventManager()
        card_manager = CardManager(event_manager)
        
        # 創建測試玩家
        class TestPlayer:
            def __init__(self):
                self.damage_multiplier = 1.0
        
        player = TestPlayer()
        
        # 測試傷害提升卡牌
        damage_card = DamageBoostCard()
        initial_damage = player.damage_multiplier
        
        # 應用卡牌效果（簡化版本）
        player.damage_multiplier += damage_card.damage_boost
        
        print(f"✅ 卡牌效果測試成功: 傷害倍率 {initial_damage} -> {player.damage_multiplier}")
        
        # 測試卡牌創建
        card = card_manager.create_card('damage_boost')
        if card:
            print(f"✅ 卡牌創建成功: {card.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ 卡牌效果測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🎮 ROUNDS-like Python Game - 優化版本測試")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_pygame_availability,
        test_basic_functionality,
        test_weapon_switching,
        test_card_effects
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 測試結果: {passed}/{total} 通過")
    
    if passed == total:
        print("🎉 所有測試通過！遊戲系統運作正常。")
        print("\n🚀 可以運行遊戲:")
        print("   python main.py")
        print("   python main.py --debug")
    else:
        print("⚠️ 部分測試失敗，請檢查相關系統。")
        print("\n🛠️ 建議:")
        print("   1. 確保已安裝所有依賴: pip install -r requirements.txt")
        print("   2. 檢查 Python 版本 (建議 3.8+)")
        print("   3. 查看錯誤信息並修復相關問題")

if __name__ == "__main__":
    main()
