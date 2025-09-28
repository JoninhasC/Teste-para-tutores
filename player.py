from configGlobal import *
import configGlobal
import math

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.vx = 0.0
        self.vy = 0.0

        self.on_ground = False
        self.facing_right = True

        self.idle_left_images = ["characters/azul01"]
        self.walk_left_images = ["characters/azul01", "characters/azul02"]
        self.jump_left_images = ["characters/azul01"]

        self.idle_right_images = ["characters/azul01r"]
        self.walk_right_images = ["characters/azul01r", "characters/azul02r"]
        self.jump_right_images = ["characters/azul01r"]

        self.current_animation = "idle"
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8

        self.width = 16
        self.height = 24
        
        self._debug_ticks = 0
        self.lives = MAX_LIVES

    def update(self, level=None):
        self.vy += GRAVITY

        old_x, old_y = self.x, self.y

        if level:
            try:
                self._phase = getattr(level, 'phase', 1)
            except Exception:
                self._phase = 1
            self.x += self.vx
            player_rect_x = (self.x - self.width//2, self.y - self.height//2, self.width, self.height)
            if configGlobal.DEV_MODE:
                solids = level.get_tiles_overlapping(player_rect_x, {"SOLID", "DANGER"})
            else:
                solids = level.get_tiles_overlapping(player_rect_x, {"SOLID"})
            if solids:
                self.x = old_x
                self.vx = 0

            old_y = self.y
            self.y += self.vy
            player_rect_y = (self.x - self.width//2, self.y - self.height//2, self.width, self.height)
            tiles_y = level.get_tiles_overlapping(player_rect_y, {"SOLID", "PLATFORM", "COLLECTIBLE", "DANGER"})
            self.on_ground = False
            for t in tiles_y:
                if t.tile_type == "SOLID" or (t.tile_type == "DANGER" and configGlobal.DEV_MODE):
                    if self.vy > 0:
                        self.y = (t.y) - (self.height // 2)
                    elif self.vy < 0:
                        self.y = (t.y + t.height) + (self.height // 2)
                    self.vy = 0
                    self.on_ground = True
                elif t.tile_type == "PLATFORM":
                    top = t.y
                    feet_prev = old_y + (self.height // 2)
                    feet_now = self.y + (self.height // 2)
                    if self.vy > 0 and feet_prev <= top and feet_now >= top:
                        self.y = top - (self.height // 2)
                        self.vy = 0
                        self.on_ground = True
                elif t.tile_type == "DANGER" and not configGlobal.DEV_MODE:
                    print(f"Player tocou em tile DANGER! Tile ID: {t.tile_id}")
                    self.die()
                elif t.tile_type == "COLLECTIBLE":
                    self.collect_item(t)
        else:
            self.x += self.vx
            self.y += self.vy
            if self.y >= HEIGHT - 100:
                self.y = HEIGHT - 100
                self.vy = 0
                self.on_ground = True
            else:
                self.on_ground = False

        if self.vx > 0:
            self.vx = max(0.0, self.vx - 0.5)
        elif self.vx < 0:
            self.vx = min(0.0, self.vx + 0.5)

        self.update_animation()

        self._clamp_to_screen()
        self._print_debug_position()

    def update_animation(self):
        new_animation = "jump" if not self.on_ground else ("walk" if abs(self.vx) > 0.1 else "idle")

        if new_animation != self.current_animation:
            self.current_animation = new_animation
            self.animation_frame = 0
            self.animation_timer = 0

        images = self.get_current_images()
        if not images:
            return

        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % len(images)

    def get_current_images(self):
        right = self.facing_right
        if self.current_animation == "idle":
            return self.idle_right_images if right else self.idle_left_images
        if self.current_animation == "walk":
            return self.walk_right_images if right else self.walk_left_images
        if self.current_animation == "jump":
            return self.jump_right_images if right else self.jump_left_images
        return self.idle_right_images if right else self.idle_left_images

    def draw(self, screen):
        images = self.get_current_images()
        if not images:
            return

        frame_index = self.animation_frame % len(images)
        image_name = images[frame_index]

        screen.blit(image_name, (self.x - self.width // 2, self.y - self.height // 2))

    def move_left(self):
        self.vx = -PLAYER_SPEED
        self.facing_right = False

    def move_right(self):
        self.vx = PLAYER_SPEED
        self.facing_right = True

    def jump(self):
        if self.on_ground:
            self.vy = JUMP_STRENGTH
            self.on_ground = False
    
    def check_tile_collisions(self, level, old_x, old_y):
        player_rect = (self.x - self.width//2, self.y - self.height//2, 
                       self.width, self.height)
        
        collisions = level.check_collision(player_rect)
        
        if collisions['solid']:
            self.x = old_x
            self.y = old_y
            self.vx = 0
            self.vy = 0
            self.on_ground = True
        
        elif collisions['platform']:
            if self.vy > 0:
                self.y = old_y
                self.vy = 0
                self.on_ground = True
            else:
                self.on_ground = False
        
        if collisions['danger'] and not configGlobal.DEV_MODE:
            self.die()
        
        for tile in collisions['collectible']:
            self.collect_item(tile)
    
    def die(self):
        print(f"Player morreu! DEV_MODE: {configGlobal.DEV_MODE}")
        
        try:
            from main import play_damage_sound
            play_damage_sound()
        except Exception:
            pass
            
        if self.lives > 0:
            self.lives -= 1
        if self.lives <= 0:
            try:
                from configGlobal import GAME_OVER
                import builtins
            except Exception:
                pass
        phase = getattr(self, '_phase', 1)
        if phase == 2:
            self.x = SPAWN2_X
            self.y = SPAWN2_Y
        else:
            self.x = SPAWN_X
            self.y = SPAWN_Y
        self.vx = 0
        self.vy = 0
    
    def collect_item(self, tile):
        print(f"Coletou item: {tile.tile_id}")
        tile.tile_id = -1
        
        try:
            from main import play_collect_sound
            play_collect_sound()
        except Exception:
            pass
            
        if tile.tile_id == -1 and hasattr(self, 'on_collect'):
            try:
                self.on_collect(67)
            except Exception:
                pass

    def _clamp_to_screen(self):
        left = self.width // 2
        right = WIDTH - self.width // 2
        top = self.height // 2
        bottom = HEIGHT - self.height // 2

        if self.x < left:
            self.x = left
            self.vx = 0
        elif self.x > right:
            self.x = right
            self.vx = 0

        if self.y < top:
            self.y = top
            self.vy = 0
        elif self.y > bottom:
            self.y = bottom
            self.vy = 0

    def _print_debug_position(self):
        self._debug_ticks += 1
        if self._debug_ticks % 10 == 0:
            print(f"Player pos -> x: {int(self.x)}  y: {int(self.y)}")