# enemy.py - Sistema de inimigos para o jogo

from configGlobal import *
import math

class Enemy:
    def __init__(self, x, y, enemy_type="a"):
        """Cria um novo inimigo
        enemy_type: "a", "b" (terrestres) ou "p" (voador)
        """
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.width = 16
        self.height = 16
        
        # Velocidade e direção
        self.vx = ENEMY_SPEED * 1.15  if enemy_type != "p" else ENEMY_SPEED * 0.7  # Velocidade mais devagar para terrestres
        self.vy = 0
        self.facing_right = True
        
        # Estado
        self.is_flying = (enemy_type == "p")
        self.health = 1
        self.is_alive = True
        
        # Animação
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10
        
        # Movimento (para inimigos terrestres)
        self.move_timer = 0
        self.move_direction = 1  # 1 = direita, -1 = esquerda
        self.move_duration = 60  # frames para mudar direção
        
        # Limites de movimento para patrulha
        self.patrol_left = x - 50  # Limite esquerdo
        self.patrol_right = x + 50  # Limite direito
        
        # Voo (para inimigo voador)
        self.fly_timer = 0
        self.fly_amplitude = 20  # altura do voo
        self.base_y = y
        
        # Configurar sprites baseado no tipo
        self._setup_sprites()
    
    def _setup_sprites(self):
        """Configura os sprites de animação baseado no tipo de inimigo"""
        base_path = f"characters/{self.enemy_type}"
        

        # Sprites para esquerda (01, 02, 03)
        self.walk_left_images = [
            f"{base_path}01",
            f"{base_path}02", 
            f"{base_path}03"
        ]
        
        # Sprites para direita (01r, 02r, 03r)
        self.walk_right_images = [
            f"{base_path}01r",
            f"{base_path}02r",
            f"{base_path}03r"
        ]
    
    def update(self, level=None):
        """Atualiza a lógica do inimigo"""
        if not self.is_alive:
            return
            
        # Movimento baseado no tipo
        if self.is_flying:
            self._update_flying_movement()
        else:
            self._update_ground_movement(level)
        
        # Atualizar animação
        self._update_animation()
        
        # Limitar à tela
        self._clamp_to_screen()
        
        # Debug: mostrar posição do inimigo A
        if self.enemy_type == "a" and self.move_timer % 30 == 0:  # A cada 30 frames
            print(f"Inimigo A - Pos: x:{int(self.x)}, y:{int(self.y)}, Dir: {self.move_direction}")
    
    def _update_flying_movement(self):
        """Movimento do inimigo voador (padrão senoidal)"""
        self.fly_timer += 1
        
        # Movimento horizontal
        self.x += self.vx
        
        # Movimento vertical (senoidal)
        self.y = self.base_y + math.sin(self.fly_timer * 0.1) * self.fly_amplitude
        
        # Mudar direção nas bordas
        if self.x <= self.width // 2 or self.x >= WIDTH - self.width // 2:
            self.vx = -self.vx
            self.facing_right = self.vx > 0
    
    def _update_ground_movement(self, level):
        """Movimento do inimigo terrestre"""
        self.move_timer += 1
        
        # Salvar posição anterior
        old_x = self.x
        
        # Mover horizontalmente
        self.x += self.vx * self.move_direction
        
        # Aplicar gravidade
        if not self.is_flying:
            self.vy += GRAVITY
            self.y += self.vy
        
        # Verificar colisão com o chão
        if level and not self.is_flying:
            self._check_ground_collision(level)
        
        # Verificar colisão com paredes/obstáculos
        if level:
            self._check_wall_collision(level, old_x)
        
        # Mudar direção periodicamente (backup)
        if self.move_timer >= self.move_duration:
            self.move_direction = -self.move_direction
            self.facing_right = self.move_direction > 0
            self.move_timer = 0
    
    def _check_ground_collision(self, level):
        """Verifica colisão com o chão para inimigos terrestres"""
        enemy_rect = (self.x - self.width//2, self.y - self.height//2, 
                     self.width, self.height)
        
        # Verificar tiles sólidos abaixo
        tiles_below = level.get_tiles_overlapping(enemy_rect, {"SOLID"})
        
        for tile in tiles_below:
            # Se o inimigo está caindo e colidiu com um tile sólido
            if self.vy > 0 and self.y < tile.y:
                self.y = tile.y - self.height // 2
                self.vy = 0
                break
    
    def _check_wall_collision(self, level, old_x):
        """Verifica colisão com paredes e inverte direção"""
        enemy_rect = (self.x - self.width//2, self.y - self.height//2, 
                     self.width, self.height)
        
        # Verificar tiles sólidos na frente
        solid_tiles = level.get_tiles_overlapping(enemy_rect, {"SOLID"})
        
        if solid_tiles:
            # Se colidiu, voltar para posição anterior e inverter direção
            self.x = old_x
            self.move_direction = -self.move_direction
            self.facing_right = self.move_direction > 0
            self.move_timer = 0  # Reset timer
            print(f"Inimigo {self.enemy_type} encontrou parede em x:{int(self.x)}, virando!")
    
    def _update_animation(self):
        """Atualiza a animação do inimigo"""
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 3  # 3 frames de animação
    
    def _clamp_to_screen(self):
        """Mantém o inimigo dentro da tela"""
        # Só limitar nas bordas extremas da tela, não interferir com detecção de paredes
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
    
    def draw(self, screen):
        """Desenha o inimigo na tela"""
        if not self.is_alive:
            return
            
        # Escolher sprites baseado na direção
        images = self.walk_right_images if self.facing_right else self.walk_left_images
        
        if images and self.animation_frame < len(images):
            image_name = images[self.animation_frame]
            screen.blit(image_name, (self.x - self.width // 2, self.y - self.height // 2))
    
    def get_collision_rect(self):
        """Retorna o retângulo de colisão do inimigo"""
        return (self.x - self.width//2, self.y - self.height//2, 
                self.width, self.height)
    
    def take_damage(self, damage=1):
        """Inimigo recebe dano"""
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False
            print(f"Inimigo {self.enemy_type} morreu!")
    
    def deal_damage_to_player(self, player):
        """Causa dano ao player se colidir"""
        if not self.is_alive:
            return False
            
        enemy_rect = self.get_collision_rect()
        player_rect = (player.x - player.width//2, player.y - player.height//2,
                      player.width, player.height)
        
        # Verificar colisão
        if (enemy_rect[0] < player_rect[0] + player_rect[2] and
            enemy_rect[0] + enemy_rect[2] > player_rect[0] and
            enemy_rect[1] < player_rect[1] + player_rect[3] and
            enemy_rect[1] + enemy_rect[3] > player_rect[1]):
            
            player.die()  # Player perde uma vida
            return True
        
        return False
