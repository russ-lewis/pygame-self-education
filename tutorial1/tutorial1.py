#! /usr/bin/python3

# https://realpython.com/pygame-a-primer/

import pygame
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE,
                           KEYDOWN, QUIT,
                           RLEACCEL,
                           MOUSEMOTION)

import random
import math



pygame.init()

ADD_ENEMY = pygame.USEREVENT+1
pygame.time.set_timer(ADD_ENEMY, 250)

clock = pygame.time.Clock()



# TODO: enable when you figure out how to make it work from WSL.
# TODO: auto-detect whether it will work, and live without it
#
# pygame.mixer.init()
# pygame.mixer.music.load("valkyries.mp3")
# pygame.mixer.music.play(loops=-1)



SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        tmp = pygame.image.load("spacey.svg").convert()
        self.surf = pygame.Surface((118,37))
        self.surf.blit(tmp, (0,0))
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.image = self.surf    # required by sprite.Group.draw()
        self.rect = self.surf.get_rect()

    def handle_keys(self, keys):
        if keys[K_UP]:
            self.rect.move_ip(0,-5)
            if self.rect.top < 0:
                self.rect.top = 0
        if keys[K_DOWN]:
            self.rect.move_ip(0,5)
            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
        if keys[K_LEFT]:
            self.rect.move_ip(-5,0)
            if self.rect.left < 0:
                self.rect.left = 0
        if keys[K_RIGHT]:
            self.rect.move_ip(5,0)
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()
        tmp = pygame.image.load("missile_0.png").convert()
        self.surf = pygame.transform.flip(tmp, True,False)
        self.surf.set_colorkey((255,255,255), pygame.RLEACCEL)
        self.image = self.surf    # required by sprite.Group.draw()
        self.rect = self.surf.get_rect(
                         center=(
                             random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
                             random.randint(0, SCREEN_HEIGHT)
                         ))
        self.speed = random.randint(5,20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if (self.rect.right < 0):
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud,self).__init__()
        tmp = pygame.image.load("cloud.png").convert()
        self.surf = pygame.transform.scale_by(tmp, random.randint(3,5))
        self.surf.set_colorkey((255,255,255), pygame.RLEACCEL)
        self.image = self.surf    # required by sprite.Group.draw()
        self.rect = self.surf.get_rect(
                         center=(
                             random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
                             random.randint(0, SCREEN_HEIGHT)
                         ))
        self.speed = random.randint(2,5)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if (self.rect.right < 0):
            self.kill()

class CrossHairs(pygame.sprite.Sprite):
    def __init__(self):
        super(CrossHairs,self).__init__()
        self.surf = self.image = pygame.Surface((40,40))
        self.surf.fill((0,0,0))
        self.surf.set_colorkey((0,0,0))
        pygame.draw.rect(self.surf, (255,0,0), (18, 0,4,18))
        pygame.draw.rect(self.surf, (255,0,0), (18,22,4,18))
        pygame.draw.rect(self.surf, (255,0,0), ( 0,18,18,4))
        pygame.draw.rect(self.surf, (255,0,0), (22,18,18,4))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos,vel):
        super(Bullet,self).__init__()
        self.surf = self.image = pygame.Surface((4,4))
        self.surf.fill((0,255,255))
        self.rect = self.surf.get_rect()

        self.pos = pos   # separate from self.rect because we need to support floats
        self.vel = vel

    def update(self):
        self.pos  = ( self.pos[0]+self.vel[0], self.pos[1]+self.vel[1] )
        self.rect.left = self.pos[0]
        self.rect.top  = self.pos[1]



enemies    = pygame.sprite.Group()
clouds     = pygame.sprite.Group()
bullets    = pygame.sprite.Group()

bg_sprites = pygame.sprite.Group()
fg_sprites = pygame.sprite.Group()
ui_sprites = pygame.sprite.Group()

player = Player()
fg_sprites.add(player)

crosshairs = CrossHairs()
ui_sprites.add(crosshairs)



TICKS_PER_BULLET = 5
ticks_to_next_bullet = TICKS_PER_BULLET

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        if event.type == ADD_ENEMY:
            new_enemy = Enemy()
            enemies   .add(new_enemy)
            fg_sprites.add(new_enemy)

            if random.randint(0,5) == 0:
                new_cloud = Cloud()
                clouds    .add(new_cloud)
                bg_sprites.add(new_cloud)

        if event.type == MOUSEMOTION:
            crosshairs.rect.center = pygame.mouse.get_pos()

    player.handle_keys(pygame.key.get_pressed())
    enemies.update()
    clouds .update()
    bullets.update()

    ticks_to_next_bullet -= 1
    if ticks_to_next_bullet == 0:
        ticks_to_next_bullet = TICKS_PER_BULLET

        BULLET_SPEED = 5
        player_pos     =     player.rect.center
        crosshairs_pos = crosshairs.rect.center
        fire_dir = ( crosshairs_pos[0]-player_pos[0],
                     crosshairs_pos[1]-player_pos[1] )
        fire_mag = math.sqrt( fire_dir[0]**2 + fire_dir[1]**2 )
        fire_vec = ( fire_dir[0]*BULLET_SPEED/fire_mag, fire_dir[1]*BULLET_SPEED/fire_mag )
        new_bullet = Bullet(player_pos, fire_vec)
        bullets   .add(new_bullet)
        fg_sprites.add(new_bullet)

    screen.fill( (0,0,192) )

#    for entity in bg_sprites:
#        screen.blit(entity.surf, entity.rect)
#    for entity in fg_sprites:
#        screen.blit(entity.surf, entity.rect)
    bg_sprites.draw(screen)
    fg_sprites.draw(screen)
    ui_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(30)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    for b in bullets:
        hits = pygame.sprite.spritecollide(b, enemies, dokill=True)
        if len(hits) != 0:
            b.kill()

pygame.quit()

