"""
物理系統 - 優化版本
處理遊戲中所有物理運算，包括碰撞檢測、重力等
增加了效能優化和更精確的碰撞檢測
"""

try:
    import pygame
except ImportError:
    pygame = None

from typing import List, Tuple, Optional, Set
import logging
import math

from ..core.config import GameConfig


class Vector2:
    """2D 向量類 - 優化版本"""
    
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y
    
    def __add__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> 'Vector2':
        return Vector2(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar: float) -> 'Vector2':
        if scalar != 0:
            return Vector2(self.x / scalar, self.y / scalar)
        return Vector2(0, 0)
    
    def length(self) -> float:
        """計算向量長度"""
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def length_squared(self) -> float:
        """計算向量長度的平方（避免開根號運算）"""
        return self.x * self.x + self.y * self.y
    
    def normalize(self) -> 'Vector2':
        """標準化向量"""
        length = self.length()
        if length == 0:
            return Vector2(0, 0)
        return Vector2(self.x / length, self.y / length)
    
    def dot(self, other: 'Vector2') -> float:
        """點積"""
        return self.x * other.x + self.y * other.y
    
    def to_tuple(self) -> Tuple[float, float]:
        """轉換為元組"""
        return (self.x, self.y)
    
    def copy(self) -> 'Vector2':
        """複製向量"""
        return Vector2(self.x, self.y)


class PhysicsBody:
    """物理體類 - 優化版本"""
    
    def __init__(self, x: float, y: float, width: float, height: float):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.width = width
        self.height = height
        self.mass = 1.0
        self.friction = 0.95
        self.restitution = 0.3  # 彈性係數
        self.is_static = False
        self.is_grounded = False
        self.affected_by_gravity = True
        
        # 碰撞相關
        self.collision_layer = 0
        self.collision_mask = 0xFFFFFFFF  # 預設與所有層碰撞
        self.is_trigger = False  # 是否為觸發器
        
        # 效能優化
        self.last_position = Vector2(x, y)
        self.needs_update = True
        self.sleep_threshold = 0.1  # 休眠閾值
        self.is_sleeping = False
    
    @property
    def rect(self):
        """獲取碰撞矩形"""
        if pygame:
            return pygame.Rect(
                int(self.position.x - self.width / 2),
                int(self.position.y - self.height / 2),
                int(self.width),
                int(self.height)
            )
        else:
            # 簡單的矩形類
            return {
                'x': int(self.position.x - self.width / 2),
                'y': int(self.position.y - self.height / 2),
                'width': int(self.width),
                'height': int(self.height)
            }
    
    @property
    def center(self) -> Tuple[int, int]:
        """獲取中心點"""
        return (int(self.position.x), int(self.position.y))
    
    def wake_up(self) -> None:
        """喚醒物理體"""
        self.is_sleeping = False
        self.needs_update = True
    
    def can_sleep(self) -> bool:
        """檢查是否可以休眠"""
        return (not self.is_static and 
                self.velocity.length_squared() < self.sleep_threshold and
                self.acceleration.length_squared() < self.sleep_threshold)


class CollisionInfo:
    """碰撞資訊類"""
    
    def __init__(self, body_a: PhysicsBody, body_b: PhysicsBody, 
                 normal: Vector2, penetration: float):
        self.body_a = body_a
        self.body_b = body_b
        self.normal = normal  # 碰撞法向量
        self.penetration = penetration  # 穿透深度


