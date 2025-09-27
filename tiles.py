# tiles.py - Sistema global de tiles

from configGlobal import *
from pgzero.actor import Actor

def build(filename, tile_size):
    """Constrói elementos do mapa a partir de um arquivo CSV"""
    # Abrindo o arquivo como leitura
    with open(filename, "r") as f:
        # Extraindo o conteúdo e quebrando linhas
        contents = f.read().splitlines()
    
    # Quebrando as linhas
    contents = [c.split(",") for c in contents]
    
    # Percorrendo cada uma das linhas entre as disponíveis
    for row in range(len(contents)):
        # Percorrendo cada coluna dessa linha
        for col in range(len(contents[0])):
            # Extrair o elemento de cada linha e coluna
            val = contents[row][col]
            # Testar se o valor na posição é valido
            if val.isdigit() or (val[0] == "-" and val[1:].isdigit()):
                contents[row][col] = int(val)
    
    # Criação dos itens que serão construidos
    items = []

    # Caminhando pelas linhas
    for row in range(len(contents)):
        # Caminhando pelas colunas
        for col in range(len(contents[0])):
            # Extraindo o elemento da posição
            tile_num = contents[row][col]
            # Verificar se o espaço não é vazio
            if tile_num != -1:
                # Criação dos Actors
                item = Actor(f"tile_{tile_num:04d}")
                # Posicionar os Actors
                item.topleft = (tile_size * col, tile_size * row)
                # Reunindo todos os itens
                items.append(item)
    return items

# ===== VARIÁVEIS GLOBAIS =====
# Carregar todos os tiles do jogo
platforms = build("final_plat.csv", TILE_SIZE)
decorations = build("final_deco.csv", TILE_SIZE)
objects = build("final_obj.csv", TILE_SIZE)

print(f"Plataformas carregadas: {len(platforms)}")
print(f"Decorações carregadas: {len(decorations)}")
print(f"Objetos carregados: {len(objects)}")

def draw_level():
    """Desenha todo o nível"""
    # Desenhar plataformas
    for platform in platforms:
        platform.draw()
    
    # Desenhar decorações
    for decoration in decorations:
        decoration.draw()
    
    # Desenhar objetos
    for obj in objects:
        obj.draw()

def check_collision(player):
    """Verifica colisão entre player e plataformas"""
    # Criar retângulo do player
    player_rect = {
        'x': player.x - player.width//2,
        'y': player.y - player.height//2,
        'width': player.width,
        'height': player.height
    }
    
    for platform in platforms:
        # Verificar colisão manual
        if (player_rect['x'] < platform.x + platform.width and
            player_rect['x'] + player_rect['width'] > platform.x and
            player_rect['y'] < platform.y + platform.height and
            player_rect['y'] + player_rect['height'] > platform.y):
            return True
    return False