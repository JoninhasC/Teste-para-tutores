# =============================================================================
# CONFIGURAÇÕES BÁSICAS DO JOGO - PLATFORMER
# =============================================================================

# Configurações do sistema de tiles (grade do jogo)
TILE_SIZE = 32          # Tamanho de cada quadrado/tile em pixels (reduzido para tela menor)
ROWS = 15               # Número de linhas de tiles na tela
COLS = 25               # Número de colunas de tiles na tela

# Dimensões da janela do jogo
WIDTH = COLS * TILE_SIZE    # Largura total: 25 tiles × 32px = 800px
HEIGHT = ROWS * TILE_SIZE   # Altura total: 15 tiles × 32px = 480px
TITLE = "PLATAFORM GAME"    # Título da janela

# =============================================================================
# CONFIGURAÇÕES DE FÍSICA DO JOGO
# =============================================================================

# Força da gravidade (puxa o personagem para baixo)
GRAVITY = 1.5

# Velocidades iniciais do personagem
Y_VELOCITY = 0          # Velocidade vertical (para cima/baixo)
X_VELOCITY = 0          # Velocidade horizontal (esquerda/direita)

# Configurações de movimento
JUMP_FORCE = -20        # Força do pulo (negativo = para cima)
X_ACCELERATION = 10     # Aceleração horizontal do personagem

# =============================================================================
# CONFIGURAÇÕES DE ANIMAÇÃO DOS SPRITES
# =============================================================================

# Velocidade das animações do herói
HERO_IDLE_SPEED = 0.1   # Velocidade da animação quando parado
HERO_WALK_SPEED = 0.1   # Velocidade da animação quando andando

# =============================================================================
# POSIÇÕES INICIAIS
# =============================================================================

# Posição inicial do herói no jogo (x, y)
# x = 1 tile da esquerda, y = meio da tela verticalmente
HERO_START_POS = TILE_SIZE, HEIGHT/2



