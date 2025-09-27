from pgzero.builtins import keyboard

def handle_input(player, game_state):
    if game_state == 1 and player:
        if keyboard.left or keyboard.a:
            player.move_left()
        elif keyboard.right or keyboard.d:
            player.move_right()

        if keyboard.space or keyboard.up or keyboard.w:
            player.jump()
