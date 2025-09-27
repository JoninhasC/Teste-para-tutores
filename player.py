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
        # Se você substituir os PNGs por versões maiores, ajuste estes valores para centralizar.
        self.width = 64
        self.height = 128

    def update(self):
        """Update player logic"""
        # Gravity
        self.vy += GRAVITY

        # Position
        self.x += self.vx
        self.y += self.vy

        # Simple ground check
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