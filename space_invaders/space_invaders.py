#! /usr/bin/python3

import pygame



SCREEN_WID = 800
SCREEN_HEI = 600

MAX_LFT = 25
MAX_RGT = SCREEN_WID - MAX_LFT

ALIEN_START = MAX_LFT
WIN_LINE    = SCREEN_WID - 100

ALIEN_ROWS = 5
ALIEN_COLS = 8

ALIEN_WID = 50

ALIEN_SPACING = 10

ALIEN_SPEED = 2
DOWN_STEPS  = 5

BULLET_SPEED = 10
GUN_SPEED    = 4



screen = pygame.display.set_mode( (SCREEN_WID, SCREEN_HEI) )

clock = pygame.time.Clock()



class Alien(pygame.sprite.Sprite):
    # this is a *class* property, so there's only one, shared by all the instances.
    image = pygame.image.load("black_alien.png").convert()
    image = pygame.transform.smoothscale_by(image, ALIEN_WID / image.get_width())
    image.set_colorkey((255,255,255), pygame.RLEACCEL)

    def __init__(self, pos):
        super(Alien,self).__init__()
        self.rect = self.image.get_rect()
        self.rect.left = pos[0]
        self.rect.top  = pos[1]

# TODO: add cities/shields above the gun

class Bullet(pygame.sprite.Sprite):
    # this is a *class* property, so there's only one, shared by all the instances.
    image = pygame.Surface((4,8))
    image.fill((0,0,0))

    def __init__(self):
        super(Bullet,self).__init__()
        self.rect = self.image.get_rect()

class Gun(pygame.sprite.Sprite):
    def __init__(self):
        super(Gun,self).__init__()
        self.surf = pygame.image.load("gun.png").convert()
        self.surf.set_colorkey((255,255,255), pygame.RLEACCEL)
        self.image = self.surf    # required by sprite.Group.draw()
        self.rect = self.surf.get_rect()
        self.rect.left   = (SCREEN_WID - self.image.get_width()) / 2
        self.rect.bottom =  SCREEN_HEI - self.image.get_height() - 10

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def spawn_bullet(self):
        retval = Bullet()
        retval.rect.left   = (self.rect.left+self.rect.right)/2 - retval.rect.width/2
        retval.rect.bottom =  self.rect.top
        return retval



direction  = 1   # move right.  -1 means left.  Ignored if down_count>0
down_count = 0



aliens = pygame.sprite.Group()

wid_each = ALIEN_WID                + ALIEN_SPACING
hei_each = Alien.image.get_height() + ALIEN_SPACING
for i in range(ALIEN_COLS):
    for j in range(ALIEN_ROWS):
        x = MAX_LFT     + wid_each * i
        y = ALIEN_START + wid_each * j

        aliens.add(Alien( (x,y) ))

bullets = pygame.sprite.Group()

gun = Gun()



running = True
while running:
    clock.tick(50)


    # DRAW EVERYTHING
    screen.fill( (255,255,255) )
    aliens .draw(screen)
    bullets.draw(screen)
    gun    .draw(screen)
    pygame.display.flip()


    # MOVE THE ALIENS
    if down_count > 0:
        for a in aliens:
            a.rect.top += ALIEN_SPEED
        down_count -= 1
    elif direction == 1:
        for a in aliens:
            a.rect.left += ALIEN_SPEED
        right = max(a.rect.right for a in aliens)
        if right >= MAX_RGT:
            direction = 0
            down_count = DOWN_STEPS
    elif direction == 0:
        for a in aliens:
            a.rect.left -= ALIEN_SPEED
        left = min(a.rect.left for a in aliens)
        if left <= MAX_LFT:
            direction = 1
            down_count = DOWN_STEPS

    # MOVE THE BULLETS
    for b in bullets:
        b.rect.top -= BULLET_SPEED


    # BULLETS HIT ALIENS?
    for b in bullets:
        hits = pygame.sprite.spritecollide(b, aliens, dokill=True)
        if len(hits) != 0:
            b.kill()
    # BULLETS OFF THE SCREEN?
    for b in bullets:
        if b.rect.bottom < 0:
            b.kill()


    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = FALSE

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == ord(' '):
                bullets.add(gun.spawn_bullet())

            if event.key == ord('a') or event.key == pygame.K_LEFT:
                gun.rect.left -= GUN_SPEED
            if event.key == ord('d') or event.key == pygame.K_RIGHT:
                gun.rect.left += GUN_SPEED

pygame.quit()

