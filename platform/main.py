import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'Player')
        img_dir2 = path.join(self.dir, 'Tiles')
        img_dir3 = path.join(self.dir, 'Enemies')
        img_dir4 = path.join(self.dir, 'Items')
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump17.wav'))
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Powerup2.wav'))
        self.no_hit_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Powerup7.wav'))
        self.death_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Hit_Hurt15.wav'))
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.spritesheet2 = Spritesheet(path.join(img_dir2, SS2))
        self.spritesheet3 = Spritesheet(path.join(img_dir3, SS3))
        self.spritesheet4 = Spritesheet(path.join(img_dir4, SS4))
        self.spritesheet5 = Spritesheet(path.join(img_dir, SS5))
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pg.image.load(path.join(img_dir4, 'cloud{}.png'.format(i))).convert())

    def new(self):
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.player = Player(self)
        for plat in PLATFORM_LIST:
            Platform(self, *plat)
        self.mob_timer = 0
        pg.mixer.music.load(path.join(self.snd_dir, 'Vocals.ogg'))
        for i in range(8):
            c = Cloud(self)
            c.rect.y += 500
        self.run()

    def run(self):
        pg.mixer.music.play(loops=-1)
        self.playing = True
        PLAYER_FRICTION = -0.12
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
        self.all_sprites.update()

        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)

        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if mob_hits and not self.player.invince:
            self.death_sound.play()
            self.playing = False

        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 10 and \
                self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
        if self.player.rect.top <= HEIGHT / 4:
            if random.randrange(100) < 8:
                Cloud(self)
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y / (randrange(2, 10))), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)
                if mob.rect.top >= HEIGHT:
                    mob.kill()

        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.death_sound.play()
            self.playing = False

        while len(self.platforms) < 6:
            height = random.randrange(5, 25)
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH-width),
                     random.randrange(-56, -25))

        if self.score >= 1000:
            PLAYER_FRICTION = -0.002

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.jump()
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    self.player.jump_cut()
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 33, BLUE, WIDTH / 2, 15)
        pg.display.flip()

    def show_start_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir, 'Element.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, YELLOW, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrow keys to move, space bar to jump", 22, YELLOW, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Push enter key to begin", 22, YELLOW, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("Record Score: " + str(self.highscore), 22, YELLOW, WIDTH / 2, 15)
        self.draw_text("Game over sceen with a new record and start screen music by Trevor Lentz", 15, YELLOW, WIDTH / 2, HEIGHT * 3 / 4 + 100)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text("Too Bad...", 48, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Your Score: " + str(self.score), 22, YELLOW, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press enter to try again", 22, RED, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            pg.mixer.music.load(path.join(self.snd_dir, 'Binary Architect.ogg'))
            pg.mixer.music.play(loops=-1)
            self.highscore = self.score
            self.draw_text("But... you did beat the record.", 22, BLUE, WIDTH / 2, HEIGHT / 4 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.highscore))
        else:
            pg.mixer.music.load(path.join(self.snd_dir, 'Smiles Outside.ogg'))
            pg.mixer.music.play(loops=-1)
            self.draw_text("Record Score: " + str(self.highscore), 22, YELLOW, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                keys = pg.key.get_pressed()
                if keys[pg.K_RETURN]:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, False, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
