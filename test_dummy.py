#!/usr/bin/env python3
"""
Test script for testing the dummy system and card selection
Run this to test bullet damage and card selection when killing dummies
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.core.game import Game
    from src.core.config import GameConfig
    import pygame
except ImportError as e:
    print(f"Import error: {e}")
    print("Please install pygame: pip install pygame")
    sys.exit(1)


def test_dummy_system():
    """Test the dummy system"""
    print("Testing Dummy System")
    print("=" * 50)
    print("Controls:")
    print("- WASD: Move player")
    print("- SPACE: Jump")
    print("- Left Mouse: Shoot")
    print("- Q/E: Switch weapons")
    print("- R: Reload")
    print("- T: Show test card selection")
    print("- H: Heal player")
    print("- 1: Add static dummy at mouse position")
    print("- 2: Add moving dummy at mouse position") 
    print("- 3: Clear all dummies")
    print("- ESC: Quit")
    print()
    print("Test Targets:")
    print("- Static dummy at (300, 300)")
    print("- Moving dummy at (500, 350)")
    print("- Static dummy at (800, 250)")
    print()
    print("When you kill a dummy, card selection should appear!")
    print("=" * 50)
    
    # Create test configuration
    config = GameConfig(
        debug=True,
        window_width=1280,
        window_height=720,
        target_fps=60,
        sound_enabled=False  # Disable sound for testing
    )
    
    try:
        # Create and run game
        game = Game(config)
        if hasattr(game, 'dummy_manager'):
            print(f"Game initialized with {len(game.dummy_manager.get_all_dummies())} test dummies")
        game.run()
    except KeyboardInterrupt:
        print("\nTest stopped by user")
    except Exception as e:
        print(f"Test error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_dummy_system()
