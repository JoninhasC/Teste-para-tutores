import pgzrun
from configGlobal import *


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
    
    # Título do jogo
    screen.draw.text("PLATFORMER GAME", 
                     center=(WIDTH // 2, 200), 
                     fontsize=60, 
                     color="white")
     # Botão START
    screen.draw.text("START GAME", 
                     center=(WIDTH // 2, 350), 
                     fontsize=40, 
                     color="yellow")
    # Botão SOUND
    sound_text = "SOUND: ON" if SOUND_ENABLED else "SOUND: OFF"
    screen.draw.text(sound_text, 
                     center=(WIDTH // 2, 450), 
                     fontsize=40, 
                     color="white")
    # Botão EXIT
    screen.draw.text("EXIT", 
                     center=(WIDTH // 2, 550),fontsize=40,color="red")

def draw_game():
    """Desenha o jogo"""
    screen.clear()
    screen.fill((100, 150, 200))  # Cor de fundo azul claro
    
    # Por enquanto, só desenhamos um texto
    screen.draw.text("JOGO EM ANDAMENTO", 
                     center=(WIDTH // 2, HEIGHT // 2), 
                     fontsize=50, 
                     color="white")

def on_mouse_down(pos):
    """
    Esta função é chamada quando o jogador clica
    pos = posição do clique (x, y)
    """
    if game_state == MENU:
        handle_menu_click(pos)

def handle_menu_click(pos):
    """ Processa cliques no menun"""
    x,y = pos 
     # Verifica se clicou no botão START (área aproximada)
    if 300 <= y <= 400 and WIDTH//2 - 100 <= x <= WIDTH//2 + 100:
        start_game()
    
    # Verifica se clicou no botão SOUND
    elif 400 <= y <= 500 and WIDTH//2 - 100 <= x <= WIDTH//2 + 100:
        toggle_sound()
    
    # Verifica se clicou no botão EXIT
    elif 500 <= y <= 600 and WIDTH//2 - 100 <= x <= WIDTH//2 + 100:
        exit()


def start_game():
    """ininicar o jogo"""
    global game_state
    game_state = PLAYING
    print("Inicializando Game")

def toggle_sound():
    """Ligar/Desligar o som"""
    global SOUND_ENABLED, MUSIC_ENABLED
    SOUND_ENABLED = not SOUND_ENABLED
    MUSIC_ENABLED = not MUSIC_ENABLED
    print(f"Som: {'Ligado' if SOUND_ENABLED else 'Desligado'}")
   



















# ===== INICIAR O JOGO =====
pgzrun.go()
