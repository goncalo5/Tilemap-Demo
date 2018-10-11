#!/usr/bin/env python
from os import path
import random
import pygame as pg
from settings import *
from sprites import Player, Mob, Wall, Obstacle, Item
from tilemap import Map, TiledMap, Camera, collide_hit_rect

# HUD functions


def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        color = GREEN
    elif pct > 0.3:
        color = YELLOW
    else:
        color = RED
    pg.draw.rect(surf, color, fill_rect)
    pg.draw.rect(surf, color, outline_rect, 2)


class Game(object):
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 1, 2048)
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

    def load_a_thing(self, thing_file, thing_dir_list):
        thing_dir = self.dir
        for dir in thing_dir_list:
            thing_dir = path.join(thing_dir, dir)
        thing_path = path.join(thing_dir, thing_file)
        return thing_path

    def load_a_image(self, thing_file, thing_dir_list=['img'], thing_size=None):
        thing_path = self.load_a_thing(thing_file, thing_dir_list)
        thing_img = pg.image.load(thing_path).convert_alpha()
        if thing_size:
            thing_img = pg.transform.scale(thing_img, thing_size)
        return thing_img

    def load_data(self):
        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, 'img')
        # Fonts:
        self.title_font = self.load_a_thing(FONT_TITLE, FONT_DIR)
        self.hud_font = self.load_a_thing(FONT_HUD, FONT_DIR)
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((100, 0, 0, 180))

        # Walls:
        self.wall_img = self.load_a_image(WALL_IMG, WALL_DIR, WALL_SIZE)
        # Player:
        self.player_img = self.load_a_image(PLAYER_IMG, PLAYER_DIR)
        self.bullet_images = {}
        self.bullet_images['lg'] = self.load_a_image(BULLET_IMG, BULLET_DIR)
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'],
                                                      [15, 15])

        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(self.load_a_image(img, MUZZLE_FLASHES_DIR))
        # Mobs:
        self.mob_img = self.load_a_image(MOB_IMG, MOB_DIR)

        self.item_images = {}
        for item in ITEM_IMAGES:
            item_path = path.join(self.img_dir, ITEM_IMAGES[item])
            self.item_images[item] = pg.image.load(item_path).convert_alpha()
        self.splat = self.load_a_image(SPLAT_IMAGE, SPLAT_DIR, (64, 64))
        # load sound
        self.music_path = self.load_a_thing(BG_MUSIC, MUSIC_DIR)
        pg.mixer.music.load(self.music_path)
        self.effects_sounds = {}
        for type in EFFECTS_SOUND:
            snd = self.load_a_thing(EFFECTS_SOUND[type], SOUND_DIR)
            snd = pg.mixer.Sound(snd)
            snd.set_volume(SOUND_VOLUME)
            self.effects_sounds[type] = snd
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(self.load_a_thing(snd, SOUND_DIR))
                s.set_volume(SOUND_VOLUME)
                self.weapon_sounds[weapon].append(s)
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            snd = pg.mixer.Sound(self.load_a_thing(snd, SOUND_DIR))
            snd.set_volume(SOUND_VOLUME)
            self.zombie_moan_sounds.append(snd)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            snd = pg.mixer.Sound(self.load_a_thing(snd, SOUND_PAIN_DIR))
            snd.set_volume(SOUND_VOLUME)
            self.player_hit_sounds.append(snd)
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            snd = pg.mixer.Sound(self.load_a_thing(snd, SOUND_DIR))
            snd.set_volume(SOUND_VOLUME)
            self.zombie_hit_sounds.append(snd)

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.items = pg.sprite.Group()
        # Maps:
        # self.map = Map(path.join(self.dir, MAP))
        map_path = self.load_a_thing(MAPS[0], MAPS_DIR)
        self.map = TiledMap(map_path)
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == '1':
        #             Wall(self, col, row)
        #         if tile == 'P':
        #             # create player:
        #             self.player = Player(self, col, row)
        #         if tile == 'M':
        #             Mob(self, col, row)
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'zombie':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name in ['health', 'shotgun']:
                Item(self, obj_center, tile_object.name)

        # self.player = Player(self, 5, 5)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.effects_sounds['level_start'].play()

    def run(self):
        # game loop - set  self.playing = False to end the game
        self.running = True
        pg.mixer.music.play(loops=-1)
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.
            self.events()
            if not self.paused:
                self.update()
            self.draw()
        self.show_go_screen()
        self.new()
        self.run()

    def events(self):
        for event in pg.event.get():
            self.handle_common_events(event)
            self.player.events(event)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused

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
        # game over?
        if len(self.mobs) == 0:
            self.playing = False
        # player hits items:
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for item_hit in hits:
            if item_hit.type == 'health' and\
                    self.player.health < PLAYER_HEALTH:
                item_hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
            if item_hit.type == 'shotgun':
                item_hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'shotgun'

        # Mobs hit player:
        hits = pg.sprite.spritecollide(self.player, self.mobs, False,
                                       collide_hit_rect)
        for hit in hits:
            if random.random() < 0.7:
                random.choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.running = False
        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullets hit mobs:
        mob_hits_bullets = pg.sprite.groupcollide(self.mobs, self.bullets,
                                                  False, True)
        for mob_hit, bullet_that_hit in mob_hits_bullets.items():
            # mob_hit.health -= WEAPONS[self.player.weapon]['damage'] *\
                # len(mob_hits_bullets[mob_hit])
            for bullet in bullet_that_hit:
                mob_hit.health -= bullet.damage

            mob_hit.vel = vec(0, 0)

    def draw_text(self, text, font_name, size, color, x, y, align='topleft'):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        setattr(text_rect, align, (x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_grid(self):
        # vertically:
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        # horizontally:
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption('fps: %.5s' % self.clock.get_fps())
        self.screen.blit(self.map_img, self.camera.apply(rect=self.map_rect))
        # self.screen.fill(BG_COLOR)
        # self.draw_grid()
        # self.all_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            try:
                if self.draw_debug:
                    pg.draw.rect(self.screen, CYAN,
                                 self.camera.apply(rect=sprite.hit_rect), 1)
            except AttributeError:
                pass
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN,
                             self.camera.apply(rect=wall.rect), 1)
        draw_player_health(self.screen, 10, 10,
                           float(self.player.health) / PLAYER_HEALTH)
        self.draw_text('Zombie: %s' % len(self.mobs), self.hud_font, 30, WHITE,
                       WIDTH - 10, 10, align='topright')
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text('Paused', self.title_font, 105, RED, WIDTH / 2,
                           HEIGHT / 2, 'center')
        pg.display.flip()

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text('GAME OVER', self.title_font, 100, RED, WIDTH / 2,
                       HEIGHT / 2, 'center')
        self.draw_text('Press a key to start', self.title_font, 75, WHITE,
                       WIDTH / 2, HEIGHT * 3 / 4, 'center')
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def quit(self):
        self.running = False


Game()
