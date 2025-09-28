# tile.py - Sistema de tiles com colisão dinâmica

from configGlobal import *

class Tile:
    def __init__(self, tile_id, x, y, layer):
        self.tile_id = tile_id
        self.layer = layer  # "platform", "object", "collectible", "decoration"
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.tile_type = self.get_tile_type(tile_id)
        
    def get_tile_type(self, tile_id):
        """Determina o tipo de colisão do tile dinamicamente"""
        for tile_type, ids in TILE_COLLISION_TYPES.items():
            if tile_id in ids:
                return tile_type
        return "EMPTY"
    
    def is_solid(self):
        """Verifica se o tile é sólido"""
        return self.tile_type in ["SOLID", "PLATFORM"]
    
    def is_dangerous(self):
        """Verifica se o tile é perigoso (somente camada de objetos)"""
        return self.tile_type == "DANGER" and self.layer == "object"
    
    def is_collectible(self):
        """Verifica se o tile é coletável"""
        return self.tile_type == "COLLECTIBLE"
    
    def is_platform(self):
        """Verifica se é uma plataforma (só colisão por cima)"""
        return self.tile_type == "PLATFORM"
    
    def get_rect(self):
        """Retorna o retângulo de colisão"""
        return (self.x, self.y, self.width, self.height)
    
    def get_collision_rect(self):
        """Retorna retângulo de colisão específico para o tipo, com padding para evitar colisão maior que o visual"""
        padding = 2  # reduz hitbox para dentro do tile
        if self.tile_type == "PLATFORM":
            # Plataforma: só colisão na parte superior, com leve recuo lateral
            return (self.x + padding, self.y, self.width - 2 * padding, 3)
        if self.tile_type == "SOLID":
            # Sólido: colisão completa porém levemente menor que o tile para não "agarrar" nas bordas
            return (self.x + padding, self.y + padding, self.width - 2 * padding, self.height - 2 * padding)
        if self.tile_type == "DANGER":
            # Hitbox menor para reduzir falsos acertos
            inset = 4
            return (self.x + inset, self.y + inset, self.width - 2 * inset, self.height - 2 * inset)
        if self.tile_type == "COLLECTIBLE":
            # Pegada um pouco menor que o tile
            inset = 2
            return (self.x + inset, self.y + inset, self.width - 2 * inset, self.height - 2 * inset)
        # Decoração e vazio: sem colisão
        return (self.x, self.y, 0, 0)