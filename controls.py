from pgzero.builtins import keyboard
from configGlobal import *

def handle_input(player, game_state):
    if game_state == 1 and player:
        if keyboard.left or keyboard.a:
            player.move_left()
        elif keyboard.right or keyboard.d:
            player.move_right()

        if keyboard.space or keyboard.up or keyboard.w:
            player.jump()
        
        if keyboard.q:
            print("Botão Q pressionado!")
            toggle_dev_mode()

def toggle_dev_mode():
    """Alterna o modo desenvolvedor (imortalidade)"""
    import configGlobal
    configGlobal.DEV_MODE = not configGlobal.DEV_MODE
    status = "ATIVADO" if configGlobal.DEV_MODE else "DESATIVADO"
    print(f"Modo DEV {status} - Player {'imortal' if configGlobal.DEV_MODE else 'mortal'}")
    print(f"Valor atual de DEV_MODE: {configGlobal.DEV_MODE}")
    
    # Tocar som de clique quando alternar modo DEV
    try:
        from main import play_click_sound
        play_click_sound()
    except Exception:
        pass
