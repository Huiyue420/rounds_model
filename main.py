"""
ROUNDS-like Python Game - 優化版本
主程式入口點 - 包含短期優化功能
"""

import sys
import os
import argparse

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.core.game import Game
    from src.core.config import GameConfig
except ImportError as e:
    print(f"Import error: {e}")
    print("請確保已安裝所有依賴套件：pip install -r requirements.txt")
    sys.exit(1)


def main():
    """主函數"""
    parser = argparse.ArgumentParser(description='ROUNDS-like Python Game - 優化版本')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--server', action='store_true', help='Run as server')
    parser.add_argument('--port', type=int, default=8765, help='Server port')
    parser.add_argument('--no-sound', action='store_true', help='Disable sound effects')
    
    args = parser.parse_args()
    
    # 創建遊戲配置
    config = GameConfig(
        debug=args.debug,
        server_mode=args.server,
        server_port=args.port,
        sound_enabled=not args.no_sound
    )
    
    try:
        # 創建並運行遊戲
        game = Game(config)
        game.run()
    except KeyboardInterrupt:
        print("\n遊戲已停止")
    except Exception as e:
        print(f"遊戲錯誤: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
