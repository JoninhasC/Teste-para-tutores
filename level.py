# level.py - Sistema de geração de níveis com colisão dinâmica

from configGlobal import *
from tile import Tile
import os
import csv

class Level:
    def __init__(self, phase: int = 1):
        """Inicializa o sistema de níveis. phase=1 usa CSVs padrão; phase=2 usa arquivos *02.csv."""
        self.phase = phase
        self.platforms = []  # final_plat.csv
        self.objects = []    # final_obj.csv  
        self.collectibles = []  # final_peg.csv
        self.decorations = []  # final_deco.csv
        self.tiles = []  # Matriz de tiles com colisão
        
        # Carregar o mapa
        self.load_level()
        self.build_collision_map()
    
    def load_level(self):
        """Carrega o mapa dos arquivos CSV"""
        print("Carregando mapa...")
        suffix = "02" if self.phase == 2 else ""
        def pick(*candidates):
            for name in candidates:
                if name and os.path.exists(name):
                    return name
            return candidates[0]

        plat = pick(
            f"final_plat{suffix and suffix or ''}.csv",
            f"final_plat_{suffix}.csv"
        ) if suffix else "final_plat.csv"

        obj = pick(
            f"final_obj{suffix and suffix or ''}.csv",
            f"final_obj_{suffix}.csv"
        ) if suffix else "final_obj.csv"

        # Alguns projetos nomeiam 'peg' como 'peco' por engano; considerar ambos
        peg = pick(
            f"final_peg{suffix and suffix or ''}.csv",
            f"final_peg_{suffix}.csv",
            f"final_peco{suffix and suffix or ''}.csv",
            f"final_peco_{suffix}.csv"
        ) if suffix else "final_peg.csv"

        deco = pick(
            f"final_deco{suffix and suffix or ''}.csv",
            f"final_deco_{suffix}.csv"
        ) if suffix else "final_deco.csv"
        # Carregar cada CSV
        self.load_csv(plat, self.platforms, "plataformas")
        self.load_csv(obj, self.objects, "objetos")
        self.load_csv(peg, self.collectibles, "itens")
        self.load_csv(deco, self.decorations, "decorações")
        
        print(f"Mapa carregado: {len(self.platforms)}x{len(self.platforms[0]) if self.platforms else 0}")
    
    def build_collision_map(self):
        """Constrói o mapa de colisão dinamicamente"""
        print("Construindo mapa de colisão...")
        
        # Inicializar matriz de tiles
        self.tiles = []
        for y in range(ROWS):
            tile_row = []
            for x in range(COLS):
                # Determinar qual tile_id usar (prioridade: plataformas > objetos > itens > decoração)
                tile_id = -1
                
                # 1. Verificar plataformas (prioridade máxima)
                if y < len(self.platforms) and x < len(self.platforms[y]):
                    if self.platforms[y][x] != -1:
                        tile_id = self.platforms[y][x]
                
                # 2. Verificar objetos
                if tile_id == -1 and y < len(self.objects) and x < len(self.objects[y]):
                    if self.objects[y][x] != -1:
                        tile_id = self.objects[y][x]
                
                # 3. Verificar itens coletáveis
                if tile_id == -1 and y < len(self.collectibles) and x < len(self.collectibles[y]):
                    if self.collectibles[y][x] != -1:
                        tile_id = self.collectibles[y][x]
                
                # 4. Verificar decorações
                if tile_id == -1 and y < len(self.decorations) and x < len(self.decorations[y]):
                    if self.decorations[y][x] != -1:
                        tile_id = self.decorations[y][x]
                
                # Criar tile com colisão (com informação da camada)
                # A camada determina o comportamento (ex.: DANGER só em 'object')
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
        """Carrega um arquivo CSV e converte para lista de tiles"""
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    # Converter cada linha para lista de inteiros
                    tile_row = [int(tile) for tile in row]
                    target_list.append(tile_row)
            print(f"✓ {layer_name}: {filename} carregado com {len(target_list)} linhas")
        except FileNotFoundError:
            print(f"✗ Erro: Arquivo {filename} não encontrado!")
        except Exception as e:
            print(f"✗ Erro ao carregar {filename}: {e}")
    
    def draw(self, screen):
        """Desenha o mapa na tela"""
        # Desenhar na ordem correta (plataformas por baixo, decoração por cima)
        
        # 1. Plataformas (fundo)
        self.draw_layer(screen, self.platforms, "platform")
        
        # 2. Objetos
        self.draw_layer(screen, self.objects, "object")
        
        # 3. Itens coletáveis
        self.draw_layer(screen, self.collectibles, "collectible")
        
        # 4. Decorações (por cima)
        self.draw_layer(screen, self.decorations, "decoration")
    
    def draw_layer(self, screen, layer_data, layer_type):
        """Desenha uma camada específica do mapa"""
        for y, row in enumerate(layer_data):
            for x, tile_id in enumerate(row):
                if tile_id != -1:  # Se não for vazio
                    # Calcular posição na tela (18x18 pixels)
                    screen_x = x * TILE_SIZE
                    screen_y = y * TILE_SIZE
                    
                    # Gerar nome do arquivo de imagem (4 dígitos)
                    image_name = f"tile_{tile_id:04d}"
                    
                    # Desenhar o tile
                    try:
                        screen.blit(image_name, (screen_x, screen_y))
                    except:
                        # Se a imagem não existir, desenhar um quadrado colorido
                        color = self.get_tile_color(tile_id, layer_type)
                        screen.draw.filled_rect(
                            (screen_x, screen_y, TILE_SIZE, TILE_SIZE), 
                            color
                        )
    
    def get_tile_color(self, tile_id, layer_type):
        """Retorna uma cor para o tile baseada no tipo e ID"""
        if layer_type == "platform":
            return (139, 69, 19)  # Marrom para plataformas
        elif layer_type == "object":
            return (128, 128, 128)  # Cinza para objetos
        elif layer_type == "collectible":
            return (255, 215, 0)  # Dourado para itens
        elif layer_type == "decoration":
            return (34, 139, 34)  # Verde para decorações
        return (255, 255, 255)  # Branco padrão
    
    def get_tile_at(self, x, y):
        """Retorna o tile na posição (x, y)"""
        if 0 <= y < ROWS and 0 <= x < COLS:
            return self.tiles[y][x]
        return None
    
    def check_collision(self, player_rect):
        """Verifica colisões do player com tiles"""
        collisions = {
            'solid': False,
            'platform': False,
            'danger': False,
            'collectible': []
        }
        
        # Verificar tiles ao redor do player (otimização)
        start_x = max(0, int(player_rect[0] // TILE_SIZE) - 1)
        end_x = min(COLS, int((player_rect[0] + player_rect[2]) // TILE_SIZE) + 2)
        start_y = max(0, int(player_rect[1] // TILE_SIZE) - 1)
        end_y = min(ROWS, int((player_rect[1] + player_rect[3]) // TILE_SIZE) + 2)
        
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = self.get_tile_at(x, y)
                if tile and tile.tile_id != -1:
                    cx, cy, cw, ch = tile.get_collision_rect()
                    # Ignorar tiles sem área de colisão (decoração/vazio)
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
        """Verifica se dois retângulos colidem"""
        return (rect1[0] < rect2[0] + rect2[2] and
                rect1[0] + rect1[2] > rect2[0] and
                rect1[1] < rect2[1] + rect2[3] and
                rect1[1] + rect1[3] > rect2[1])

    def get_tiles_overlapping(self, rect, include_types=None):
        """Retorna lista de tiles cujo retângulo de colisão intersecta 'rect'.
        include_types: conjunto opcional de tipos (e.g., {"SOLID", "PLATFORM"}).
        Decorações e vazios são automaticamente ignorados.
        """
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
                # ignorar decoração e vazio
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