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

# ===== CONFIGURAÇÕES DE ÁUDIO =====
SOUND_ENABLED = True
MUSIC_ENABLED = True

# ===== CONFIGURAÇÕES DE FÍSICA =====
GRAVITY = 0.8
JUMP_STRENGTH = -15
PLAYER_SPEED = 5
ENEMY_SPEED = 2

# ===== CONFIGURAÇÕES DE ANIMAÇÃO =====
ANIMATION_SPEED = 8