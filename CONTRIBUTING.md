# Contributing to ROUNDS-like Python Game

感謝您對本專案的興趣！以下是如何參與貢獻的指南。

## 🚀 如何開始

1. **Fork 專案**
   ```bash
   # 在 GitHub 上 fork 此專案
   # 然後 clone 到本地
   git clone https://github.com/[your-username]/rounds-model.git
   cd rounds-model
   ```

2. **設置開發環境**
   ```bash
   # 安裝依賴
   pip install -r requirements.txt
   
   # 運行測試確保環境正常
   python test_simple.py
   ```

3. **創建分支**
   ```bash
   git checkout -b feature/new-feature
   # 或
   git checkout -b fix/bug-description
   ```

## 🛠️ 開發流程

### 代碼規範
- 使用 4 個空格縮進
- 函數和類名使用中文註釋
- 變數名使用英文，但要有意義
- 每個函數都應該有 docstring

### 提交規範
使用以下格式的提交信息：
```
類型(範圍): 簡短描述

詳細描述（如果需要）

關聯 Issue: #123
```

類型包括：
- `feat`: 新功能
- `fix`: 修復 bug
- `docs`: 文檔更新
- `style`: 代碼格式化
- `refactor`: 重構代碼
- `test`: 測試相關
- `chore`: 其他雜項

### 測試
在提交前請確保：
- 運行 `python test_simple.py` 通過
- 運行 `python test_basic.py` 通過
- 新功能有對應的測試

## 🎮 專案結構

請參閱 README.md 中的專案結構說明，新增功能時請遵循現有的架構。

## 🐛 問題回報

發現 bug 時，請：
1. 檢查是否已有相關 Issue
2. 創建新 Issue 時請包含：
   - 運行環境（Python 版本、OS）
   - 重現步驟
   - 預期行為 vs 實際行為
   - 錯誤信息或截圖

## 💡 功能建議

建議新功能時：
1. 先創建 Issue 討論可行性
2. 描述功能的用例和價值
3. 考慮對現有系統的影響

## 📝 文檔

- 更新代碼時請同步更新相關文檔
- 新功能需要更新 README.md
- API 變更需要更新 DEVELOPMENT.md

## 🤝 行為準則

- 尊重所有參與者
- 接受建設性批評
- 專注於專案目標
- 幫助新手參與

## 📞 聯繫方式

如有問題，歡迎：
- 創建 Issue
- 發起 Discussion
- 提交 Pull Request

感謝您的貢獻！ 🎉
