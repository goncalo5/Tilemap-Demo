#!/usr/bin/env python
import pygame as pg
from settings import *


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


class Map(object):
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE


class Camera(object):
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        x = max(-(self.width - WIDTH), x)  # right
        y = min(0, y)  # top
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y,  self.width, self.height)

    def apply(self, entity=None, rect=None):
        # need to use move, because we don't want to change the images
        # just the images in the camera, and the move returns a new rect
        # so in that case we don't change the image location,
        # we create a new location with the returned rect
        if rect:
            return rect.move(self.camera.topleft)
        return entity.rect.move(self.camera.topleft)
