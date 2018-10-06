#!/usr/bin/env python
from os import path
import random
import pygame as pg
from settings import *
from sprites import Player, Wall
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

    def load_data(self):
        self.dir = path.dirname(__file__)
        self.img_dir = self.dir
        for dir in PLAYER_DIR:
            self.img_dir = path.join(self.img_dir, dir)
        self.map = Map(path.join(self.dir, 'map2.txt'))
        # load imgs:
        self.player_img = path.join(self.img_dir, PLAYER_IMG)
        self.player_img = pg.image.load(self.player_img).convert_alpha()
        # load sound
        pg.mixer.init()

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        # create walls:
        self.walls = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    # create player:
                    self.player = Player(self, col, row)
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

    def draw_grid(self):
        # vertically:
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        # horizontally:
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.draw_grid()
        # self.all_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def quit(self):
        self.running = False


Game()
