# player.py - Classe do herói do jogo

from configGlobal import *
import math

class Player:
    def __init__(self, x, y):
        """Cria um novo player"""
        # Posição
        self.x = x
        self.y = y
        
        # Velocidade
        self.vx = 0  # velocidade horizontal
        self.vy = 0  # velocidade vertical
        
        # Estado
        self.on_ground = False  # se está no chão
        self.facing_right = True  # direção que está olhando
        
        # Animação - usando os sprites corretos com nomes em minúsculo
        self.idle_images = ["characters/azul01.png"]  # Sprite de idle
        self.walk_images = ["characters/azul01.png", 
                           "characters/azul02.png"]  # Sprites de caminhada
        self.jump_images = ["characters/azul01.png"]  # Sprite de pulo
        
        self.current_animation = "idle"
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8
        
        # Tamanho do sprite (ajustado para 128x256)
        self.width = 64  # Metade da largura original
        self.height = 128  # Metade da altura original
        
        
    def update(self):
        """Atualiza a lógica do player"""
        # Aplicar gravidade
        self.vy += GRAVITY
        
        # Atualizar posição
        self.x += self.vx
        self.y += self.vy
        
        # Verificar se está no chão (por enquanto, chão fixo)
        if self.y >= HEIGHT - 100:  # 100 pixels do chão
            self.y = HEIGHT - 100
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
        # Limitar velocidade horizontal
        if self.vx > 0:
            self.vx = max(0, self.vx - 0.5)  # freio
        elif self.vx < 0:
            self.vx = min(0, self.vx + 0.5)  # freio
        
        # Atualizar animação
        self.update_animation()
    
    def update_animation(self):
        """Atualiza a animação do player"""
        # Determinar qual animação usar
        if not self.on_ground:
            self.current_animation = "jump"
        elif abs(self.vx) > 0.1:
            self.current_animation = "walk"
        else:
            self.current_animation = "idle"
        
        # Atualizar frame da animação
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % len(self.get_current_images())
    
    def get_current_images(self):
        """Retorna as imagens da animação atual"""
        if self.current_animation == "idle":
            return self.idle_images
        elif self.current_animation == "walk":
            return self.walk_images
        elif self.current_animation == "jump":
            return self.jump_images
        return self.idle_images
    
    def draw(self, screen):
        """Desenha o player na tela"""
        # Obter imagem atual
        current_images = self.get_current_images()
        current_image = current_images[self.animation_frame]
        
        # Desenhar sprite
        if self.facing_right:
            screen.blit(current_image, (self.x - self.width//2, self.y - self.height//2))
        else:
            # Virar sprite horizontalmente
            screen.blit(current_image, (self.x - self.width//2, self.y - self.height//2), 
                      flipx=True)
    
    def move_left(self):
        """Move o player para a esquerda"""
        self.vx = -PLAYER_SPEED
        self.facing_right = False
    
    def move_right(self):
        """Move o player para a direita"""
        self.vx = PLAYER_SPEED
        self.facing_right = True
    
    def jump(self):
        """Faz o player pular"""
        if self.on_ground:
            self.vy = JUMP_STRENGTH
            self.on_ground = False