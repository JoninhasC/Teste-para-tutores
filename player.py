# player.py - Classe do herói do jogo (compatível com PgZero)

from configGlobal import *
import math

class Player:
    def __init__(self, x, y):
        """Create a new player"""
        # Position
        self.x = x
        self.y = y

        # Velocity
        self.vx = 0.0
        self.vy = 0.0

        # State
        self.on_ground = False
        self.facing_right = True

        # Animation lists (PgZero: coloque os PNGs em images/characters/ e referencie sem .png)
        # Esquerda (originais)
        self.idle_left_images = ["characters/azul01"]
        self.walk_left_images = ["characters/azul01", "characters/azul02"]
        self.jump_left_images = ["characters/azul01"]

        # Direita (espelhadas) -> crie os arquivos espelhados: azul01_r.png, azul02_r.png
        # Se ainda não tiver os arquivos, você pode temporariamente repetir as imagens da esquerda,
        # mas o personagem não parecerá espelhado até você adicionar as versões _r.
        self.idle_right_images = ["characters/azul01r"]
        self.walk_right_images = ["characters/azul01r", "characters/azul02r"]
        self.jump_right_images = ["characters/azul01r"]

        # Animation control
        self.current_animation = "idle"  # "idle", "walk", "jump"
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8  # ticks per frame

        # Logical sprite size used only for centering offsets (não muda o tamanho real da imagem)
        # Ajustado para ser compatível com tiles de 18x18
        self.width = 16  # Menor que o tile (18)
        self.height = 24  # Maior que o tile para parecer mais realista
        
        # Debug
        self._debug_ticks = 0

    def update(self, level=None):
        """Update player logic (colisão separada por eixos e plataformas top-only)."""
        # Gravity
        self.vy += GRAVITY

        # Salvar posição anterior
        old_x, old_y = self.x, self.y

        if level:
            # guardar fase atual para respawn
            try:
                self._phase = getattr(level, 'phase', 1)
            except Exception:
                self._phase = 1
            # --- mover no eixo X ---
            self.x += self.vx
            player_rect_x = (self.x - self.width//2, self.y - self.height//2, self.width, self.height)
            # Colidir só com sólidos no eixo X
            solids = level.get_tiles_overlapping(player_rect_x, {"SOLID"})
            if solids:
                # Recuar no X ao ponto anterior
                self.x = old_x
                self.vx = 0

            # --- mover no eixo Y ---
            old_y = self.y
            self.y += self.vy
            player_rect_y = (self.x - self.width//2, self.y - self.height//2, self.width, self.height)
            # Checar sólidos e plataformas
            tiles_y = level.get_tiles_overlapping(player_rect_y, {"SOLID", "PLATFORM", "DANGER", "COLLECTIBLE"})
            # Reset estado de chão; será setado se pousar
            self.on_ground = False
            for t in tiles_y:
                if t.tile_type == "SOLID":
                    # Se descendo, pousa no topo; se subindo, bate na parte de baixo
                    if self.vy > 0:
                        self.y = (t.y) - (self.height // 2)
                    elif self.vy < 0:
                        self.y = (t.y + t.height) + (self.height // 2)
                    self.vy = 0
                    self.on_ground = True
                elif t.tile_type == "PLATFORM":
                    # Plataforma só bloqueia quando descendo e quando o pé cruzou o topo da plataforma
                    top = t.y
                    feet_prev = old_y + (self.height // 2)
                    feet_now = self.y + (self.height // 2)
                    if self.vy > 0 and feet_prev <= top and feet_now >= top:
                        self.y = top - (self.height // 2)
                        self.vy = 0
                        self.on_ground = True
                elif t.tile_type == "DANGER":
                    self.die()
                elif t.tile_type == "COLLECTIBLE":
                    self.collect_item(t)
        else:
            # Fallback: colisão simples com chão
            self.x += self.vx
            self.y += self.vy
            if self.y >= HEIGHT - 100:
                self.y = HEIGHT - 100
                self.vy = 0
                self.on_ground = True
            else:
                self.on_ground = False

        # Horizontal friction
        if self.vx > 0:
            self.vx = max(0.0, self.vx - 0.5)
        elif self.vx < 0:
            self.vx = min(0.0, self.vx + 0.5)

        # Animation
        self.update_animation()

        # Limitar à tela e imprimir posição (debug)
        self._clamp_to_screen()
        self._print_debug_position()

    def update_animation(self):
        """Update animation state and frame"""
        new_animation = "jump" if not self.on_ground else ("walk" if abs(self.vx) > 0.1 else "idle")

        # Reset when animation changes to avoid invalid frame index
        if new_animation != self.current_animation:
            self.current_animation = new_animation
            self.animation_frame = 0
            self.animation_timer = 0

        images = self.get_current_images()
        if not images:
            return

        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % len(images)

    def get_current_images(self):
        """Choose images by animation and facing direction"""
        right = self.facing_right
        if self.current_animation == "idle":
            return self.idle_right_images if right else self.idle_left_images
        if self.current_animation == "walk":
            return self.walk_right_images if right else self.walk_left_images
        if self.current_animation == "jump":
            return self.jump_right_images if right else self.jump_left_images
        # fallback
        return self.idle_right_images if right else self.idle_left_images

    def draw(self, screen):
        """Draw the player"""
        images = self.get_current_images()
        if not images:
            return

        frame_index = self.animation_frame % len(images)
        image_name = images[frame_index]

        # Em PgZero, desenhe pelo nome do recurso (sem flip, sem extensão).
        # A imagem deve existir em images/characters/<arquivo>.png
        screen.blit(image_name, (self.x - self.width // 2, self.y - self.height // 2))

    def move_left(self):
        """Move player left"""
        self.vx = -PLAYER_SPEED
        self.facing_right = False

    def move_right(self):
        """Move player right"""
        self.vx = PLAYER_SPEED
        self.facing_right = True

    def jump(self):
        """Make the player jump"""
        if self.on_ground:
            self.vy = JUMP_STRENGTH
            self.on_ground = False
    
    def check_tile_collisions(self, level, old_x, old_y):
        """Verifica colisões com tiles do cenário"""
        # Criar retângulo do player
        player_rect = (self.x - self.width//2, self.y - self.height//2, 
                       self.width, self.height)
        
        # Verificar colisões
        collisions = level.check_collision(player_rect)
        
        # Colisão sólida - reverter movimento
        if collisions['solid']:
            self.x = old_x
            self.y = old_y
            self.vx = 0
            self.vy = 0
            self.on_ground = True
        
        # Plataforma - só colisão por cima
        elif collisions['platform']:
            if self.vy > 0:  # Caindo
                self.y = old_y
                self.vy = 0
                self.on_ground = True
            else:
                self.on_ground = False
        
        # Perigo - mata o player
        if collisions['danger']:
            self.die()
        
        # Coletáveis
        for tile in collisions['collectible']:
            self.collect_item(tile)
    
    def die(self):
        """Player morre"""
        print("Player morreu!")
        # Por enquanto, só reseta a posição
        phase = getattr(self, '_phase', 1)
        if phase == 2:
            self.x = SPAWN2_X
            self.y = SPAWN2_Y
        else:
            self.x = SPAWN_X
            self.y = SPAWN_Y
        self.vx = 0
        self.vy = 0
    
    def collect_item(self, tile):
        """Coleta um item e sinaliza evento para troca de fase se for o 67."""
        print(f"Coletou item: {tile.tile_id}")
        tile.tile_id = -1
        if tile.tile_id == -1 and hasattr(self, 'on_collect'):
            # Notificar jogo do item coletado com o id original
            try:
                self.on_collect(67)
            except Exception:
                pass

    # Utilitários
    def _clamp_to_screen(self):
        """Mantém o player dentro da tela."""
        left = self.width // 2
        right = WIDTH - self.width // 2
        top = self.height // 2
        bottom = HEIGHT - self.height // 2

        if self.x < left:
            self.x = left
            self.vx = 0
        elif self.x > right:
            self.x = right
            self.vx = 0

        if self.y < top:
            self.y = top
            self.vy = 0
        elif self.y > bottom:
            self.y = bottom
            self.vy = 0

    def _print_debug_position(self):
        """Imprime posição no terminal em baixa frequência para facilitar depuração."""
        self._debug_ticks += 1
        if self._debug_ticks % 10 == 0:  # reduz spam
            print(f"Player pos -> x: {int(self.x)}  y: {int(self.y)}")