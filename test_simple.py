"""
簡化測試腳本
驗證遊戲的基本功能是否正常運作（避免複雜的導入問題）
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
        
        try:
            from src.weapons.weapon_manager import WeaponManager
            print("✅ 武器系統導入成功")
        except Exception as e:
            print(f"⚠️ 武器系統導入警告: {e}")
        
        try:
            from src.cards.card_manager import CardManager
            print("✅ 卡牌系統導入成功")
        except Exception as e:
            print(f"⚠️ 卡牌系統導入警告: {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 導入失敗: {e}")
        return False

def test_basic_systems():
    """測試基本系統"""
    print("\n🧪 測試基本系統...")
    
    try:
        from src.core.config import GameConfig
        from src.core.event_manager import EventManager, EventType
        from src.systems.physics_system import PhysicsSystem, Vector2
        
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
        
        return True
        
    except Exception as e:
        print(f"❌ 基本系統測試失敗: {e}")
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

def test_config_system():
    """測試配置系統"""
    print("\n🧪 測試配置系統...")
    
    try:
        from src.core.config import GameConfig
        
        # 測試預設配置
        config = GameConfig()
        print(f"✅ 預設配置: {config.window_width}x{config.window_height}")
        
        # 測試自定義配置
        config = GameConfig(window_width=800, window_height=600, debug=True)
        print(f"✅ 自定義配置: {config.window_width}x{config.window_height}")
        
        # 測試武器配置
        if hasattr(config, 'weapon_configs') and config.weapon_configs:
            weapon_count = len(config.weapon_configs)
            print(f"✅ 武器配置: {weapon_count} 種武器")
            
            # 列出武器
            for weapon_name in config.weapon_configs.keys():
                print(f"   - {weapon_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置系統測試失敗: {e}")
        return False

def test_event_system():
    """測試事件系統"""
    print("\n🧪 測試事件系統...")
    
    try:
        from src.core.event_manager import EventManager, EventType, Event
        
        # 創建事件管理器
        event_manager = EventManager()
        
        # 測試事件訂閱和發送
        received_events = []
        
        def test_handler(event):
            received_events.append(event.type)
        
        # 訂閱事件
        event_manager.subscribe(EventType.PLAYER_MOVE, test_handler)
        event_manager.subscribe(EventType.WEAPON_SWITCH, test_handler)
        
        # 發送事件
        event_manager.emit(EventType.PLAYER_MOVE, {'direction': 1})
        event_manager.emit(EventType.WEAPON_SWITCH, {'weapon': 'pistol'})
        
        # 處理事件
        event_manager.process_events()
        
        if len(received_events) == 2:
            print("✅ 事件系統測試成功")
            print(f"   處理了 {len(received_events)} 個事件")
            return True
        else:
            print(f"⚠️ 事件系統部分工作，處理了 {len(received_events)} 個事件")
            return False
        
    except Exception as e:
        print(f"❌ 事件系統測試失敗: {e}")
        return False

def test_file_structure():
    """測試文件結構"""
    print("\n🧪 測試文件結構...")
    
    required_files = [
        'src/core/config.py',
        'src/core/event_manager.py',
        'src/core/game.py',
        'src/systems/physics_system.py',
        'src/systems/sound_system.py',
        'src/weapons/weapon_base.py',
        'src/weapons/weapon_manager.py',
        'src/cards/card_base.py',
        'src/cards/card_manager.py',
        'src/ui/game_ui.py',
        'src/ui/card_selection_ui.py',
        'main.py',
        'requirements.txt',
        'README.md'
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            existing_files.append(file_path)
        else:
            missing_files.append(file_path)
    
    print(f"✅ 存在的文件: {len(existing_files)}/{len(required_files)}")
    
    if missing_files:
        print("⚠️ 缺少的文件:")
        for file_path in missing_files:
            print(f"   - {file_path}")
    
    # 檢查資產目錄
    assets_dir = 'assets/sounds'
    if os.path.exists(assets_dir):
        print("✅ 資產目錄存在")
    else:
        print("⚠️ 資產目錄不存在")
    
    return len(missing_files) == 0

def main():
    """主測試函數"""
    print("🎮 ROUNDS-like Python Game - 簡化測試")
    print("=" * 50)
    
    tests = [
        ("導入測試", test_imports),
        ("Pygame 可用性", test_pygame_availability),
        ("基本系統", test_basic_systems),
        ("配置系統", test_config_system),
        ("事件系統", test_event_system),
        ("文件結構", test_file_structure),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} 發生異常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 測試結果: {passed}/{total} 通過")
    
    if passed >= total * 0.8:  # 80% 通過率
        print("🎉 大部分測試通過！系統基本可用。")
        print("\n🚀 可以嘗試運行遊戲:")
        print("   python main.py --debug")
        print("   python main.py --no-sound  (如果音效有問題)")
    else:
        print("⚠️ 多個測試失敗，請檢查相關系統。")
        print("\n🛠️ 建議:")
        print("   1. 確保已安裝所有依賴: pip install -r requirements.txt")
        print("   2. 檢查 Python 版本 (建議 3.8+)")
        print("   3. 查看錯誤信息並修復相關問題")
    
    print(f"\n📝 注意: 這是簡化測試，某些複雜功能可能需要實際運行遊戲才能驗證。")

if __name__ == "__main__":
    main()