class PhysicsSystem:
    """物理系統類 - 優化版本"""
    
    def __init__(self, config: GameConfig):
        self.config = config
        self.bodies: List[PhysicsBody] = []
        self.gravity = Vector2(0, config.gravity)
        self.logger = logging.getLogger(__name__)
        
        # 效能優化設置
        self.spatial_hash: dict = {}  # 空間哈希表
        self.hash_cell_size = 64  # 哈希格子大小
        self.broad_phase_enabled = True  # 廣相檢測
        
        # 碰撞檢測相關
        self.collision_pairs: Set[Tuple[int, int]] = set()
        self.collision_callbacks: dict = {}
        
        self.logger.info("物理系統初始化完成（優化版本）")
    
    def add_entity(self, entity) -> None:
        """添加實體到物理系統"""
        if hasattr(entity, 'physics_body'):
            if entity.physics_body not in self.bodies:
                self.bodies.append(entity.physics_body)
                entity.physics_body.wake_up()
                self.logger.debug(f"實體已添加到物理系統: {type(entity).__name__}")
    
    def remove_entity(self, entity) -> None:
        """從物理系統移除實體"""
        if hasattr(entity, 'physics_body') and entity.physics_body in self.bodies:
            self.bodies.remove(entity.physics_body)
            self.logger.debug(f"實體已從物理系統移除: {type(entity).__name__}")
    
    def update(self, dt: float) -> None:
        """更新物理系統"""
        # 更新所有活躍的物理體
        active_bodies = []
        
        for body in self.bodies:
            if not body.is_sleeping:
                self._update_body(body, dt)
                active_bodies.append(body)
                
                # 檢查是否可以休眠
                if body.can_sleep():
                    body.is_sleeping = True
                    self.logger.debug("物理體進入休眠狀態")
        
        # 碰撞檢測
        if self.broad_phase_enabled:
            self._broad_phase_collision_detection()
        
        self._narrow_phase_collision_detection()
        
        # 解決碰撞
        self._resolve_collisions()
    
    def _update_body(self, body: PhysicsBody, dt: float) -> None:
        """更新單個物理體"""
        if body.is_static:
            return
        
        # 重力影響
        if body.affected_by_gravity:
            body.acceleration = body.acceleration + self.gravity
        
        # 更新速度
        body.velocity = body.velocity + body.acceleration * dt
        
        # 摩擦力
        if body.is_grounded:
            body.velocity.x *= body.friction
        
        # 更新位置
        body.last_position = body.position.copy()
        body.position = body.position + body.velocity * dt
        
        # 重置加速度
        body.acceleration = Vector2(0, 0)
        
        # 檢查是否需要更新
        position_change = (body.position - body.last_position).length_squared()
        body.needs_update = position_change > 0.01
    
    def _broad_phase_collision_detection(self) -> None:
        """廣相碰撞檢測（使用空間哈希）"""
        self.spatial_hash.clear()
        self.collision_pairs.clear()
        
        # 將物理體加入空間哈希
        for i, body in enumerate(self.bodies):
            if body.is_sleeping or body.is_static:
                continue
            
            hash_coords = self._get_hash_coordinates(body)
            for coord in hash_coords:
                if coord not in self.spatial_hash:
                    self.spatial_hash[coord] = []
                self.spatial_hash[coord].append((i, body))
        
        # 檢查同一格子內的物體對
        for cell_bodies in self.spatial_hash.values():
            for i in range(len(cell_bodies)):
                for j in range(i + 1, len(cell_bodies)):
                    idx_a, body_a = cell_bodies[i]
                    idx_b, body_b = cell_bodies[j]
                    
                    # 檢查碰撞遮罩
                    if self._can_collide(body_a, body_b):
                        pair = (min(idx_a, idx_b), max(idx_a, idx_b))
                        self.collision_pairs.add(pair)
    
    def _get_hash_coordinates(self, body: PhysicsBody) -> List[Tuple[int, int]]:
        """獲取物理體在空間哈希中的座標"""
        coords = []
        
        # 計算物理體佔據的哈希格子
        min_x = int((body.position.x - body.width / 2) // self.hash_cell_size)
        max_x = int((body.position.x + body.width / 2) // self.hash_cell_size)
        min_y = int((body.position.y - body.height / 2) // self.hash_cell_size)
        max_y = int((body.position.y + body.height / 2) // self.hash_cell_size)
        
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                coords.append((x, y))
        
        return coords
    
    def _can_collide(self, body_a: PhysicsBody, body_b: PhysicsBody) -> bool:
        """檢查兩個物理體是否可以碰撞"""
        return (body_a.collision_mask & (1 << body_b.collision_layer)) != 0 and \
               (body_b.collision_mask & (1 << body_a.collision_layer)) != 0
    
    def _narrow_phase_collision_detection(self) -> None:
        """窄相碰撞檢測（精確檢測）"""
        collisions = []
        
        for pair in self.collision_pairs:
            idx_a, idx_b = pair
            if idx_a < len(self.bodies) and idx_b < len(self.bodies):
                body_a = self.bodies[idx_a]
                body_b = self.bodies[idx_b]
                
                collision_info = self._check_aabb_collision(body_a, body_b)
                if collision_info:
                    collisions.append(collision_info)
        
        self.current_collisions = collisions
    
    def _check_aabb_collision(self, body_a: PhysicsBody, body_b: PhysicsBody) -> Optional[CollisionInfo]:
        """AABB 碰撞檢測"""
        # 計算兩個矩形的邊界
        a_left = body_a.position.x - body_a.width / 2
        a_right = body_a.position.x + body_a.width / 2
        a_top = body_a.position.y - body_a.height / 2
        a_bottom = body_a.position.y + body_a.height / 2
        
        b_left = body_b.position.x - body_b.width / 2
        b_right = body_b.position.x + body_b.width / 2
        b_top = body_b.position.y - body_b.height / 2
        b_bottom = body_b.position.y + body_b.height / 2
        
        # 檢查是否相交
        if (a_right > b_left and a_left < b_right and
            a_bottom > b_top and a_top < b_bottom):
            
            # 計算穿透深度和法向量
            overlap_x = min(a_right - b_left, b_right - a_left)
            overlap_y = min(a_bottom - b_top, b_bottom - a_top)
            
            if overlap_x < overlap_y:
                # 水平碰撞
                normal = Vector2(-1 if a_left < b_left else 1, 0)
                penetration = overlap_x
            else:
                # 垂直碰撞
                normal = Vector2(0, -1 if a_top < b_top else 1)
                penetration = overlap_y
            
            return CollisionInfo(body_a, body_b, normal, penetration)
        
        return None
    
    def _resolve_collisions(self) -> None:
        """解決碰撞"""
        for collision in getattr(self, 'current_collisions', []):
            self._resolve_collision(collision)
    
    def _resolve_collision(self, collision: CollisionInfo) -> None:
        """解決單個碰撞"""
        body_a, body_b = collision.body_a, collision.body_b
        
        # 喚醒休眠的物理體
        body_a.wake_up()
        body_b.wake_up()
        
        # 位置修正
        if not body_a.is_static and not body_b.is_static:
            correction = collision.normal * (collision.penetration / 2)
            body_a.position = body_a.position - correction
            body_b.position = body_b.position + correction
        elif not body_a.is_static:
            correction = collision.normal * collision.penetration
            body_a.position = body_a.position - correction
        elif not body_b.is_static:
            correction = collision.normal * collision.penetration
            body_b.position = body_b.position + correction
        
        # 速度修正（彈性碰撞）
        if not body_a.is_static and not body_b.is_static:
            relative_velocity = body_a.velocity - body_b.velocity
            velocity_along_normal = relative_velocity.dot(collision.normal)
            
            if velocity_along_normal > 0:
                return  # 物體正在分離
            
            restitution = min(body_a.restitution, body_b.restitution)
            impulse_magnitude = -(1 + restitution) * velocity_along_normal
            impulse_magnitude /= (1/body_a.mass + 1/body_b.mass)
            
            impulse = collision.normal * impulse_magnitude
            body_a.velocity = body_a.velocity + impulse / body_a.mass
            body_b.velocity = body_b.velocity - impulse / body_b.mass
        
        # 設置接地狀態
        if collision.normal.y < -0.5:  # 向上的法向量
            if not body_a.is_static:
                body_a.is_grounded = True
            if not body_b.is_static:
                body_b.is_grounded = True
    
    def get_bodies_count(self) -> int:
        """獲取物理體數量"""
        return len(self.bodies)
    
    def get_active_bodies_count(self) -> int:
        """獲取活躍物理體數量"""
        return len([body for body in self.bodies if not body.is_sleeping])
    
    def cleanup(self) -> None:
        """清理物理系統"""
        self.bodies.clear()
        self.spatial_hash.clear()
        self.collision_pairs.clear()
        self.logger.info("物理系統已清理")
