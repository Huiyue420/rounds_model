# ROUNDS-like Python Game - 優化版本

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

一個用 Python 和 pygame 開發的類似 ROUNDS 的多人 2D 對戰遊戲 - 短期優化版本。

## 📖 目錄

- [🚀 新增優化功能](#-新增優化功能)
- [🎮 遊戲操作](#-遊戲操作)
- [🔫 武器系統](#-武器系統)
- [🎴 能力卡牌](#-能力卡牌)
- [🛠️ 快速開始](#️-快速開始)
- [📁 項目結構](#-項目結構)
- [🎯 特色功能說明](#-特色功能說明)
- [🤝 參與貢獻](#-參與貢獻)
- [📄 授權條款](#-授權條款)

## 🚀 新增優化功能

### ✨ 短期優化功能
- 🔫 **多種武器系統** - 手槍、散彈槍、衝鋒槍、狙擊槍
- 🎴 **卡牌選擇系統** - 每回合結束後選擇能力卡牌
- 🎵 **音效系統** - 射擊、跳躍、碰撞、重裝音效
- 🎨 **改進 UI 系統** - 更好的血量條、彈藥顯示、卡牌界面
- ⚡ **效能優化** - 改進的物理計算和渲染效率

### 🎮 遊戲操作

| 操作 | 按鍵 | 說明 |
|------|------|------|
| 移動 | A/D 或 ←/→ | 左右移動 |
| 跳躍 | 空白鍵 | 跳躍（需要在地面上）|
| 射擊 | 滑鼠左鍵 | 朝滑鼠位置射擊 |
| 重裝 | R | 重新裝彈 |
| 切換武器 | Q/E | 切換不同武器 |
| 退出 | ESC | 結束遊戲 |

### 🔫 武器系統

#### 手槍 (Pistol)
- 傷害: 25
- 射速: 2 發/秒
- 彈匣: 8 發
- 重裝時間: 1.5 秒

#### 散彈槍 (Shotgun)
- 傷害: 15 x 5 顆彈丸
- 射速: 1 發/秒
- 彈匣: 4 發
- 重裝時間: 2.5 秒

#### 衝鋒槍 (SMG)
- 傷害: 15
- 射速: 8 發/秒
- 彈匣: 24 發
- 重裝時間: 2.0 秒

#### 狙擊槍 (Sniper)
- 傷害: 75
- 射速: 0.5 發/秒
- 彈匣: 3 發
- 重裝時間: 3.0 秒

### 🎴 能力卡牌

#### 攻擊強化
- **傷害提升** - 增加 25% 武器傷害
- **快速射擊** - 增加 50% 射擊速度
- **大型彈匣** - 彈匣容量 +50%

#### 防禦強化
- **護甲** - 減少 20% 受到傷害
- **快速治療** - 每秒恢復 5 HP
- **額外生命** - 最大 HP +50

#### 移動強化
- **速度提升** - 移動速度 +30%
- **多重跳躍** - 可以二段跳
- **高跳** - 跳躍力 +40%

### 🛠️ 快速開始

```bash
# 克隆或下載專案後
cd rounds_model

# 安裝必要套件
pip install -r requirements.txt

# 運行遊戲
python main.py

# 調試模式
python main.py --debug

# 關閉音效（如果出現音效問題）
python main.py --no-sound
```

## 📁 項目結構

```
rounds_model/
├── main.py                 # 主程式入口點
├── requirements.txt        # Python 依賴套件
├── README.md              # 專案說明文件
├── src/                   # 主要源代碼
│   ├── core/              # 核心遊戲系統
│   │   ├── game.py        # 主遊戲循環和狀態管理
│   │   ├── config.py      # 遊戲配置類
│   │   └── event_manager.py # 事件系統
│   ├── entities/          # 遊戲實體
│   │   ├── player.py      # 玩家類
│   │   ├── bullet.py      # 子彈類
│   │   └── world.py       # 遊戲世界
│   ├── systems/           # 遊戲系統
│   │   ├── physics_system.py  # 物理引擎
│   │   ├── render_system.py   # 渲染系統
│   │   ├── input_system.py    # 輸入處理
│   │   ├── sound_system.py    # 音效系統
│   │   └── ui_system.py       # UI 系統
│   ├── weapons/           # 武器系統
│   │   ├── weapon_base.py # 武器基礎類
│   │   ├── pistol.py      # 手槍
│   │   ├── shotgun.py     # 散彈槍
│   │   ├── smg.py         # 衝鋒槍
│   │   └── sniper.py      # 狙擊槍
│   ├── cards/             # 卡牌系統
│   │   ├── card_base.py   # 卡牌基礎類
│   │   ├── card_manager.py # 卡牌管理器
│   │   └── card_effects.py # 卡牌效果
│   └── ui/                # 用戶界面
│       ├── game_ui.py     # 遊戲內 UI
│       └── card_selection_ui.py # 卡牌選擇界面
└── assets/                # 遊戲資源
    └── sounds/            # 音效檔案
```

## 🎯 特色功能說明

### 武器切換系統
玩家可以在遊戲中使用 Q/E 鍵切換不同武器，每種武器都有獨特的特性和用途。

### 卡牌選擇機制
每當玩家擊殺對手後，會出現卡牌選擇界面，可以從 3 張隨機卡牌中選擇一張來強化角色。

### 音效反饋
完整的音效系統提供沉浸式遊戲體驗，包括武器音效、環境音效等。

## 🧪 測試

專案包含兩種測試模式：

```bash
# 簡化測試（推薦用於快速檢查）
python test_simple.py

# 完整功能測試
python test_basic.py
```

## 🛠️ 系統需求

- **Python**: 3.8 或更高版本
- **作業系統**: Windows 10/11, macOS, Linux
- **記憶體**: 至少 2GB RAM
- **儲存空間**: 100MB 可用空間

## 🤝 參與貢獻

歡迎參與專案貢獻！請查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解詳細指南。

### 如何貢獻
1. Fork 此專案
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 創建 Pull Request

## 🐛 問題回報

發現 bug 或有功能建議？請到 [Issues](https://github.com/Huiyue420/rounds_model/issues) 頁面提交。

## 📄 授權條款

此專案使用 MIT 授權條款 - 查看 [LICENSE](LICENSE) 文件了解詳情。

## 🙏 致謝

- 感謝 [Landfall Games](https://landfall.se/) 開發的原版 ROUNDS 遊戲提供靈感
- 感謝 Pygame 社群提供優秀的遊戲開發工具
- 感謝所有貢獻者的參與和支持

---

🎮 Happy Gaming!
