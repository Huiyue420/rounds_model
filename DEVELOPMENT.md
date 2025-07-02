# ROUNDS-like Python Game - 開發文檔

## 🎯 專案概述

這是一個基於原版 `rounds_py` 的短期優化版本，包含以下新功能：

- 🔫 **多種武器系統** - 手槍、散彈槍、衝鋒槍、狙擊槍
- 🎴 **卡牌選擇系統** - 能力強化卡牌
- 🎵 **音效系統** - 完整的音效支援
- 🎨 **改進 UI 系統** - 更好的用戶界面
- ⚡ **效能優化** - 空間哈希、物理休眠等

## 🏗️ 架構設計

### 系統架構圖
```
Game (主遊戲循環)
├── EventManager (事件系統)
├── PhysicsSystem (物理系統)
├── SoundSystem (音效系統)
├── WeaponManager (武器管理)
├── CardManager (卡牌管理)
├── GameUI (遊戲界面)
└── CardSelectionUI (卡牌選擇界面)
```

### 模組化設計

每個系統都是獨立的模組，可以單獨移除而不影響其他系統：

- **核心系統** (`src/core/`): 遊戲核心邏輯
- **實體系統** (`src/entities/`): 遊戲對象
- **功能系統** (`src/systems/`): 物理、渲染、音效等
- **武器系統** (`src/weapons/`): 武器相關邏輯
- **卡牌系統** (`src/cards/`): 卡牌效果和管理
- **UI 系統** (`src/ui/`): 用戶界面

## 🔧 技術實現詳解

### 1. 武器系統

#### 基礎架構
```python
class WeaponBase(ABC):
    def __init__(self, weapon_type, config, event_manager):
        # 從配置讀取武器屬性
        # 設置修正值（受卡牌影響）
    
    def shoot(self, start_pos, target_pos) -> bool:
        # 檢查射擊條件
        # 計算彈道
        # 發送事件
    
    def reload(self) -> bool:
        # 重裝邏輯
```

#### 武器特性
| 武器 | 傷害 | 射速 | 彈匣 | 特殊效果 |
|------|------|------|------|----------|
| 手槍 | 25 | 2/秒 | 8發 | 平衡型 |
| 散彈槍 | 15x5 | 1/秒 | 4發 | 散射彈丸 |
| 衝鋒槍 | 15 | 8/秒 | 24發 | 高射速 |
| 狙擊槍 | 75 | 0.5/秒 | 3發 | 高傷害 |

#### 可擴展性
- 新增武器：繼承 `WeaponBase` 類
- 修改屬性：編輯 `config.py` 中的 `weapon_configs`
- 自定義效果：重寫 `_create_bullets` 方法

### 2. 卡牌系統

#### 卡牌類型
- **攻擊型**: 傷害提升、射速提升、大型子彈
- **防禦型**: 護甲、快速治療、額外生命
- **移動型**: 速度提升、二段跳、高跳
- **功能型**: 大型彈匣、換彈加速

#### 卡牌稀有度
- **普通** (50%): 基礎增強效果
- **稀有** (30%): 中等增強效果  
- **史詩** (15%): 強力增強效果
- **傳說** (5%): 極強增強效果

#### 效果疊加
```python
# 可疊加卡牌
if card.can_stack():
    card.add_stack()
    effect_value *= card.current_stacks

# 應用到玩家
player.damage_multiplier += card.damage_boost
weapon.reload_time *= (1 - card.reload_speed_boost)
```

### 3. 音效系統

#### 音效管理
```python
class SoundSystem:
    def __init__(self, config, event_manager):
        # 初始化 pygame.mixer
        # 載入音效檔案
        # 創建佔位音效（如果檔案不存在）
    
    def play_sound(self, sound_name, volume=None):
        # 播放指定音效
        # 調整音量
```

#### 事件驅動
```python
# 發送音效事件
event_manager.emit(EventType.SOUND_PLAY, {
    'sound': 'pistol_shoot',
    'volume': 0.8
})
```

### 4. UI 系統

#### 組件化設計
```python
class UIElement:
    def render(self, screen, font): pass
    def update(self, dt): pass

class HealthBar(UIElement):
    # 血量條實現
    
class AmmoDisplay(UIElement):
    # 彈藥顯示實現
```

#### 事件更新
```python
# UI 通過事件更新
event_manager.emit(EventType.UI_UPDATE_HEALTH, {
    'current_health': player.health,
    'max_health': player.max_health
})
```

### 5. 物理系統優化

