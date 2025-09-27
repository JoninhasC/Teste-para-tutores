# =============================================================================
# CONFIGURAÇÕES DA TELA E VISUAL
# =============================================================================

# TILE_SIZE: Tamanho de cada quadradinho (tile) do jogo em pixels
TILE_SIZE = 24

# ROWS e COLS: Quantas linhas e colunas de tiles cabem na tela
# 20 linhas x 30 colunas = grade de 20x30 tiles
ROWS = 20
COLS = 30

# WIDTH e HEIGHT: Tamanho total da janela do jogo
WIDTH = COLS * TILE_SIZE    # 720px - largura da janela
HEIGHT = ROWS * TILE_SIZE   # 480px - altura da janela
TITLE = "PLATAFORM GAME"    # Título que aparece na barra da janela

# =============================================================================
# CONFIGURAÇÕES DE FÍSICA DO JOGO
# =============================================================================

# GRAVITY: Força que puxa o personagem para baixo
# Quanto maior, mais rápido o personagem cai
# 1 é um valor suave para um jogo de plataforma
GRAVITY = 1

# JUMP_FORCE: Força do pulo do personagem
# Número negativo porque "para cima" é direção negativa no sistema de coordenadas
# -50 significa que o personagem vai subir 50 pixels por frame quando pular
JUMP_FORCE = -50

# X_ACCELERATION: Velocidade de movimento horizontal
# Quanto maior, mais rápido o personagem anda para os lados
# 50 é um valor alto para movimento responsivo
X_ACCELERATION = 50

# =============================================================================
# CONFIGURAÇÕES DE ANIMAÇÃO (FUTURAMENTE)
# =============================================================================

# Velocidades das animações dos sprites
# 0.1 significa que a animação muda de frame a cada 0.1 segundos
HERO_IDLE_SPEED = 0.1   # Velocidade da animação quando parado
HERO_WALK_SPEED = 0.1   # Velocidade da animação quando andando

# =============================================================================
# POSIÇÕES INICIAIS
# =============================================================================

# HERO_START_POS: Onde o personagem aparece quando o jogo começa
# (TILE_SIZE, HEIGHT // 2) = 1 tile da esquerda, meio da tela verticalmente
HERO_START_POS = (TILE_SIZE, HEIGHT // 2)

# =============================================================================
# PALETA DE CORES DO JOGO
# =============================================================================
# Todas as cores usadas no jogo, organizadas em um dicionário
# Formato: (R, G, B) onde cada valor vai de 0 a 255

COLORS = {
    'background': (30, 30, 30),        # Cinza escuro para o fundo
    'solid_tile': (100, 50, 0),        # Marrom para tiles sólidos (chão/parede)
    'solid_tile_border': (150, 100, 0), # Marrom claro para borda dos tiles
    'character': (0, 100, 200),        # Azul para o personagem
    'character_border': (255, 255, 255), # Branco para borda do personagem
    'text': (255, 255, 255),           # Branco para texto principal
    'text_secondary': (200, 200, 200)  # Cinza claro para texto secundário
}

# =============================================================================
# TIPOS DE TILES (QUADRADINHOS) DO MAPA
# =============================================================================
# Cada número representa um tipo diferente de tile no mapa

TILE_TYPES = {
    'EMPTY': 0,      # Tile vazio (transparente, personagem pode passar)
    'SOLID': 1,      # Tile sólido (chão/parede, personagem não pode passar)
    'PLATFORM': 2,   # Plataforma (personagem pode pular em cima)
    'SPIKE': 3       # Espinho (machuca o personagem)
}
