import os

# Força abrir a janela centralizada no monitor principal
os.environ['SDL_VIDEO_CENTERED'] = '1'

# configGlobal.py - EXPLICAÇÃO DETALHADA

import pgzrun  # Biblioteca principal do jogo
import random  # Para gerar números aleatórios (inimigos, etc.)
import math    # Para cálculos matemáticos (distâncias, ângulos)

# ===== CONFIGURAÇÕES DO JOGO =====
TILE_SIZE = 64        # Tamanho de cada quadrado do mapa (64x64 pixels)
ROWS = 15            # Número de linhas do mapa
COLS = 30            # Número de colunas do mapa
WIDTH = COLS * TILE_SIZE   # Largura da tela: 30 * 64 = 1920 pixels
HEIGHT = ROWS * TILE_SIZE  # Altura da tela: 15 * 64 = 960 pixels

# ===== ESTADOS DO JOGO =====
# O jogo tem diferentes "telas": menu, jogando, pausado
MENU = 0      # Tela do menu principal
PLAYING = 1   # Tela do jogo
PAUSED = 2    # Tela de pausa

# ===== CONFIGURAÇÕES DE ÁUDIO =====
SOUND_ENABLED = True   # Sons ligados/desligados
MUSIC_ENABLED = True   # Música ligada/desligada

# ===== CONFIGURAÇÕES DE FÍSICA =====
GRAVITY = 0.8          # Força da gravidade (puxa o personagem para baixo)
JUMP_STRENGTH = -15    # Força do pulo (negativo = para cima)
PLAYER_SPEED = 5       # Velocidade de movimento do herói
ENEMY_SPEED = 2        # Velocidade dos inimigos

# ===== CONFIGURAÇÕES DE ANIMAÇÃO =====
ANIMATION_SPEED = 8    # Velocidade das animações (frames por segundo)