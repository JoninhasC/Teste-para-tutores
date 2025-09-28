from configGlobal import *
from tile import Tile

class Level:
    def __init__(self, phase: int = 1):
        self.phase = phase
        self.platforms = []
        self.objects = []
        self.collectibles = []
        self.decorations = []
        self.tiles = []
        
        self.load_level()
        self.build_collision_map()
    
    def load_level(self):
        print("Carregando mapa...")
        suffix = "02" if self.phase == 2 else ""
        
        if suffix:
            plat_file = "final_plat02.csv"
            obj_file = "final_obj02.csv"
            peg_file = "final_peg02.csv"
            deco_file = "final_deco02.csv"
        else:
            plat_file = "final_plat.csv"
            obj_file = "final_obj.csv"
            peg_file = "final_peg.csv"
            deco_file = "final_deco.csv"
       
        self.load_csv(plat_file, self.platforms, "plataformas")
        self.load_csv(obj_file, self.objects, "objetos")
        self.load_csv(peg_file, self.collectibles, "itens")
        self.load_csv(deco_file, self.decorations, "decorações")
        
        print(f"Mapa carregado: {len(self.platforms)}x{len(self.platforms[0]) if self.platforms else 0}")
    
    def build_collision_map(self):
        print("Construindo mapa de colisão...")
        
        self.tiles = []
        for y in range(ROWS):
            tile_row = []
            for x in range(COLS):
                tile_id = -1
                
                if y < len(self.platforms) and x < len(self.platforms[y]):
                    if self.platforms[y][x] != -1:
                        tile_id = self.platforms[y][x]
                
                if tile_id == -1 and y < len(self.objects) and x < len(self.objects[y]):
                    if self.objects[y][x] != -1:
                        tile_id = self.objects[y][x]
                
                if tile_id == -1 and y < len(self.collectibles) and x < len(self.collectibles[y]):
                    if self.collectibles[y][x] != -1:
                        tile_id = self.collectibles[y][x]
                
                if tile_id == -1 and y < len(self.decorations) and x < len(self.decorations[y]):
                    if self.decorations[y][x] != -1:
                        tile_id = self.decorations[y][x]
                
                layer_name = (
                    "platform" if (y < len(self.platforms) and x < len(self.platforms[y]) and self.platforms[y][x] != -1) else
                    ("object" if (y < len(self.objects) and x < len(self.objects[y]) and self.objects[y][x] != -1) else
                     ("collectible" if (y < len(self.collectibles) and x < len(self.collectibles[y]) and self.collectibles[y][x] != -1) else
                      ("decoration" if (y < len(self.decorations) and x < len(self.decorations[y]) and self.decorations[y][x] != -1) else "empty")))
                )
                tile = Tile(tile_id, x, y, layer_name)
                tile_row.append(tile)
            
            self.tiles.append(tile_row)
        
        print(f"✓ Mapa de colisão construído: {len(self.tiles)}x{len(self.tiles[0]) if self.tiles else 0}")
    
    def load_csv(self, filename, target_list, layer_name):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        tile_row = [int(tile.strip()) for tile in line.split(',')]
                        target_list.append(tile_row)
            print(f"✓ {layer_name}: {filename} carregado com {len(target_list)} linhas")
        except FileNotFoundError:
            print(f"✗ Erro: Arquivo {filename} não encontrado!")
        except Exception as e:
            print(f"✗ Erro ao carregar {filename}: {e}")
    
    def draw(self, screen):
        self.draw_layer(screen, self.platforms, "platform")
        
        self.draw_layer(screen, self.objects, "object")
        
        self.draw_layer(screen, self.collectibles, "collectible")
        
        self.draw_layer(screen, self.decorations, "decoration")
    
    def draw_layer(self, screen, layer_data, layer_type):
        for y, row in enumerate(layer_data):
            for x, tile_id in enumerate(row):
                if tile_id != -1:
                    screen_x = x * TILE_SIZE
                    screen_y = y * TILE_SIZE
                    
                    image_name = f"tile_{tile_id:04d}"
                    
                    try:
                        screen.blit(image_name, (screen_x, screen_y))
                    except:
                        color = self.get_tile_color(tile_id, layer_type)
                        screen.draw.filled_rect(
                            (screen_x, screen_y, TILE_SIZE, TILE_SIZE), 
                            color
                        )
    
    def get_tile_color(self, tile_id, layer_type):
        if layer_type == "platform":
            return (139, 69, 19)
        elif layer_type == "object":
            return (128, 128, 128)
        elif layer_type == "collectible":
            return (255, 215, 0)
        elif layer_type == "decoration":
            return (34, 139, 34)
        return (255, 255, 255)
    
    def get_tile_at(self, x, y):
        if 0 <= y < ROWS and 0 <= x < COLS:
            return self.tiles[y][x]
        return None
    
    def check_collision(self, player_rect):
        collisions = {
            'solid': False,
            'platform': False,
            'danger': False,
            'collectible': []
        }
        
        start_x = max(0, int(player_rect[0] // TILE_SIZE) - 1)
        end_x = min(COLS, int((player_rect[0] + player_rect[2]) // TILE_SIZE) + 2)
        start_y = max(0, int(player_rect[1] // TILE_SIZE) - 1)
        end_y = min(ROWS, int((player_rect[1] + player_rect[3]) // TILE_SIZE) + 2)
        
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = self.get_tile_at(x, y)
                if tile and tile.tile_id != -1:
                    cx, cy, cw, ch = tile.get_collision_rect()
                    
                    if cw <= 0 or ch <= 0:
                        continue
                    if self.rects_collide(player_rect, (cx, cy, cw, ch)):
                        if tile.tile_type == "SOLID":
                            collisions['solid'] = True
                        elif tile.tile_type == "PLATFORM":
                            collisions['platform'] = True
                        elif tile.is_dangerous():
                            collisions['danger'] = True
                        elif tile.is_collectible():
                            collisions['collectible'].append(tile)
        
        return collisions
    
    def rects_collide(self, rect1, rect2):
        return (rect1[0] < rect2[0] + rect2[2] and
                rect1[0] + rect1[2] > rect2[0] and
                rect1[1] < rect2[1] + rect2[3] and
                rect1[1] + rect1[3] > rect2[1])

    def get_tiles_overlapping(self, rect, include_types=None):
        tiles = []
        start_x = max(0, int(rect[0] // TILE_SIZE) - 1)
        end_x = min(COLS, int((rect[0] + rect[2]) // TILE_SIZE) + 2)
        start_y = max(0, int(rect[1] // TILE_SIZE) - 1)
        end_y = min(ROWS, int((rect[1] + rect[3]) // TILE_SIZE) + 2)

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = self.get_tile_at(x, y)
                if not tile or tile.tile_id == -1:
                    continue
                if tile.tile_type in ("DECORATION", "EMPTY"):
                    continue
                if include_types and tile.tile_type not in include_types:
                    continue
                cx, cy, cw, ch = tile.get_collision_rect()
                if cw <= 0 or ch <= 0:
                    continue
                if self.rects_collide(rect, (cx, cy, cw, ch)):
                    tiles.append(tile)
        return tiles