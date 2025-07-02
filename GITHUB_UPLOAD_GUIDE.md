# GitHub 上傳指南

本指南將協助您將 ROUNDS-like Python Game 專案上傳到 GitHub。

## 📋 前置準備

### 1. 確保 Git 已安裝
```bash
# 檢查 Git 版本
git --version
```

如果沒有安裝 Git，請到 [git-scm.com](https://git-scm.com/) 下載安裝。

### 2. 設定 Git 用戶資訊
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 3. 確保專案可以正常運行
```bash
# 在專案目錄中運行測試
python test_simple.py
```

## 🚀 上傳步驟

### 步驟 1: 初始化 Git 儲存庫
```bash
# 在專案根目錄中執行
cd rounds_model
git init
```

### 步驟 2: 添加文件到暫存區
```bash
# 添加所有文件
git add .

# 或者選擇性添加文件
git add src/
git add main.py
git add requirements.txt
git add README.md
git add .gitignore
```

### 步驟 3: 創建第一次提交
```bash
git commit -m "Initial commit: ROUNDS-like Python Game with optimized features

- 多種武器系統（手槍、散彈槍、衝鋒槍、狙擊槍）
- 卡牌選擇系統
- 音效系統
- 改進的 UI 系統
- 效能優化
- 完整的測試套件"
```

### 步驟 4: 在 GitHub 上創建儲存庫

1. 登入 [GitHub](https://github.com)
2. 點擊右上角的 "+" 按鈕，選擇 "New repository"
3. 填寫儲存庫資訊：
   - **Repository name**: `rounds-python-game` 或您喜歡的名稱
   - **Description**: `A ROUNDS-like 2D multiplayer battle game built with Python and Pygame`
   - **Visibility**: Public 或 Private（依您的需求）
   - **不要**勾選 "Initialize this repository with README"（因為我們已經有了）

### 步驟 5: 連接本地儲存庫到 GitHub
```bash
# 添加遠端儲存庫（替換成您的 GitHub 用戶名和儲存庫名）
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git

# 設定主分支名稱
git branch -M main
```

### 步驟 6: 推送到 GitHub
```bash
# 首次推送
git push -u origin main
```

## 🔧 後續更新

當您對專案進行更改時：

```bash
# 查看變更狀態
git status

# 添加變更的文件
git add .

# 提交變更
git commit -m "描述您的變更"

# 推送到 GitHub
git push
```

## 🌟 提交信息規範

使用清晰的提交信息：

```bash
# 好的提交信息範例
git commit -m "feat: 添加新的卡牌效果 - 彈跳子彈"
git commit -m "fix: 修復武器切換時的音效問題"
git commit -m "docs: 更新 README 中的安裝說明"
git commit -m "test: 添加卡牌系統的單元測試"
```

## 📂 重要文件說明

您的專案現在包含以下 Git 相關文件：

- **`.gitignore`**: 指定 Git 應該忽略的文件和目錄
- **`LICENSE`**: MIT 開源許可證
- **`CONTRIBUTING.md`**: 貢獻指南
- **`.github/workflows/python-tests.yml`**: GitHub Actions 自動化測試配置

## 🛠️ 故障排除

### 問題 1: 推送被拒絕
```bash
# 如果遠端有變更，先拉取
git pull origin main --rebase
git push
```

### 問題 2: 忘記添加 .gitignore
```bash
# 移除已追踪但應該被忽略的文件
git rm -r --cached __pycache__/
git commit -m "Remove cached files that should be ignored"
```

### 問題 3: 需要修改最後一次提交
```bash
# 修改最後一次提交信息
git commit --amend -m "新的提交信息"
```

## 📊 GitHub 功能利用

### 啟用 Issues 和 Discussions
在您的 GitHub 儲存庫設定中：
1. 前往 Settings > Features
2. 啟用 Issues
3. 啟用 Discussions（用於社群討論）

### 設定 GitHub Pages（可選）
如果您想要建立專案網站：
1. 前往 Settings > Pages
2. 選擇 Source: Deploy from a branch
3. 選擇 Branch: main, / (root)

### 添加標籤和發布版本
```bash
# 創建標籤
git tag -a v1.0.0 -m "First stable release"
git push origin v1.0.0
```

然後在 GitHub 上前往 "Releases" 創建正式發布版本。

## 🎉 完成！

您的專案現在已經在 GitHub 上了！其他人可以：
- 查看您的代碼
- 提交 Issues
- Fork 您的專案
- 提交 Pull Requests

不要忘記定期更新您的專案，並與社群互動！
