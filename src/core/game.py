"""
Main Game Class - Optimized Version
Manages the main game loop and core systems, integrating all new features
"""

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    pygame = None

import sys
import math
from typing import Optional, List
import logging
import time

from .config import GameConfig
from .event_manager import EventManager, EventType
from ..systems.physics_system import PhysicsSystem
from ..systems.sound_system import SoundSystem
from ..ui.game_ui import GameUI
from ..ui.card_selection_ui import CardSelectionUI
from ..weapons.weapon_manager import WeaponManager
from ..cards.card_manager import CardManager
from ..entities.player import Player
from ..entities.bullet import BulletManager, Bullet
from ..entities.world import GameWorld
from ..entities.dummy import DummyManager


class Game:
    """Main Game Class - Optimized Version"""
    
    def __init__(self, config: GameConfig):
        self.config = config
        self.running = False
        self.clock = None
        self.screen = None
        
        # Setup logging
        log_level = logging.DEBUG if config.debug else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Check pygame availability
        if not PYGAME_AVAILABLE:
            self.logger.error("Pygame not installed. Cannot run game.")
            self.logger.info("Please run: pip install pygame")
            return
        
        # Initialize pygame
        self._init_pygame()
        
        # Initialize systems
        self.event_manager = EventManager()
        self.physics_system = PhysicsSystem(config)
        self.sound_system = SoundSystem(config, self.event_manager)
        
        # Initialize UI systems
        self.game_ui = GameUI(config, self.event_manager)
        self.card_selection_ui = CardSelectionUI(config, self.event_manager)
        
        # Initialize game managers
        self.weapon_manager = WeaponManager(config, self.event_manager)
        self.card_manager = CardManager(self.event_manager)
        
        # Initialize game world and entities
        self.world = GameWorld(config.window_width, config.window_height)
        self.bullet_manager = BulletManager()
        self.dummy_manager = DummyManager(config)  # Add dummy manager
        self.players: List[Player] = []
        
        # Test dummies
        self._create_test_dummies()  # Create test dummies
        
        # Players
        self._create_players()
        
        # Game state
        self.game_state = "playing"  # playing, card_selection, paused
        self.selected_player_for_cards = None
        
        # Input handling
        self.keys_pressed = {}
        self.key_events = []
        
        # Register event handlers
        self._register_event_handlers()
        
        # Statistics
        self.frame_count = 0
        self.last_fps_update = time.time()
        self.current_fps = 0.0
        
        self.logger.info("Game initialized successfully (Optimized Version)")
    
    def _init_pygame(self) -> None:
        """Initialize Pygame"""
        if not PYGAME_AVAILABLE:
            return
        
        pygame.init()
        
        # Create window
        flags = pygame.FULLSCREEN if self.config.fullscreen else 0
        self.screen = pygame.display.set_mode(self.config.get_window_size(), flags)
        pygame.display.set_caption(self.config.window_title)
        
        # Initialize clock
        self.clock = pygame.time.Clock()
        
        self.logger.info(f"Pygame initialized - Resolution: {self.config.window_size}")
    
    def _create_test_dummies(self) -> None:
        """Create test dummies for testing"""
        # Create some static dummies
        dummy1 = self.dummy_manager.add_dummy(300, 300, moving=False)
        dummy2 = self.dummy_manager.add_dummy(500, 350, moving=True, move_speed=50, move_range=150)
        dummy3 = self.dummy_manager.add_dummy(800, 250, moving=False)
        
        self.logger.info("Test dummies created")
    
    def _create_players(self) -> None:
        """Create players"""
        # Create local player
        start_x = self.config.window_width // 2
        start_y = 100  # Start near top of screen
        
        player = Player(start_x, start_y, self.config, player_id=1)
        self.players.append(player)
        
        self.logger.info(f"Player created - Position: ({start_x}, {start_y})")
    
    def _register_event_handlers(self) -> None:
        """Register event handlers"""
        self.event_manager.subscribe(EventType.WEAPON_SWITCH, self._handle_weapon_switch)
        self.event_manager.subscribe(EventType.CARD_SELECT, self._handle_card_select)
        self.event_manager.subscribe(EventType.PLAYER_DEATH, self._handle_player_death)
        self.event_manager.subscribe(EventType.WEAPON_SHOOT, self._handle_weapon_shoot)
        self.event_manager.subscribe(EventType.DUMMY_DEATH, self._handle_dummy_death)
    
    def run(self) -> None:
        """Run the main game loop"""
        if not PYGAME_AVAILABLE:
            self.logger.error("Cannot start game: Pygame not available")
            return
        
        self.running = True
        self.logger.info("Game started")
        
        try:
            while self.running:
                # Calculate delta time
                dt = self.clock.tick(self.config.target_fps) / 1000.0
                
                # Handle events
                self._handle_events()
                
                # Update game
                if self.game_state == "playing":
                    self._update(dt)
                elif self.game_state == "card_selection":
                    self._update_card_selection(dt)
                
                # Render
                self._render()
                
                # Update display
                pygame.display.flip()
                
                # Update statistics
                self._update_statistics()
                
        except Exception as e:
            self.logger.error(f"Game runtime error: {e}")
            if self.config.debug:
                raise
        finally:
            self._cleanup()
    
    def _handle_events(self) -> None:
        """Handle events"""
        self.key_events = []
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.key_events.append(event)
                self._handle_keydown(event)
            elif event.type == pygame.KEYUP:
                self.key_events.append(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event)
        
        # Update continuous key states
        self.keys_pressed = pygame.key.get_pressed()
    
    def _handle_keydown(self, event) -> None:
        """Handle key down events"""
        if event.key == pygame.K_ESCAPE:
            self.running = False
        elif event.key == pygame.K_q:
            # Switch to previous weapon
            self.weapon_manager.previous_weapon()
        elif event.key == pygame.K_e:
            # Switch to next weapon
            self.weapon_manager.next_weapon()
        elif event.key == pygame.K_r:
            # Reload
            self.weapon_manager.reload()
        elif event.key == pygame.K_c:
            # Test card selection
            self._show_card_selection_test()
        elif event.key == pygame.K_t:
            # Show test card selection
            self._show_card_selection_test()
        elif event.key == pygame.K_h:
            # Test healing
            if self.players:
                self.players[0].heal(25)
                self._update_ui()
        elif event.key == pygame.K_1:
            # Add static dummy at mouse position
            mouse_pos = pygame.mouse.get_pos()
            self.dummy_manager.add_dummy(mouse_pos[0], mouse_pos[1], moving=False)
            self.logger.info(f"Added static dummy at {mouse_pos}")
        elif event.key == pygame.K_2:
            # Add moving dummy at mouse position
            mouse_pos = pygame.mouse.get_pos()
            self.dummy_manager.add_dummy(mouse_pos[0], mouse_pos[1], moving=True, move_speed=50, move_range=100)
            self.logger.info(f"Added moving dummy at {mouse_pos}")
        elif event.key == pygame.K_3:
            # Clear all dummies
            self.dummy_manager.clear_all()
            self.logger.info("Cleared all dummies")
    
    def _handle_mouse_click(self, event) -> None:
        """Handle mouse click events"""
        if event.button == 1:  # Left click
            if self.game_state == "card_selection":
                # Card selection mode
                self.card_selection_ui.handle_click(event.pos)
            else:
                # Normal game mode - shoot
                if self.players:
                    player = self.players[0]
                    # Only allow shooting if player is alive
                    if not player.alive:
                        return
                        
                    start_pos = player.get_center_position()
                    target_pos = event.pos
                    
                    # Calculate angle
                    dx = target_pos[0] - start_pos[0]
                    dy = target_pos[1] - start_pos[1]
                    angle = math.atan2(dy, dx)
                    
                    # Calculate bullet spawn position outside player collision box
                    player_radius = player.width / 2
                    spawn_offset = player_radius + 5  # 5 pixels outside player
                    bullet_start_x = start_pos[0] + math.cos(angle) * spawn_offset
                    bullet_start_y = start_pos[1] + math.sin(angle) * spawn_offset
                    
                    # Try to shoot
                    weapon_fired = self.weapon_manager.shoot(start_pos, target_pos)
                    if weapon_fired:
                        # Create bullet
                        weapon_info = self.weapon_manager.get_weapon_info()
                        bullet = Bullet(
                            bullet_start_x, bullet_start_y, angle,
                            weapon_info.get('bullet_speed', 500),
                            weapon_info.get('damage', 25),
                            weapon_info.get('bullet_size', 3.0)
                        )
                        self.bullet_manager.add_bullet(bullet)
                    
                    self._update_ui()
    
    def _update(self, dt: float) -> None:
        """Update game state"""
        # Process event queue
        self.event_manager.process_events()
        
        # Update weapon system
        self.weapon_manager.update(dt)
        
        # Update players
        for player in self.players:
            # Handle player input
            player.handle_input(self.keys_pressed, self.key_events)
            
            # Update player physics
            player.update(dt, gravity=self.config.gravity)
            
            # Check collision with platforms
            player.check_ground_collision(self.world.get_platforms())
            
            # Check world boundaries
            self.world.check_boundaries(player)
        
        # Update bullets
        self.bullet_manager.update(dt, self.world.get_platforms(), self.players)
        
        # Update dummies
        self.dummy_manager.update(dt)
        
        # Check bullet-dummy collisions
        self._check_bullet_dummy_collisions()
        
        # Update physics system
        self.physics_system.update(dt)
        
        # Update UI
        self.game_ui.update(dt, self.current_fps)
        
        # Periodically update UI display
        self._update_ui()
    
    def _update_card_selection(self, dt: float) -> None:
        """Update card selection state"""
        self.card_selection_ui.update(dt)
    
    def _render(self) -> None:
        """Render game screen"""
        # Clear screen
        self.screen.fill(self.config.get_background_color())
        
        # Render world
        self.world.render(self.screen)
        
        # Render players
        for player in self.players:
            if player.alive:
                player.render(self.screen)
        
        # Render dummies
        self.dummy_manager.render(self.screen)
        
        # Render bullets
        self.bullet_manager.render(self.screen)
        
        # Render UI
        self.game_ui.render(self.screen)
        
        # Render card selection interface
        if self.game_state == "card_selection":
            self.card_selection_ui.render(self.screen)
        
        # Render debug info
        if self.config.debug:
            self._render_debug_info()
    
    def _render_debug_info(self) -> None:
        """Render debug information"""
        font = pygame.font.Font(None, 24)
        debug_info = [
            f"Players: {len(self.players)}",
            f"Active Bullets: {self.bullet_manager.get_bullet_count()}",
            f"Physics Bodies: {self.physics_system.get_bodies_count()}",
            f"Active Bodies: {self.physics_system.get_active_bodies_count()}",
            f"Game State: {self.game_state}",
            f"Current Weapon: {self.weapon_manager.current_weapon.get_display_name()}",
        ]
        
        if self.players:
            player = self.players[0]
            debug_info.extend([
                f"Player Pos: ({player.position.x:.1f}, {player.position.y:.1f})",
                f"Player Vel: ({player.velocity.x:.1f}, {player.velocity.y:.1f})",
                f"On Ground: {player.on_ground}",
                f"Health: {player.health}/{player.max_health}"
            ])
        
        y_offset = 10
        for info in debug_info:
            text_surface = font.render(info, True, (255, 255, 0))
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 25
    
    def _update_statistics(self) -> None:
        """Update statistics"""
        self.frame_count += 1
        current_time = time.time()
        
        if current_time - self.last_fps_update >= 1.0:
            self.current_fps = self.frame_count / (current_time - self.last_fps_update)
            self.frame_count = 0
            self.last_fps_update = current_time
    
    def _update_ui(self) -> None:
        """Update UI display"""
        if not self.players:
            return
        
        player = self.players[0]
        
        # Update health display
        self.event_manager.emit(EventType.UI_UPDATE_HEALTH, {
            'current_health': player.health,
            'max_health': player.max_health
        })
        
        # Update weapon and ammo display
        weapon_info = self.weapon_manager.get_weapon_info()
        self.event_manager.emit(EventType.UI_UPDATE_WEAPON, {
            'weapon_name': weapon_info['name']
        })
        
        self.event_manager.emit(EventType.UI_UPDATE_AMMO, {
            'current_ammo': weapon_info['ammo'],
            'max_ammo': weapon_info['max_ammo'],
            'is_reloading': weapon_info['is_reloading'],
            'reload_progress': weapon_info['reload_progress']
        })
    
    def _show_card_selection_test(self) -> None:
        """Show test card selection"""
        if self.players and self.game_state == "playing":
            # Get random cards
            cards = self.card_manager.get_random_cards(3)
            cards_data = [card.to_dict() for card in cards]
            
            # Show card selection interface
            self.card_selection_ui.show_selection(
                player_id=self.players[0].player_id,
                cards_data=cards_data,
                callback=self._on_card_selected
            )
            
            self.game_state = "card_selection"
            self.selected_player_for_cards = self.players[0]
    
    def _on_card_selected(self, player_id: int, card_data: dict) -> None:
        """Card selection callback"""
        if self.selected_player_for_cards:
            # Create card instance
            card = self.card_manager.create_card(card_data['id'])
            if card:
                # Add to player
                self.card_manager.add_card_to_player(player_id, card)
                # Apply effects
                self.card_manager.apply_card_to_player(player_id, card, self.selected_player_for_cards)
                
                self.logger.info(f"Player {player_id} gained card: {card_data['name']}")
        
        # Return to game mode
        self.game_state = "playing"
        self.selected_player_for_cards = None
        
        # Update UI
        self._update_ui()
    
    def _handle_weapon_switch(self, event) -> None:
        """Handle weapon switch event"""
        data = event.data
        weapon_name = data.get('weapon_name', '')
        
        self.logger.info(f"Weapon switched: {weapon_name}")
        
        # Play switch sound
        self.event_manager.emit(EventType.SOUND_PLAY, {
            'sound': 'weapon_switch'
        })
        
        # Update UI
        self._update_ui()
    
    def _handle_weapon_shoot(self, event) -> None:
        """Handle weapon shoot event"""
        data = event.data
        weapon_name = data.get('weapon_name', '')
        
        # Play shoot sound
        self.event_manager.emit(EventType.SOUND_PLAY, {
            'sound': f'{weapon_name}_shoot'
        })
    
    def _handle_card_select(self, event) -> None:
        """Handle card select event"""
        data = event.data
        card_data = data.get('card_data', {})
        
        self.logger.info(f"Card selected: {card_data.get('name', 'Unknown')}")
    
    def _handle_player_death(self, event) -> None:
        """Handle player death event"""
        data = event.data
        player_id = data.get('player_id', 0)
        
        self.logger.info(f"Player {player_id} died")
        
        # TODO: Implement respawn logic
    
    def _check_bullet_dummy_collisions(self) -> None:
        """Check collisions between bullets and dummies"""
        bullets_to_remove = []
        
        for bullet in self.bullet_manager.bullets:
            # Handle both tuple and float bullet sizes
            if isinstance(bullet.size, (tuple, list)):
                width, height = bullet.size
            else:
                width = height = bullet.size
                
            bullet_rect = pygame.Rect(
                bullet.position.x - width//2, 
                bullet.position.y - height//2,
                width, 
                height
            )
            
            killed_dummy = self.dummy_manager.handle_bullet_collision(
                bullet_rect, bullet.damage, "bullet"
            )
            
            if killed_dummy:
                # Mark bullet for removal
                bullets_to_remove.append(bullet)
                
                # Trigger dummy death event
                self.event_manager.emit(EventType.DUMMY_DEATH, {
                    'dummy_id': killed_dummy.dummy_id,
                    'killer_player_id': getattr(bullet, 'owner_id', 1)  # Default to player 1
                })
        
        # Remove bullets that hit dummies
        for bullet in bullets_to_remove:
            if bullet in self.bullet_manager.bullets:
                self.bullet_manager.bullets.remove(bullet)
    
    def _handle_dummy_death(self, event) -> None:
        """Handle dummy death event - trigger card selection"""
        data = event.data
        dummy_id = data.get('dummy_id')
        killer_player_id = data.get('killer_player_id', 1)
        
        self.logger.info(f"Dummy {dummy_id} killed by player {killer_player_id}")
        
        # Find the killer player
        killer_player = None
        for player in self.players:
            if player.player_id == killer_player_id:
                killer_player = player
                break
        
        if killer_player and self.game_state == "playing":
            # Show card selection
            cards = self.card_manager.get_random_cards(3)
            cards_data = [card.to_dict() for card in cards]
            
            self.card_selection_ui.show_selection(
                player_id=killer_player.player_id,
                cards_data=cards_data,
                callback=self._on_card_selected
            )
            
            self.game_state = "card_selection"
            self.selected_player_for_cards = killer_player
            
            self.logger.info(f"Card selection triggered for player {killer_player_id}")
    
    def _cleanup(self) -> None:
        """Cleanup resources"""
        self.logger.info("Cleaning up game resources...")
        
        # Cleanup systems
        if hasattr(self, 'sound_system'):
            self.sound_system.cleanup()
        
        if hasattr(self, 'physics_system'):
            self.physics_system.cleanup()
        
        if hasattr(self, 'game_ui'):
            self.game_ui.cleanup()
        
        # Cleanup pygame
        if PYGAME_AVAILABLE:
            pygame.quit()
        
        self.logger.info("Game closed")
