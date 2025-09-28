# main.py - Ajustado para as novas dimensões

import pgzrun
from configGlobal import *
import configGlobal
from player import Player
from level import Level
from controls import handle_input
from enemy import Enemy

# ===== VARIÁVEIS GLOBAIS =====
game_state = MENU          # Estado atual do jogo (começa no menu)
player = None              # Objeto do herói (será criado depois)
enemies = []               # Lista de inimigos
level = None               # Objeto do nível/mapa
menu_buttons = []          # Lista de botões do menu
current_phase = 1          # Fase atual

def draw():
    """
    Esta função é chamada automaticamente pelo PGZero
    Ela desenha tudo na tela
    """
    if game_state == MENU:
        draw_menu()        # Desenha o menu principal
    elif game_state == PLAYING:
        draw_game()        # Desenha o jogo
    elif game_state == VICTORY:
        draw_victory()
    elif game_state == GAME_OVER:
        draw_game_over()
    elif game_state == CONTROLS:
        draw_controls()    # Desenha a tela de controles

def draw_menu():
    """Desenha o menu principal"""
    screen.clear()  # Limpa a tela
    screen.fill((50, 50, 100))  # Cor de fundo azul escuro
    
    # Título do jogo
    screen.draw.text("PLATFORMER GAME", 
                     center=(WIDTH // 2, 80), 
                     fontsize=40, 
                     color="white")
    
    # Botão START
    screen.draw.text("START GAME", 
                     center=(WIDTH // 2, 150), 
                     fontsize=25, 
                     color="yellow")
    
    # Botão CONTROLS
    screen.draw.text("CONTROLS", 
                     center=(WIDTH // 2, 200), 
                     fontsize=25, 
                     color="cyan")
    
    # Botão SOUND
    sound_text = "SOUND: ON" if SOUND_ENABLED else "SOUND: OFF"
    screen.draw.text(sound_text, 
                     center=(WIDTH // 2, 250), 
                     fontsize=25, 
                     color="white")
    
    # Botão EXIT
    screen.draw.text("EXIT", 
                     center=(WIDTH // 2, 300), 
                     fontsize=25, 
                     color="red")

def draw_game():
    """Desenha o jogo"""
    screen.clear()
    screen.fill((100, 150, 200))  # Cor de fundo azul claro
    
    # Desenhar o mapa primeiro (fundo)
    if level:
        level.draw(screen)
    
    # Desenhar inimigos
    for enemy in enemies:
        if enemy.is_alive:
            enemy.draw(screen)
    
    # Desenhar o player por cima
    if player:
        player.draw(screen)
        # HUD de vidas (canto superior esquerdo)
        screen.draw.text(f"Vidas: {player.lives}", topleft=(8, 6), fontsize=20, color="white")
        
        # Indicador de modo DEV
        if configGlobal.DEV_MODE:
            screen.draw.text("DEV MODE - IMORTAL", topleft=(8, 30), fontsize=16, color="lime")
    

def draw_controls():
    """Desenha a tela de controles"""
    screen.clear()
    screen.fill((30, 30, 80))  # Cor de fundo azul escuro
    
    # Título
    screen.draw.text("CONTROLES DO JOGO", 
                     center=(WIDTH // 2, 50), 
                     fontsize=30, 
                     color="white")
    
    # Controles de movimento
    screen.draw.text("MOVIMENTO:", 
                     center=(WIDTH // 2, 100), 
                     fontsize=20, 
                     color="yellow")
    
    screen.draw.text("A / seta para esquerda - Mover para esquerda", 
                     center=(WIDTH // 2, 130), 
                     fontsize=16, 
                     color="white")
    
    screen.draw.text("D / seta para direita - Mover para direita", 
                     center=(WIDTH // 2, 150), 
                     fontsize=16, 
                     color="white")
    
    screen.draw.text("W / seta para cima/ ESPAÇO - Pular", 
                     center=(WIDTH // 2, 170), 
                     fontsize=16, 
                     color="white")
    
    # Controles especiais
    screen.draw.text("ESPECIAIS:", 
                     center=(WIDTH // 2, 210), 
                     fontsize=20, 
                     color="yellow")
    
    screen.draw.text("Q - Modo DEV (Imortal)", 
                     center=(WIDTH // 2, 240), 
                     fontsize=16, 
                     color="lime")
    
    # Botão voltar
    screen.draw.text("Clique para voltar ao MENU", 
                     center=(WIDTH // 2, 320), 
                     fontsize=18, 
                     color="cyan")

def draw_victory():
    screen.clear()
    screen.fill((20, 90, 40))
    screen.draw.text("Parabéns! Você concluiu o jogo!", center=(WIDTH // 2, 120), fontsize=28, color="white")
    screen.draw.text("Clique para voltar ao MENU", center=(WIDTH // 2, 180), fontsize=20, color="yellow")
    screen.draw.text("Ou pressione ESC para sair", center=(WIDTH // 2, 220), fontsize=18, color="white")

def draw_game_over():
    screen.clear()
    screen.fill((120, 30, 30))
    screen.draw.text("Você perdeu!", center=(WIDTH // 2, 120), fontsize=32, color="white")
    screen.draw.text("Clique para voltar ao MENU", center=(WIDTH // 2, 180), fontsize=20, color="yellow")
    screen.draw.text("Ou pressione ESC para sair", center=(WIDTH // 2, 220), fontsize=18, color="white")

def on_mouse_down(pos):
    """
    Esta função é chamada quando o jogador clica
    pos = posição do clique (x, y)
    """
    if game_state == MENU:
        handle_menu_click(pos)
    elif game_state == VICTORY:
        # Voltar ao menu
        to_menu()
    elif game_state == GAME_OVER:
        to_menu()
    elif game_state == CONTROLS:
        # Voltar ao menu
        to_menu()

def handle_menu_click(pos):
    """ Processa cliques no menu"""
    x, y = pos 
    
    # Verifica se clicou no botão START
    if 130 <= y <= 170 and WIDTH//2 - 80 <= x <= WIDTH//2 + 80:
        start_game()
    
    # Verifica se clicou no botão CONTROLS
    elif 180 <= y <= 220 and WIDTH//2 - 80 <= x <= WIDTH//2 + 80:
        show_controls()
    
    # Verifica se clicou no botão SOUND
    elif 230 <= y <= 270 and WIDTH//2 - 80 <= x <= WIDTH//2 + 80:
        toggle_sound()
    
    # Verifica se clicou no botão EXIT
    elif 280 <= y <= 320 and WIDTH//2 - 80 <= x <= WIDTH//2 + 80:
        exit()

def start_game():
    """ininicar o jogo"""
    global game_state, player, level, current_phase, enemies
    game_state = PLAYING
    level = Level(current_phase)  # Carrega fase atual
    player = Player(SPAWN_X, SPAWN_Y)
    
    # Criar inimigos para a fase atual
    create_enemies_for_phase(current_phase)
    
    # Registrar callback de coleta para avançar de fase
    def on_collect(item_id):
        if item_id == 67:
            advance_phase()
    player.on_collect = on_collect
    # reset de estado ao iniciar
    player.vx = 0
    player.vy = 0
    player.on_ground = False
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
        
        # Atualizar inimigos
        for enemy in enemies:
            if enemy.is_alive:
                enemy.update(level)
                # Verificar colisão com player (só se não estiver em modo DEV)
                if not configGlobal.DEV_MODE:
                    enemy.deal_damage_to_player(player)
        
        # Se vidas acabarem, game over (só se não estiver em modo DEV)
        if player.lives <= 0 and not configGlobal.DEV_MODE:
            to_game_over()
    elif game_state == VICTORY:
        # permitir sair com ESC
        try:
            from pgzero.builtins import keyboard
            if keyboard.escape:
                exit()
        except Exception:
            pass
    elif game_state == GAME_OVER:
        try:
            from pgzero.builtins import keyboard
            if keyboard.escape:
                exit()
        except Exception:
            pass

def advance_phase():
    """Avança para próxima fase ou mostra vitória."""
    global current_phase, level, player, game_state, enemies
    if current_phase == 1:
        current_phase = 2
        level = Level(current_phase)
        player.x, player.y = SPAWN2_X, SPAWN2_Y
        player.vx = 0
        player.vy = 0
        player.on_ground = False
        # Criar inimigos para a nova fase
        create_enemies_for_phase(current_phase)
        print("Fase 2 carregada")
    else:
        game_state = VICTORY
        print("Vitória!")

def to_menu():
    global game_state, current_phase, player, level, enemies
    game_state = MENU
    current_phase = 1
    player = None
    level = None
    enemies = []

def to_game_over():
    global game_state
    game_state = GAME_OVER

def show_controls():
    """Mostra a tela de controles"""
    global game_state
    game_state = CONTROLS
    print("Mostrando controles do jogo")

def create_enemies_for_phase(phase):
    """Cria inimigos para a fase especificada"""
    global enemies
    enemies = []
    
    if phase == 1:
        # Fase 1: 1 inimigo de cada tipo
        # Inimigo A que anda até encontrar parede
        enemies.append(Enemy(239, 133, "a"))  # Inimigo terrestre A
        enemies.append(Enemy(300, 200, "p"))  # Inimigo voador P
    elif phase == 2:
        # Fase 2: 1 inimigo de cada tipo em posições diferentes
        enemies.append(Enemy(299, 150, "a"))  # Inimigo terrestre A
        enemies.append(Enemy(209, 294, "b"))  # Inimigo terrestre B
        enemies.append(Enemy(350, 180, "p"))  # Inimigo voador P
    
    print(f"Criados {len(enemies)} inimigos para a Fase {phase}")

# ===== INICIAR O JOGO =====
pgzrun.go()