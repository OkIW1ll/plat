# game settings
TITLE = "Sky Jump"
WIDTH = 500
HEIGHT = 620
FPS = 60
FONT_NAME = 'press start p2'
HS_FILE = "highscore.txt"
SPRITESHEET = "p1_spritesheet.png"
SS2 = "tiles_spritesheet.png"
SS3 = "enemies_spritesheet.png"
SS4 = "items_spritesheet.png"
SS5 = "invince_spritesheet.png"

# player settings
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.5
PLAYER_JUMP = 18

# platform settings
PLATFORM_LIST = [(5, HEIGHT - 40),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4),
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100)]

BOOST_POWER = 60
POW_SPAWN_PCT = 8
MOB_FREQ = 5000
PLAYER_LAYER = 3
PLAT_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE
