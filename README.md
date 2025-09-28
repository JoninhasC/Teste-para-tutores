# 🎮 Platformer Game - PgZero

Um jogo de plataforma 2D desenvolvido em Python usando PgZero, com animações completas, múltiplos inimigos, sistema de áudio e duas fases progressivas.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PgZero](https://img.shields.io/badge/PgZero-1.2%2B-green)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Como Jogar](#-como-jogar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Sistema de Classes](#-sistema-de-classes)
- [Assets](#-assets)
- [Desenvolvimento](#-desenvolvimento)

## 🎯 Sobre o Projeto

Este é um jogo de plataforma clássico onde o jogador controla um personagem azul através de dois níveis desafiadores, coletando itens, evitando inimigos perigosos e navegando por plataformas. O projeto foi desenvolvido seguindo as melhores práticas de programação Python e design de jogos.

### ✨ Destaques Técnicos

- **Arquitetura Modular**: Código organizado em classes especializadas
- **Sistema de Colisão Avançado**: AABB otimizado com hitboxes customizadas
- **Animação Completa**: Sprites animados para todos os personagens
- **IA de Inimigos**: Três tipos diferentes de comportamento
- **Sistema de Áudio**: Playlist automática + efeitos sonoros

## 🚀 Funcionalidades

### 🎮 Gameplay
- ✅ **Duas fases progressivas** com layouts únicos
- ✅ **Sistema de vidas** (5 vidas por partida)
- ✅ **Múltiplos tipos de tiles** (sólidos, plataformas, perigos, coletáveis)
- ✅ **Sistema de checkpoint** com respawn automático
- ✅ **Coleta de itens** para progressão

### 👹 Inimigos
- ✅ **3 tipos de inimigos** com IA diferenciada:
  - **Tipo A**: Patrulha terrestre normal
  - **Tipo B**: Patrulha terrestre rápida
  - **Tipo P**: Movimento aéreo senoidal

### 🎵 Sistema de Áudio
- ✅ **17 músicas de fundo** em playlist automática
- ✅ **Efeitos sonoros** contextuais
- ✅ **Controle de áudio** (ligar/desligar)

### 🎭 Animações
- ✅ **Player animado**: Idle, caminhada, pulo (direita/esquerda)
- ✅ **Inimigos animados**: 3 frames por inimigo (direita/esquerda)
- ✅ **Animação temporal** fluida

### 🛠️ Recursos Especiais
- ✅ **Modo Desenvolvedor** (imortalidade - tecla Q)
- ✅ **Menu interativo** com botões clicáveis
- ✅ **Sistema de estados** (Menu, Jogo, Vitória, Game Over)

## 📋 Requisitos

### Software Necessário
- **Python 3.8+**
- **PgZero 1.2+**

### Bibliotecas Utilizadas
```python
# Bibliotecas permitidas conforme especificação
import pgzrun      # Framework principal
import math        # Movimentos senoidais
import random      # Elementos aleatórios
```

## ⚡ Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/JoninhasC/Teste-para-tutores.git
cd Teste-para-tutores
```

### 2. Instale o PgZero
```bash
pip install pgzero
```

### 3. Execute o jogo
```bash
python main.py
```
ou
```bash
pgzrun main.py
```

## 🎯 Como Jogar

### 🕹️ Controles

| Tecla | Ação |
|-------|------|
| **A** / **←** | Mover para esquerda |
| **D** / **→** | Mover para direita |
| **W** / **↑** / **ESPAÇO** | Pular |
| **Q** | Modo desenvolvedor (imortal) |
| **Mouse** | Navegar menus |

### 🎮 Objetivo

1. **Navegue** pelas plataformas evitando inimigos
2. **Colete** o item especial (brilhante) em cada fase
3. **Complete** as duas fases para vencer
4. **Cuidado** com os tiles vermelhos - são perigosos!

### ❤️ Sistema de Vidas

- Você começa com **5 vidas**
- Perde 1 vida ao tocar em inimigos ou tiles perigosos
- Respawn automático na posição inicial da fase
- Game Over quando as vidas acabam

## 📁 Estrutura do Projeto

```
Teste-para-tutores/
├── main.py                 # Arquivo principal e loop do jogo
├── configGlobal.py         # Constantes e configurações
├── player.py               # Classe do jogador
├── enemy.py                # Classe dos inimigos
├── level.py                # Sistema de fases e colisão
├── tile.py                 # Sistema de tiles individual
├── controls.py             # Sistema de entrada
├── README.md               # Este arquivo
├── images/                 # Assets visuais
│   ├── characters/         # Sprites dos personagens
│   │   ├── azul01.png     # Player - frame 1
│   │   ├── azul01r.PNG    # Player - frame 1 (direita)
│   │   ├── azul02.png     # Player - frame 2
│   │   ├── azul02r.PNG    # Player - frame 2 (direita)
│   │   ├── a01.png        # Inimigo A - frame 1
│   │   ├── a01r.PNG       # Inimigo A - frame 1 (direita)
│   │   └── ...            # Demais sprites
│   └── tile_XXXX.png      # Tiles do mapa (180 tiles)
├── sounds/                 # Efeitos sonoros
│   └── click_003.ogg      # Som de clique/ação
├── music/                  # Música de fundo
│   ├── jingles_nes00.ogg  # Track 1
│   ├── jingles_nes01.ogg  # Track 2
│   └── ...                # 17 tracks total
└── *.csv                  # Arquivos de mapa das fases
```

## 🏗️ Sistema de Classes

### 🎭 **Player** (`player.py`)
- **Física**: Gravidade, pulo, movimento horizontal
- **Colisão**: Sistema dual-axis com rollback
- **Animação**: 6 sprites (idle, walk, jump × direita/esquerda)
- **Estados**: Vida, posição, velocidade

### 👹 **Enemy** (`enemy.py`)
- **IA Diversificada**: 3 padrões de movimento
- **Animação**: 3 frames por tipo × 2 direções
- **Colisão**: Detecção com jogador e cenário
- **Comportamentos**:
  - Patrulha terrestre com detecção de bordas
  - Movimento aéreo senoidal

### 🗺️ **Level** (`level.py`)
- **Carregamento**: 4 camadas CSV (plataformas, objetos, coletáveis, decoração)
- **Colisão**: Sistema de tiles otimizado
- **Renderização**: Multi-layer com fallback colorido

### 🧱 **Tile** (`tile.py`)
- **Tipos**: SOLID, PLATFORM, DANGER, COLLECTIBLE, DECORATION
- **Hitboxes**: Customizadas por tipo de tile
- **Sistema**: Classificação automática por ID

## 🎨 Assets

### 🖼️ Visuais
- **180 tiles** de ambiente (tile_0000.png - tile_0179.png)
- **Sprites animados** para todos os personagens
- **Paleta consistente** pixel art 18x18

### 🎵 Áudio
- **17 músicas** de fundo (jingles_nes)
- **Efeitos sonoros** para ações
- **Formato OGG** para compatibilidade

### 🗺️ Mapas
- **2 fases** progressivas
- **4 camadas** por fase (CSV):
  - Plataformas sólidas
  - Objetos interativos  
  - Itens coletáveis
  - Decoração ambiente

## 🔧 Desenvolvimento

### 🏛️ Arquitetura

O projeto segue o padrão **Component-Entity-System** adaptado:

```python
# Fluxo principal
main.py → pgzrun.go()
    ├── draw() → Renderização por estado
    ├── update(dt) → Lógica do jogo
    └── on_mouse_down() → Entrada do usuário

# Sistemas especializados
Player → Física + Animação + Colisão
Enemy → IA + Movimento + Detecção
Level → Mapa + Tiles + Colisão
```

### ⚙️ Configuração

Todas as constantes ficam em `configGlobal.py`:
```python
# Física
GRAVITY = 1
JUMP_STRENGTH = -15
PLAYER_SPEED = 3

# Tela
TILE_SIZE = 18
WIDTH = 540  # 30 tiles
HEIGHT = 360 # 20 tiles
```

### 🐛 Debug

Modo desenvolvedor ativado com **Q**:
- Player imortal
- Debug visual
- Logs detalhados

## 📜 Licença

Este projeto foi desenvolvido para fins educacionais. Assets da Kenney (CC0).

---