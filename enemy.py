from configGlobal import *
import math

class Enemy:
    def __init__(self, x, y, enemy_type="a"):
        # ===== POSIÇÃO E TIPO =====
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.width = 16
        self.height = 16
        
        # ===== CONFIGURAÇÃO DE VELOCIDADE =====
        self.vx = ENEMY_SPEED * 1.15  if enemy_type != "p" else ENEMY_SPEED * 0.7  
        self.vy = 0
        self.facing_right = True
        
        # ===== ESTADO E COMPORTAMENTO =====
        self.is_flying = (enemy_type == "p")
        self.health = 1
        self.is_alive = True
        
        # ===== SISTEMA DE ANIMAÇÃO =====
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10
        
        # ===== SISTEMA DE PATRULHA =====
        self.move_timer = 0
        self.move_direction = 1  
        self.move_duration = 60  
        
        self.patrol_left = x - 50  
        self.patrol_right = x + 50  
        
        # ===== CONFIGURAÇÃO DE VOO =====
        self.fly_timer = 0
        self.fly_amplitude = 20  
        self.base_y = y
        
        self._setup_sprites()
    
    def _setup_sprites(self):
        base_path = f"characters/{self.enemy_type}"
        

        self.walk_left_images = [
            f"{base_path}01",
            f"{base_path}02", 
            f"{base_path}03"
        ]
        
        self.walk_right_images = [
            f"{base_path}01r",
            f"{base_path}02r",
            f"{base_path}03r"
        ]
    
    def update(self, level=None):
        if not self.is_alive:
            return
            
        # ===== ESCOLHER TIPO DE MOVIMENTO =====
        if self.is_flying:
            self._update_flying_movement()
        else:
            self._update_ground_movement(level)
        
        # ===== ATUALIZAR ANIMAÇÃO E LIMITES =====
        self._update_animation()
        
        self._clamp_to_screen()
        
        # ===== DEBUG INIMIGO TIPO A =====
        if self.enemy_type == "a" and self.move_timer % 30 == 0:  
            print(f"Inimigo A - Pos: x:{int(self.x)}, y:{int(self.y)}, Dir: {self.move_direction}")
    
    # ===== MOVIMENTO VOADOR =====
    def _update_flying_movement(self):
        self.fly_timer += 1
        
        self.x += self.vx
        
        self.y = self.base_y + math.sin(self.fly_timer * 0.1) * self.fly_amplitude
        
        if self.x <= self.width // 2 or self.x >= WIDTH - self.width // 2:
            self.vx = -self.vx
            self.facing_right = self.vx > 0
    
    # ===== MOVIMENTO TERRESTRE =====
    def _update_ground_movement(self, level):
        self.move_timer += 1
        
        old_x = self.x
        
        self.x += self.vx * self.move_direction
        
        if not self.is_flying:
            self.vy += GRAVITY
            self.y += self.vy
        
        if level and not self.is_flying:
            self._check_ground_collision(level)
        
        if level:
            self._check_wall_collision(level, old_x)
        
        if self.move_timer >= self.move_duration:
            self.move_direction = -self.move_direction
            self.facing_right = self.move_direction > 0
            self.move_timer = 0
    
    # ===== SISTEMA DE COLISÃO COM O CHÃO =====
    def _check_ground_collision(self, level):
        # Caixa do inimigo é usada para limitar queda quando encontra piso sólido
        enemy_rect = (self.x - self.width//2, self.y - self.height//2, 
                     self.width, self.height)
        
        tiles_below = level.get_tiles_overlapping(enemy_rect, {"SOLID"})
        
        for tile in tiles_below:
            if self.vy > 0 and self.y < tile.y:
                self.y = tile.y - self.height // 2
                self.vy = 0
                break
    
    # ===== SISTEMA DE COLISÃO COM PAREDES =====
    def _check_wall_collision(self, level, old_x):
        # Impede que o inimigo atravesse paredes invertendo a direção da patrulha
        enemy_rect = (self.x - self.width//2, self.y - self.height//2, 
                     self.width, self.height)
        
        solid_tiles = level.get_tiles_overlapping(enemy_rect, {"SOLID"})
        
        if solid_tiles:
            self.x = old_x
            self.move_direction = -self.move_direction
            self.facing_right = self.move_direction > 0
            self.move_timer = 0
            print(f"Inimigo {self.enemy_type} encontrou parede em x:{int(self.x)}, virando!")
    
    # ===== SISTEMA DE ANIMAÇÃO =====
    def _update_animation(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 3
    
    # ===== LIMITE DA TELA =====
    def _clamp_to_screen(self):
        if self.x < self.width // 2:
            self.x = self.width // 2
            self.move_direction = 1
            self.facing_right = True
            print(f"Inimigo {self.enemy_type} atingiu borda esquerda da tela")
        elif self.x > WIDTH - self.width // 2:
            self.x = WIDTH - self.width // 2
            self.move_direction = -1
            self.facing_right = False
            print(f"Inimigo {self.enemy_type} atingiu borda direita da tela")
    
    # ===== RENDERIZAÇÃO =====
    def draw(self, screen):
        if not self.is_alive:
            return
            
        images = self.walk_right_images if self.facing_right else self.walk_left_images
        
        if images and self.animation_frame < len(images):
            image_name = images[self.animation_frame]
            screen.blit(image_name, (self.x - self.width // 2, self.y - self.height // 2))
    
    # ===== SISTEMA DE COLISÃO =====
    def get_collision_rect(self):
        return (self.x - self.width//2, self.y - self.height//2, 
                self.width, self.height)
    
    # ===== SISTEMA DE VIDA =====
    def take_damage(self, damage=1):
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False
            print(f"Inimigo {self.enemy_type} morreu!")
    
    # ===== SISTEMA DE DANO AO JOGADOR =====
    def deal_damage_to_player(self, player):
        if not self.is_alive:
            return False
            
        enemy_rect = self.get_collision_rect()
        player_rect = (player.x - player.width//2, player.y - player.height//2,
                      player.width, player.height)
        
        # Teste AABB simples evita dependência de bibliotecas externas
        if (enemy_rect[0] < player_rect[0] + player_rect[2] and
            enemy_rect[0] + enemy_rect[2] > player_rect[0] and
            enemy_rect[1] < player_rect[1] + player_rect[3] and
            enemy_rect[1] + enemy_rect[3] > player_rect[1]):
            
            player.die()
            return True
        
        return False
