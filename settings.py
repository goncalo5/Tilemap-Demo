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
CYAN = (0, 255, 255)

# game options/settings
TITLE = 'Tilemap Demo'
WIDTH = 1280
HEIGHT = 1028
FPS = 80
FONT_NAME = 'arial'
HIGHSCORE_FILE = 'highscore.txt'
SPRITESHEET_DIR = []
SPRITESHEET_FILE = ''

# Maps:
MAP = 'map2.txt'
MAPS_DIR = ['img', 'maps']
MAPS = ['tile1.tmx']

# Background:
BG_COLOR = BROWN
CLOUD_DIR = []

# Fonts:
FONT_DIR = ['img']
FONT_TITLE = 'ZOMBIE.TTF'
FONT_HUD = 'Impacted2.0.ttf'

# Tiles:
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGTH = HEIGHT / TILESIZE

# Player:
PLAYER_DIR = ['img', 'topdown-shooter', 'PNG', 'Man Blue']
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_LAYER = 2
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_HEALTH = 100
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)
PLAYER_INIT_WEAPON = 'pistol'

# Weapons:
BULLET_DIR = ['img', 'topdown-shooter', 'PNG', 'Tiles']
BULLET_IMG = 'tile_187.png'
WEAPON_LAYER = 2
WEAPONS = {}
WEAPONS['pistol'] = {
    'bullet_speed': 500,
    'bullet_lifetime': 1000,
    'rate': 250,
    'kickback': 100,
    'spread': 5,
    'damage': 10,
    'bullet_size': 'lg',
    'bullet_count': 1,
    'bullet_hit_rect': pg.Rect(0, 0, 10, 10)
}
WEAPONS['shotgun'] = {
    'bullet_speed': 400,
    'bullet_lifetime': 500,
    'rate': 900,
    'kickback': 200,
    'spread': 20,
    'damage': 5,
    'bullet_size': 'sm',
    'bullet_count': 12,
    'bullet_hit_rect': pg.Rect(0, 0, 5, 5)
}

# Effects:
MUZZLE_FLASHES_DIR = ['img', 'smokeParticleAssets', 'PNG', 'White puff']
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png',
                  'whitePuff17.png', 'whitePuff18.png']
FLASH_DURATION = 40
MUZZLE_FLASHES_LAYER = 4
DAMAGE_ALPHA = [i for i in range(0, 255, 25)]

# Mob:
MOB_DIR = ['img', 'topdown-shooter', 'PNG', 'Zombie 1']
MOB_IMG = 'zoimbie1_hold.png'
MOB_LAYER = 2
MOB_MIN_SPEED = 50
MOB_MAX_SPEED = 200
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 400

# Wall:
WALL_LAYER = 3
WALL_DIR = ['img', 'topdown-shooter', 'PNG', 'Tiles']
WALL_IMG = 'tile_42.png'
WALL_SIZE = (TILESIZE, TILESIZE)

# Items:
ITEM_IMAGES = {
    'health': 'health_pack.png',
    'shotgun': 'obj_shotgun.png'
}
ITEM_LAYER = 1
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.4

# Mobs:
MOB_FREQ = 5000
MOB_LAYER = 2
SPLAT_DIR = ['img']
SPLAT_IMAGE = 'splat green.png'

# Sounds:
SOUND_VOLUME = 0.1
MUSIC_DIR = ['Sounds', 'music']
SOUND_DIR = ['Sounds', 'snd']
BG_MUSIC = 'espionage.ogg'
SOUND_PAIN_DIR = SOUND_DIR + ['pain']
PLAYER_HIT_SOUNDS = ['8.wav', '9.wav', '10.wav', '11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
# WEAPON_SOUNDS_GUN = ['sfx_weapon_singleshot2.wav']
WEAPON_SOUNDS = {
    'pistol': ['pistol.wav'],
    'shotgun': ['shotgun.wav']
}

EFFECTS_SOUND = {
    'level_start': 'level_start.wav',
    'health_up': 'health_pack.wav',
    'gun_pickup': 'gun_pickup.wav'
}
