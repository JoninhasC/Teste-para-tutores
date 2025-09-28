import pgzrun
from configGlobal import *
import configGlobal
from player import Player
from level import Level
from controls import handle_input
from enemy import Enemy

# ===== VARIÁVEIS GLOBAIS =====
game_state = MENU         
player = None            
enemies = []             
level = None               
menu_buttons = []         
current_phase = 1

# ===== SISTEMA DE PLAYLIST =====
playlist = [
    "jingles_nes00", "jingles_nes01", "jingles_nes02", "jingles_nes03", "jingles_nes04",
    "jingles_nes05", "jingles_nes06", "jingles_nes07", "jingles_nes08", "jingles_nes09",
    "jingles_nes10", "jingles_nes11", "jingles_nes12", "jingles_nes13", "jingles_nes14",
    "jingles_nes15", "jingles_nes16"
]
current_track = 0
playlist_enabled = False
music_timer = 0.0  # Timer para controlar delay entre músicas
music_delay = 1.0  # 1 segundo de delay entre músicas

# ===== SISTEMA DE SONS =====
def play_click_sound():
    """Toca o som de clique se o som estiver habilitado"""
    if SOUND_ENABLED:
        try:
            sounds.click_003.play()
        except Exception as e:
            print(f"Erro ao tocar som: {e}")

def play_collect_sound():
    """Toca som de coleta de item"""
    if SOUND_ENABLED:
        try:
            # Usar o mesmo som de clique para coleta por enquanto
            sounds.click_003.play()
        except Exception as e:
            print(f"Erro ao tocar som de coleta: {e}")

def play_damage_sound():
    """Toca som de dano"""
    if SOUND_ENABLED:
        try:
            # Usar o mesmo som de clique para dano por enquanto
            sounds.click_003.play()
        except Exception as e:
            print(f"Erro ao tocar som de dano: {e}")

# ===== SISTEMA DE PLAYLIST =====
def start_playlist():
    """Inicia a playlist de música em loop"""
    global playlist_enabled, current_track, music_timer
    if MUSIC_ENABLED:
        playlist_enabled = True
        current_track = 0
        music_timer = 0.0  # Reset timer
        play_current_track()

def stop_playlist():
    """Para a playlist de música"""
    global playlist_enabled
    playlist_enabled = False
    try:
        music.stop()
    except Exception as e:
        print(f"Erro ao parar música: {e}")

def play_current_track():
    """Toca a música atual da playlist"""
    if playlist_enabled and MUSIC_ENABLED:
        try:
            track_name = playlist[current_track]
            music.play(track_name)
            print(f"Tocando: {track_name}")
        except Exception as e:
            print(f"Erro ao tocar música {playlist[current_track]}: {e}")

def next_track():
    """Avança para a próxima música da playlist"""
    global current_track, music_timer
    if playlist_enabled:
        current_track = (current_track + 1) % len(playlist)
        music_timer = 0.0  # Reset timer
        play_current_track()          

def draw():
   
    if game_state == MENU:
        draw_menu()        
    elif game_state == PLAYING:
        draw_game()       
    elif game_state == VICTORY:
        draw_victory()
    elif game_state == GAME_OVER:
        draw_game_over()
    elif game_state == CONTROLS:
        draw_controls()

