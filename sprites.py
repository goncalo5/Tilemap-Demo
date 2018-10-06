#!/usr/bin/env python
import random
import pygame as pg
from settings import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        super(Player, self).__init__(self.groups)
        self.game = game
        self.image = game.player_img
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE

    def collide_with_walls(self, direction):
        if direction == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if direction == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                self.vel.y = 0
                self.rect.y = self.pos.y

    def events(self, event):
        # self.vx, self.vy = 0, 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN]:
            self.vel.y = PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def update(self):
        # self.x += self.vx * self.game.dt
        # self.y += self.vy * self.game.dt
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        super(Wall, self).__init__(self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