#### 空間哈希
```python
def _broad_phase_collision_detection(self):
    # 將物體放入哈希格子
    # 只檢查同一格子內的物體
    # 大幅減少碰撞檢測計算量
```

#### 物理休眠
```python
def can_sleep(self):
    return (velocity.length() < threshold and 
            acceleration.length() < threshold)
```

## 🎮 遊戲玩法設計

### 核心循環
1. **對戰階段**: 玩家互相射擊
2. **擊殺獎勵**: 擊殺對手後獲得卡牌選擇
3. **能力強化**: 選擇卡牌提升角色能力
4. **新回合開始**: 更強的角色繼續對戰

### 平衡性考量
- **武器平衡**: 高傷害武器有低射速或小彈匣
- **卡牌限制**: 稀有卡牌出現機率低
- **疊加上限**: 防止某些效果過於強力

## 🛠️ 開發指南

### 添加新武器

1. 在 `config.py` 中添加武器配置：
```python
'new_weapon': {
    'name': '新武器',
    'damage': 30,
    'fire_rate': 3.0,
    'magazine_size': 10,
    'reload_time': 2.0,
    'bullet_speed': 900.0,
    'bullet_size': (8, 8),
    'spread': 2,
    'bullets_per_shot': 1,
}
```

2. 創建武器類：
```python
class NewWeapon(WeaponBase):
    def __init__(self, config, event_manager):
        super().__init__('new_weapon', config, event_manager)
    
    def get_display_name(self):
        return "🔥 新武器"
```

3. 在 `WeaponManager` 中註冊：
```python
self.weapons['new_weapon'] = NewWeapon(config, event_manager)
```

### 添加新卡牌

1. 創建卡牌類：
```python
class NewEffectCard(CardBase):
    def __init__(self):
        super().__init__(
            card_id="new_effect",
            name="新效果",
            description="卡牌描述",
            card_type=CardType.OFFENSIVE,
            rarity=CardRarity.RARE
        )
    
    def apply_effect(self, player):
        # 實現效果邏輯
        pass
```

2. 在 `CardManager` 中註冊：
```python
self.card_types['new_effect'] = NewEffectCard
```

### 修改遊戲參數

編輯 `src/core/config.py`：
```python
# 調整玩家屬性
player_speed: float = 350.0  # 增加移動速度
player_jump_force: float = 600.0  # 增加跳躍力

# 調整物理參數
gravity: float = 1200.0  # 增加重力

# 調整武器參數
weapon_configs['pistol']['damage'] = 30  # 增加手槍傷害
```

## 🧪 測試和調試

### 基本測試
```bash
# 運行基礎測試
python test_basic.py

# 運行遊戲（調試模式）
python main.py --debug

# 運行遊戲（無音效）
python main.py --no-sound
```

### 調試快捷鍵
- `ESC`: 退出遊戲
- `Q/E`: 切換武器
- `R`: 重裝彈藥
- `C`: 測試卡牌選擇
- `T`: 測試受傷
- `H`: 測試治療

### 常見問題

#### Pygame 未安裝
```bash
pip install pygame
```

#### 音效問題
```bash
# 關閉音效運行
python main.py --no-sound
```

#### 效能問題
```python
# 降低目標 FPS
config.target_fps = 30

# 啟用物理休眠
physics_system.enable_sleeping = True
```

## 📈 未來擴展

### 短期計劃
- [ ] 完整的玩家實體類
- [ ] 子彈物理和碰撞
- [ ] 更多卡牌效果
- [ ] AI 對手

### 中期計劃  
- [ ] 網路多人模式
- [ ] 自定義關卡
- [ ] 更多武器類型
- [ ] 粒子特效系統

### 長期計劃
- [ ] 關卡編輯器
- [ ] Mod 支援
- [ ] 競技排名系統
- [ ] 跨平台支援

## 📄 API 參考

### 事件類型
```python
class EventType(Enum):
    PLAYER_MOVE = "player_move"
    PLAYER_SHOOT = "player_shoot"
    WEAPON_SWITCH = "weapon_switch"
    CARD_SELECT = "card_select"
    SOUND_PLAY = "sound_play"
    # ... 更多事件類型
```

### 配置選項
```python
@dataclass
class GameConfig:
    window_width: int = 1280
    window_height: int = 720
    target_fps: int = 60
    sound_enabled: bool = True
    # ... 更多配置選項
```

---

這個優化版本展示了如何將原始專案擴展為一個功能豐富、模組化的遊戲系統。所有新功能都與現有代碼保持兼容，可以輕鬆集成或移除。