def draw_menu():
    
    screen.clear()  
    screen.fill((50, 50, 100))  
    
   
    screen.draw.text("PLATFORMER GAME", 
                     center=(WIDTH // 2, 80), 
                     fontsize=40, 
                     color="white")
    
    
    screen.draw.text("START GAME", 
                     center=(WIDTH // 2, 150), 
                     fontsize=25, 
                     color="yellow")
    
   
    screen.draw.text("CONTROLS", 
                     center=(WIDTH // 2, 200), 
                     fontsize=25, 
                     color="cyan")
    
    
    sound_text = "SOUND: ON" if SOUND_ENABLED else "SOUND: OFF"
    screen.draw.text(sound_text, 
                     center=(WIDTH // 2, 250), 
                     fontsize=25, 
                     color="white")
    
    
    screen.draw.text("EXIT", 
                     center=(WIDTH // 2, 300), 
                     fontsize=25, 
                     color="red")

def draw_game():
    
    screen.clear()
    screen.fill((100, 150, 200))   
    
  
    if level:
        level.draw(screen)
    
   
    for enemy in enemies:
        if enemy.is_alive:
            enemy.draw(screen)
    
    if player:
        player.draw(screen)
        
        screen.draw.text(f"Vidas: {player.lives}", topleft=(8, 6), fontsize=20, color="white")
        
       
        if configGlobal.DEV_MODE:
            screen.draw.text("DEV MODE - IMORTAL", topleft=(8, 30), fontsize=16, color="lime")
            
        # Mostrar música atual se playlist estiver ativa
        if playlist_enabled and MUSIC_ENABLED:
            current_music = playlist[current_track]
            try:
                if music.is_playing(current_music):
                    screen.draw.text(f"♪ {current_music}", topleft=(8, 54), fontsize=14, color="yellow")
                else:
                    # Mostrar que está aguardando próxima música
                    remaining_time = music_delay - music_timer
                    screen.draw.text(f"⏳ {current_music} ({remaining_time:.1f}s)", topleft=(8, 54), fontsize=14, color="orange")
            except Exception:
                screen.draw.text(f"♪ {current_music}", topleft=(8, 54), fontsize=14, color="yellow")
    

def draw_controls():
   
    screen.clear()
    screen.fill((30, 30, 80))  
    
    
    screen.draw.text("CONTROLES DO JOGO", 
                     center=(WIDTH // 2, 50), 
                     fontsize=30, 
                     color="white")
    
    
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
    
    
    screen.draw.text("ESPECIAIS:", 
                     center=(WIDTH // 2, 210), 
                     fontsize=20, 
                     color="yellow")
    
    screen.draw.text("Q - Modo DEV (Imortal)", 
                     center=(WIDTH // 2, 240), 
                     fontsize=16, 
                     color="lime")
    
    
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
    # Tocar som de clique sempre que clicar
    play_click_sound()
    
    if game_state == MENU:
        handle_menu_click(pos)
    elif game_state == VICTORY:
       
        to_menu()
    elif game_state == GAME_OVER:
        to_menu()
    elif game_state == CONTROLS:
        
        to_menu()

def handle_menu_click(pos):
    """ Processa cliques no menu"""
    x, y = pos 
    
    
    if 130 <= y <= 170 and WIDTH//2 - 80 <= x <= WIDTH//2 + 80:
        start_game()
    
    
    elif 180 <= y <= 220 and WIDTH//2 - 80 <= x <= WIDTH//2 + 80:
        show_controls()
    
    
    elif 230 <= y <= 270 and WIDTH//2 - 80 <= x <= WIDTH//2 + 80:
        toggle_sound()
    
    
    elif 280 <= y <= 320 and WIDTH//2 - 80 <= x <= WIDTH//2 + 80:
        exit()

def start_game():
    """ininicar o jogo"""
    global game_state, player, level, current_phase, enemies
    game_state = PLAYING
    level = Level(current_phase)  
    player = Player(SPAWN_X, SPAWN_Y)
    
    
    create_enemies_for_phase(current_phase)
    
    # Iniciar playlist de música em loop
    start_playlist()
    
   
    def on_collect(item_id):
        if item_id == 67:
            advance_phase()
    player.on_collect = on_collect
    
    player.vx = 0
    player.vy = 0
    player.on_ground = False
    print("Inicializando Game")

def toggle_sound():
    """Ligar/Desligar o som"""
    global SOUND_ENABLED, MUSIC_ENABLED
    SOUND_ENABLED = not SOUND_ENABLED
    MUSIC_ENABLED = not MUSIC_ENABLED
    
    # Parar ou iniciar playlist baseado no estado
    if MUSIC_ENABLED and game_state == PLAYING:
        start_playlist()
    else:
        stop_playlist()
    
    print(f"Som: {'Ligado' if SOUND_ENABLED else 'Desligado'}")

def update(dt):
    """Atualiza a lógica do jogo"""
    if game_state == PLAYING and player:
        player.update(level)  
        handle_input(player, game_state)
        
        
        for enemy in enemies:
            if enemy.is_alive:
                enemy.update(level)
                
                if not configGlobal.DEV_MODE:
                    enemy.deal_damage_to_player(player)
        
        
        if player.lives <= 0 and not configGlobal.DEV_MODE:
            to_game_over()
            
        # Verificar se a música atual terminou e avançar para a próxima
        if playlist_enabled and MUSIC_ENABLED:
            global music_timer
            try:
                # Se não há música tocando, iniciar timer
                current_music = playlist[current_track]
                if not music.is_playing(current_music):
                    music_timer += dt  # Incrementar timer com delta time
                    # Se passou o tempo de delay, avançar para próxima música
                    if music_timer >= music_delay:
                        next_track()
            except Exception as e:
                # Se houver erro, aguardar delay e tentar próxima música
                music_timer += dt
                if music_timer >= music_delay:
                    next_track()
                
    elif game_state == VICTORY:
        
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
        
        create_enemies_for_phase(current_phase)
        
        # Continuar playlist (não mudar música na fase 2)
        print("Fase 2 carregada")
    else:
        game_state = VICTORY
        # Parar playlist e tocar música de vitória
        stop_playlist()
        if MUSIC_ENABLED:
            try:
                music.play("jingles_nes02")
            except Exception as e:
                print(f"Erro ao tocar música de vitória: {e}")
        print("Vitória!")

def to_menu():
    global game_state, current_phase, player, level, enemies
    game_state = MENU
    current_phase = 1
    player = None
    level = None
    enemies = []
    
    # Parar playlist quando voltar ao menu
    stop_playlist()

def to_game_over():
    global game_state
    game_state = GAME_OVER
    
    # Parar playlist e tocar música de game over
    stop_playlist()
    if MUSIC_ENABLED:
        try:
            music.play("jingles_nes03")
        except Exception as e:
            print(f"Erro ao tocar música de game over: {e}")

def show_controls():
   
    global game_state
    game_state = CONTROLS
    print("Mostrando controles do jogo")

def create_enemies_for_phase(phase):
    
    global enemies
    enemies = []
    
    if phase == 1:
       
        enemies.append(Enemy(239, 133, "a"))  
        enemies.append(Enemy(300, 200, "p"))  
    elif phase == 2:
        
        enemies.append(Enemy(299, 150, "a"))  
        enemies.append(Enemy(209, 294, "b"))  
        enemies.append(Enemy(350, 200, "p"))  
    
    print(f"Criados {len(enemies)} inimigos para a Fase {phase}")

# ===== INICIAR O JOGO =====
pgzrun.go()