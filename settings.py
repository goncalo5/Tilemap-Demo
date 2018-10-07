#!/usr/bin/env python
import pygame as pg
vec = pg.math.Vector2

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
BROWN = (106, 55, 5)

# game options/settings
TITLE = 'Tilemap Demo'
WIDTH = 768  # 1024
HEIGHT = 640  # 768
FPS = 80
FONT_NAME = 'arial'
HIGHSCORE_FILE = 'highscore.txt'
SPRITESHEET_DIR = []
SPRITESHEET_FILE = ''
MAP = 'map2.txt'

# Background:
BG_COLOR = BROWN
CLOUD_DIR = []

# Tiles:
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGTH = HEIGHT / TILESIZE

# Player:
PLAYER_LAYER = 2
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_DIR = ['img', 'topdown-shooter', 'PNG', 'Man Blue']
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)
# Gun:
BULLET_DIR = ['img', 'topdown-shooter', 'PNG', 'Tiles']
BULLET_IMG = 'tile_187.png'
BULLET_LAYER = 1
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150
KICKBACK = 200
GUN_SPREAD = 5


# Mob:
MOB_DIR = ['img', 'topdown-shooter', 'PNG', 'Zombie 1']
MOB_IMG = 'zoimbie1_hold.png'
MOB_LAYER = 2
MOB_ACC = 150
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)

# Wall:
WALL_LAYER = 3
WALL_DIR = ['img', 'topdown-shooter', 'PNG', 'Tiles']
WALL_IMG = 'tile_42.png'
WALL_SIZE = (TILESIZE, TILESIZE)

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
