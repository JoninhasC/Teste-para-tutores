import os

# Força abrir a janela centralizada no monitor principal
os.environ['SDL_VIDEO_CENTERED'] = '1'

# configGlobal.py - EXPLICAÇÃO DETALHADA

# configGlobal.py - Configurações corretas

import pgzrun
import random
import math

# ===== CONFIGURAÇÕES DO JOGO =====
TILE_SIZE = 18        # Tamanho de cada tile (18x18 pixels)
ROWS = 20            # Altura do mapa (20 tiles)
COLS = 30            # Largura do mapa (30 tiles)
WIDTH = COLS * TILE_SIZE   # Largura da tela: 30 * 18 = 540 pixels
HEIGHT = ROWS * TILE_SIZE  # Altura da tela: 20 * 18 = 360 pixels

# ===== ESTADOS DO JOGO =====
MENU = 0
PLAYING = 1
PAUSED = 2
VICTORY = 3
GAME_OVER = 4
CONTROLS = 5

# ===== CONFIGURAÇÕES DE ÁUDIO =====
SOUND_ENABLED = True
MUSIC_ENABLED = True

# ===== CONFIGURAÇÕES DE FÍSICA =====
GRAVITY = 1
JUMP_STRENGTH = -15
PLAYER_SPEED = 3
ENEMY_SPEED = 2

# ===== CONFIGURAÇÕES DE ANIMAÇÃO =====
ANIMATION_SPEED = 8

# ===== SISTEMA DE VIDAS =====
MAX_LIVES = 5

# ===== MODO DEV =====
DEV_MODE = False  # Modo desenvolvedor (imortalidade)

# ===== TIPOS DE TILE PARA COLISÃO =====
# Sistema dinâmico - cada tile_id tem um tipo de colisão
TILE_COLLISION_TYPES = {
    # Sólidos (colisão completa)
    "SOLID": [1, 2, 3, 21, 22,  41, 42, 43,61, 62, 63,  93, 133, 81, 82, 83, 101, 102, 103, 121,  122, 123, 135, 141, 142, 143],
    
    # Plataformas (só colisão por cima)
    "PLATFORM": [],
    
    
    # Perigosos (mata o player)
    "DANGER": [68],
    
    # Coletáveis (sem colisão, só coleta)
    "COLLECTIBLE": [67],
    
    # Decoração (sem colisão)
    "DECORATION": [129, 128, 144, 124, 126, 40, 0, 33, 54, 74],
    
    # Vazio
    "EMPTY": [-1]
}

# ===== POSIÇÃO INICIAL (SPAWN) =====
SPAWN_X = 8
SPAWN_Y = 330
SPAWN2_X = 11
SPAWN2_Y = 294


