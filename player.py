from configGlobal import *
import math
from pygame import Rect

class Player:
    def __init__(self, x, y):
        """Cria um novo player x, y = posição inicial """
         # Posição
        self.x = x
        self.y = y
        
        # Velocidade
        self.vx = 0  # velocidade horizontal
        self.vy = 0  # velocidade vertical

        # Animação 
        self.width = 32
        self.height = 48
        self.color = (255, 0, 0)  # vermelho

    def update(self):

        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy

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
    
    def draw(self, screen):
        """Desenha o player na tela"""
    # Desenhar um retângulo simples (por enquanto)
        screen.draw.filled_rect(
        Rect(self.x - self.width//2, self.y - self.height//2, 
             self.width, self.height), 
        self.color)

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

