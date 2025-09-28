from configGlobal import *

class Tile:
    def __init__(self, tile_id, x, y, layer):
        self.tile_id = tile_id
        self.layer = layer
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.tile_type = self.get_tile_type(tile_id)
        
    def get_tile_type(self, tile_id):
        for tile_type, ids in TILE_COLLISION_TYPES.items():
            if tile_id in ids:
                if tile_id == 68:
                    print(f"Tile {tile_id} classificado como {tile_type}")
                return tile_type
        return "EMPTY"
    
    def is_solid(self):
        return self.tile_type in ["SOLID", "PLATFORM"]
    
    def is_dangerous(self):
        return self.tile_type == "DANGER" and self.layer == "object"
    
    def is_collectible(self):
        return self.tile_type == "COLLECTIBLE"
    
    def is_platform(self):
        return self.tile_type == "PLATFORM"
    
    def get_rect(self):
        return (self.x, self.y, self.width, self.height)
    
    def get_collision_rect(self):
        import configGlobal
        
        padding = 2
        if self.tile_type == "PLATFORM":
            return (self.x + padding, self.y, self.width - 2 * padding, 3)
        if self.tile_type == "SOLID":
            return (self.x + padding, self.y + padding, self.width - 2 * padding, self.height - 2 * padding)
        if self.tile_type == "DANGER":
            if configGlobal.DEV_MODE:
                return (self.x + padding, self.y + padding, self.width - 2 * padding, self.height - 2 * padding)
            inset = 2
            return (self.x + inset, self.y + inset, self.width - 2 * inset, self.height - 2 * inset)
        if self.tile_type == "COLLECTIBLE":
            inset = 2
            return (self.x + inset, self.y + inset, self.width - 2 * inset, self.height - 2 * inset)
        return (self.x, self.y, 0, 0)