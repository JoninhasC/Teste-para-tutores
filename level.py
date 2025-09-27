# level.py - Sistema de geração de níveis CORRIGIDO

from configGlobal import *
import csv

class Level:
    def __init__(self):
        """Inicializa o sistema de níveis"""
        self.platforms = []  # final_plat.csv
        self.objects = []    # final_obj.csv  
        self.collectibles = []  # final_peg.csv
        self.decorations = []  # final_deco.csv
        
        # Carregar o mapa
        self.load_level()
    
    def load_level(self):
        """Carrega o mapa dos arquivos CSV"""
        print("Carregando mapa...")
        
        # Carregar cada CSV
        self.load_csv("final_plat.csv", self.platforms, "plataformas")
        self.load_csv("final_obj.csv", self.objects, "objetos")
        self.load_csv("final_peg.csv", self.collectibles, "itens")
        self.load_csv("final_deco.csv", self.decorations, "decorações")
        
        print(f"Mapa carregado: {len(self.platforms)}x{len(self.platforms[0]) if self.platforms else 0}")
    
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