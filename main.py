# main.py - Ajustado para as novas dimensões

import pgzrun
from configGlobal import *
from player import Player
from level import Level
from controls import handle_input

# ===== VARIÁVEIS GLOBAIS =====
game_state = MENU          # Estado atual do jogo (começa no menu)
player = None              # Objeto do herói (será criado depois)
enemies = []               # Lista de inimigos
level = None               # Objeto do nível/mapa
menu_buttons = []          # Lista de botões do menu

def draw():
    """
    Esta função é chamada automaticamente pelo PGZero
    Ela desenha tudo na tela
    """
    if game_state == MENU:
        draw_menu()        # Desenha o menu principal
    elif game_state == PLAYING:
        draw_game()        # Desenha o jogo

def draw_menu():
    """Desenha o menu principal"""
    screen.clear()  # Limpa a tela
    screen.fill((50, 50, 100))  # Cor de fundo azul escuro
    
    # Título do jogo (ajustado para tela menor)
    screen.draw.text("PLATFORMER GAME", 
                     center=(WIDTH // 2, 80), 
                     fontsize=40, 
                     color="white")
    
    # Botão START (ajustado)
    screen.draw.text("START GAME", 
                     center=(WIDTH // 2, 150), 
                     fontsize=25, 
                     color="yellow")
    
    # Botão SOUND (ajustado)
    sound_text = "SOUND: ON" if SOUND_ENABLED else "SOUND: OFF"
    screen.draw.text(sound_text, 
                     center=(WIDTH // 2, 200), 
                     fontsize=25, 
                     color="white")
    
    # Botão EXIT (ajustado)
    screen.draw.text("EXIT", 
                     center=(WIDTH // 2, 250), 
                     fontsize=25, 
                     color="red")

def draw_game():
    """Desenha o jogo"""
    screen.clear()
    screen.fill((100, 150, 200))  # Cor de fundo azul claro
    
    # Desenhar o mapa primeiro (fundo)
    if level:
        level.draw(screen)
    
    # Desenhar o player por cima
    if player:
        player.draw(screen)
    
   

def on_mouse_down(pos):
    """
    Esta função é chamada quando o jogador clica
    pos = posição do clique (x, y)
    """
    if game_state == MENU:
        handle_menu_click(pos)

def handle_menu_click(pos):
    """ Processa cliques no menu"""
    x, y = pos 
    
    # Verifica se clicou no botão START (área ajustada)
    if 120 <= y <= 180 and WIDTH//2 - 80 <= x <= WIDTH//2 + 80:
        start_game()
    
    # Verifica se clicou no botão SOUND
    elif 170 <= y <= 230 and WIDTH//2 - 80 <= x <= WIDTH//2 + 80:
        toggle_sound()
    
    # Verifica se clicou no botão EXIT
    elif 220 <= y <= 280 and WIDTH//2 - 80 <= x <= WIDTH//2 + 80:
        exit()

def start_game():
    """ininicar o jogo"""
    global game_state, player, level
    game_state = PLAYING
    player = Player(SPAWN_X, SPAWN_Y)  # Cria o player na posição definida
    level = Level()  # Cria o sistema de níveis
    print("Inicializando Game")

def toggle_sound():
    """Ligar/Desligar o som"""
    global SOUND_ENABLED, MUSIC_ENABLED
    SOUND_ENABLED = not SOUND_ENABLED
    MUSIC_ENABLED = not MUSIC_ENABLED
    print(f"Som: {'Ligado' if SOUND_ENABLED else 'Desligado'}")

def update(dt):
    """Atualiza a lógica do jogo"""
    if game_state == PLAYING and player:
        player.update(level)  # Passa o level para o player
        handle_input(player, game_state)

# ===== INICIAR O JOGO =====
pgzrun.go()