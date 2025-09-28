from pgzero.builtins import keyboard
from configGlobal import *

# ===== CONTROLE DE ENTRADA =====
def handle_input(player, game_state):
    if game_state == 1 and player:
        # ===== MOVIMENTO HORIZONTAL =====
        if keyboard.left or keyboard.a:
            player.move_left()
        elif keyboard.right or keyboard.d:
            player.move_right()

        # ===== CONTROLES DE PULO =====
        if keyboard.space or keyboard.up or keyboard.w:
            player.jump()
        
        # ===== CONTROLES ESPECIAIS =====
        if keyboard.q:
            print("Botão Q pressionado!")
            toggle_dev_mode()

# ===== SISTEMA DE MODO DESENVOLVEDOR =====
def toggle_dev_mode():
    import configGlobal
    configGlobal.DEV_MODE = not configGlobal.DEV_MODE
    status = "ATIVADO" if configGlobal.DEV_MODE else "DESATIVADO"
    print(f"Modo DEV {status} - Player {'imortal' if configGlobal.DEV_MODE else 'mortal'}")
    print(f"Valor atual de DEV_MODE: {configGlobal.DEV_MODE}")
    
    try:
        from main import play_click_sound
        play_click_sound()
    except Exception:
        pass
