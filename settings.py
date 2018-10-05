#!/usr/bin/env python
# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 200)

# game options/settings
TITLE = 'Tilemap Demo'
WIDTH = 1024
HEIGHT = 768
FPS = 60
FONT_NAME = 'arial'
HIGHSCORE_FILE = 'highscore.txt'
SPRITESHEET_DIR = []
SPRITESHEET_FILE = ''

# Background:
BG_COLOR = DARKGREY
CLOUD_DIR = []

# Tiles:
TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGTH = HEIGHT / TILESIZE

# Player:
PLAYER_SIZE_RATE = 0.4
PLAYER_ACC = .5
PLAYER_FRICTION = -0.12
PLAYER_G = 0.8
PLAYER_JUMP = 25
PLAYER_LAYER = 2

# Wall:
WALL_LAYER = 2

# powerups:
BOOST_POWER = 60
POW_SPAWN_PCT = 10
POW_LAYER = 1

# Mobs:
MOB_FREQ = 5000
MOB_LAYER = 2

# Sounds:
SOUND_DIR = 'snd'
MUSIC_GAME = 'happytune.ogg'
MUSIC_MENU = 'Yippee.ogg'
SOUND_JUMP = 'Jump.wav'
SOUND_BOOST = 'boost.wav'
