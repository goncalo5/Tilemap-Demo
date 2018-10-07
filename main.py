#!/usr/bin/env python
from os import path
import random
import pygame as pg
from settings import *
from sprites import Player, Mob, Wall
from tilemap import Map, Camera


class Game(object):
    def __init__(self):

        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(300, 100)

        # variables
        self.cmd_key_down = False

        self.load_data()
        self.new()
        self.run()

        pg.quit()

    def load_a_thing(self, thing_file, thing_dir_list=['img'], thing_size=None):
        thing_dir = self.dir
        for dir in thing_dir_list:
            thing_dir = path.join(thing_dir, dir)
        thing_img = path.join(thing_dir, thing_file)
        thing_img = pg.image.load(thing_img).convert_alpha()
        if thing_size:
            thing_img = pg.transform.scale(thing_img, thing_size)
        return thing_img

    def load_data(self):
        self.dir = path.dirname(__file__)
        # Maps:
        self.map = Map(path.join(self.dir, MAP))
        # Walls:
        self.wall_img = self.load_a_thing(WALL_IMG, WALL_DIR, WALL_SIZE)
        # Player:
        self.player_img = self.load_a_thing(PLAYER_IMG, PLAYER_DIR)
        self.bullet_img = self.load_a_thing(BULLET_IMG, BULLET_DIR)
        # Mobs:
        self.mob_img = self.load_a_thing(MOB_IMG, MOB_DIR)

        # load sound
        pg.mixer.init()

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    # create player:
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set  self.playing = False to end the game
        self.running = True
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            self.handle_common_events(event)
            self.player.events(event)

    def handle_common_events(self, event):
        # check for closing window
        if event.type == pg.QUIT:
            # force quit
            quit()

        if event.type == pg.KEYDOWN:
            if event.key == 310:
                self.cmd_key_down = True
            if self.cmd_key_down and event.key == pg.K_q:
                # force quit
                quit()

        if event.type == pg.KEYUP:
            if event.key == 310:
                self.cmd_key_down = False

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # bullets hit mobs:
        hits = pg.sprite.groupcollide(self.bullets, self.mobs, True, True)
        print hits
        for hit in hits:
            print hit
            hit.kill()

    def draw_grid(self):
        # vertically:
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        # horizontally:
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption('fps: %.5s' % self.clock.get_fps())
        self.screen.fill(BG_COLOR)
        # self.draw_grid()
        # self.all_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # pg.draw.rect(self.screen, WHITE, self.camera.apply(self.player), 2)
        # pg.draw.rect(self.screen, WHITE, self.camera.apply(rect=self.player.hit_rect), 2)
        pg.display.flip()

    def quit(self):
        self.running = False


Game()
