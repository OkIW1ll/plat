import pygame as pg
from settings import *
from random import choice, randrange
vec = pg.math.Vector2

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height// 2))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.invince = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (0 + 40, HEIGHT - 40)
        self.pos = vec(0 + 30, HEIGHT - 40)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        self.zstanding_frames = [self.game.spritesheet5.get_image(0, 231, 66, 82),
                                self.game.spritesheet5.get_image(0, 0, 68, 67)]
        for frame in self.zstanding_frames:
            frame.set_colorkey(BLACK)

        self.walk_frames_zr = [self.game.spritesheet5.get_image(0, 313, 68, 83),
                               self.game.spritesheet5.get_image(0, 396, 70, 86)]

        self.walk_frames_zl = []
        for frame in self.walk_frames_zr:
            frame.set_colorkey(BLACK)
            self.walk_frames_zl.append(pg.transform.flip(frame, True, False))

        self.zjump_frame = self.game.spritesheet5.get_image(0, 148, 67, 83)
        self.zjump_frame.set_colorkey(BLACK)

        self.standing_frames = [self.game.spritesheet.get_image(67, 196, 66, 92),
                                self.game.spritesheet.get_image(365, 98, 69, 71)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)

        self.walk_frames_r = [self.game.spritesheet.get_image(0, 0, 72, 97),
                             self.game.spritesheet.get_image(73, 0, 72, 97),
                             self.game.spritesheet.get_image(146, 0, 72, 97),
                             self.game.spritesheet.get_image(0, 98, 72, 97),
                             self.game.spritesheet.get_image(73, 98, 72, 97),
                             self.game.spritesheet.get_image(146, 98, 72, 97),
                             self.game.spritesheet.get_image(219, 0, 72, 97),
                             self.game.spritesheet.get_image(292, 0, 72, 97),
                             self.game.spritesheet.get_image(219, 98, 72, 97),
                             self.game.spritesheet.get_image(365, 0, 72, 97),
                             self.game.spritesheet.get_image(292, 98, 72, 97)]

        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))

        self.jump_frame = self.game.spritesheet.get_image(438, 93, 67, 94)
        self.jump_frame.set_colorkey(BLACK)

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        #self.rect.x += 3
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        #self.rect.x -= 3
        if hits and not self.jumping:
            self.jumping = True
            self.game.jump_sound.play()
            self.vel.y = -PLAYER_JUMP

    def update(self):
        if self.invince:
            self.zanimate()
            now = pg.time.get_ticks()
            if now > 50000:
                self.invince = False

        if not self.invince:
            self.animate()
        else:
            self.zanimate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.3:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos

        pow_hits = pg.sprite.spritecollide(self, self.game.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.game.boost_sound.play()
                self.vel.y = -BOOST_POWER
                self.jumping = False
            if pow.type == 'no_hit':
                self.game.no_hit_sound.play()
                self.invince = True

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        if self.walking:
            if now - self.last_update > 75:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if self.jumping:
            self.image = self.jump_frame
        if not self.walking and not self.jumping:
            if now - self.last_update > 250:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.mask = pg.mask.from_surface(self.image)

    def zanimate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        if self.walking:
            if now - self.last_update > 75:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_zl)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_zr[self.current_frame]
                else:
                    self.image = self.walk_frames_zl[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if self.jumping:
            self.image = self.zjump_frame
        if not self.walking and not self.jumping:
            if now - self.last_update > 250:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.zstanding_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.mask = pg.mask.from_surface(self.image)

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAT_LAYER
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet2.get_image(576, 432, 70, 70),
                self.game.spritesheet2.get_image(360, 432, 70, 70),
                self.game.spritesheet2.get_image(720, 360, 140, 70)]
        self.image = choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < POW_SPAWN_PCT:
            Pow(self.game, self)

class Pow(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(['boost', 'no_hit'])
        if self.type == 'boost':
            self.image = self.game.spritesheet2.get_image(432, 0, 70, 70)
        elif self.type == 'no_hit':
            self.image = self.game.spritesheet2.get_image(288, 720, 70, 70)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()

class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_fly1 = self.game.spritesheet3.get_image(0, 32, 72, 36)
        self.image_fly1.set_colorkey(BLACK)
        self.image_fly2 = self.game.spritesheet3.get_image(0, 0, 75, 31)
        self.image_fly2.set_colorkey(BLACK)
        self.image = self.image_fly1
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT / 2)
        self.vy = 0
        self.dy = 0.5

    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_fly1
        else:
            self.image = self.image_fly2
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = center
        self.rect.y +=self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()

class Cloud(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = CLOUD_LAYER
        self.groups = game.all_sprites, game.clouds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = choice(self.game.cloud_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        scale = randrange(50, 71) / 100
        self.image = pg.transform.scale(self.image, (int(self.rect.width * scale),
                                        int(self.rect.height * scale)))
        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(-500, -50)

    def update(self):
        if self.rect.top > HEIGHT * 2:
            self.kill()
