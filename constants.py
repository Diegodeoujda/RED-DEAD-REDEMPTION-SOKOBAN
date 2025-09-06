import random
MAPWIDTH    = 25
MAPHEIGHT   = 15
SPRITESIZE  = 32

WINDOW_WIDTH  = 1024
WINDOW_HEIGHT = 768

# Blocks
WALL            = 1
BOX             = 2
TARGET          = 3
TARGET_FILLED   = 4
PLAYER          = 5
AIR             = 6

UP      = 100
DOWN    = 101
LEFT    = 102
RIGHT   = 103

# Colors
WHITE           = (255, 255, 255)
BLACK           = (0,0,0)
BLUE            = (161, 173, 255)
GREY            = (200,200,200)
GREEN           = (238,130,238)

MUSIC = 'assets/sound/music.mp3'
ALL_BIOME = {1: 'desert', 2:'neige',3:'foret'}
BIOME = random.choice(list(ALL_BIOME.values()))


