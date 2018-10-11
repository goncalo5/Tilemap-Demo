#!/usr/bin/env python
from random import choice, uniform, randint, random
import pygame as pg
from settings import *
from tilemap import collide_hit_rect
import pytweening as tween
from itertools import chain
vec = pg.math.Vector2


def collide_with_walls(sprite, group, direction):
    if direction == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False,
                                       collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2.
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2.
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if direction == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False,
                                       collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2.
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2.
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        super(Player, self).__init__(self.groups)
        self.game = game
        self.image = game.player_img
        # self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.rot_speed = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.weapon = PLAYER_INIT_WEAPON
        self.damaged = False

    def events(self, event):
        # self.vx, self.vy = 0, 0
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            # self.vel.x = -PLAYER_SPEED
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT]:
            # self.vel.x = PLAYER_SPEED
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP]:
            # self.vel.y = -PLAYER_SPEED
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN]:
            # self.vel.y = PLAYER_SPEED
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
        # if self.vel.x != 0 and self.vel.y != 0:
        #     self.vel *= 0.7071
        if keys[pg.K_SPACE]:
            self.shoot()

    def shoot(self):
        now = pg.time.get_ticks()
        weapon = WEAPONS[self.weapon]
        if now - self.last_shot > weapon['rate']:
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            self.vel = vec(-weapon['kickback'], 0).\
                rotate(-self.rot)
            for i in range(weapon['bullet_count']):
                spread = uniform(-weapon['spread'],
                                 weapon['spread'])
                Bullet(self.game, pos, dir.rotate(spread),
                       WEAPONS[self.weapon]['damage'])
                snd = choice(self.game.weapon_sounds[self.weapon])
                if snd.get_num_channels() > 2:
                    snd.stop()
                snd.play()
            MuzzleFlash(self.game, pos)

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 2)

    def update(self):
        # self.x += self.vx * self.game.dt
        # self.y += self.vy * self.game.dt
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        if self.damaged:
            try:
                self.image.fill((255, 0, 0, next(self.damage_alpha)),
                                special_flags=pg.BLEND_RGBA_MULT)
            except StopIteration:
                self.damaged = False
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def add_health(self, amount):
        self.health += amount
        self.health = min(self.health, PLAYER_HEALTH)


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, direction, damage):
        self._layer = WEAPON_LAYER
        self.groups = game.all_sprites, game.bullets
        super(Bullet, self).__init__(self.groups)
        self.game = game
        self.weapon = WEAPONS[game.player.weapon]
        self.image =\
            game.bullet_images[self.weapon['bullet_size']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.weapon['bullet_hit_rect']
        self.hit_rect.center = self.rect.center
        self.pos = vec(pos)
        self.rect.center = self.pos
        # spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = direction * self.weapon['bullet_speed'] *\
            uniform(0.9, 1.1)
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > \
                self.weapon['bullet_lifetime']:
            self.kill()


class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = MUZZLE_FLASHES_LAYER
        self.groups = game.all_sprites
        super(MuzzleFlash, self).__init__(self.groups)
        self.game = game
        size = randint(20, 50)
        self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        super(Mob, self).__init__(self.groups)
        self.game = game
        self.image = game.mob_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy()  # copy because we have +1 mob
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)  # * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.acc_value = uniform(MOB_MIN_SPEED, MOB_MAX_SPEED)
        self.target = game.player

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < DETECT_RADIUS**2:
            if random() < 0.002:
                choice(self.game.zombie_moan_sounds).play()
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()

            self.acc.scale_to_length(self.acc_value)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += \
                self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.rect.center = self.pos
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        if self.health <= 0:
            choice(self.game.zombie_hit_sounds).play()
            self.kill()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))

    def draw_health(self):
        if self.health > MOB_HEALTH * 0.6:
            color = GREEN
        elif self.health > MOB_HEALTH * 0.3:
            color = YELLOW
        else:
            color = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, color, self.health_bar)


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        super(Wall, self).__init__(self.groups)
        self.game = game
        self.image = self.game.wall_img
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.walls
        super(Obstacle, self).__init__(self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y


class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = ITEM_LAYER
        self.groups = game.all_sprites, game.items
        super(Item, self).__init__(self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.pos = pos
        self.type = type
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.direction = 1

    def update(self):
        # bobbing motion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.direction
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.direction *= -1
