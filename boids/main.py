#! /usr/bin/python3

import numpy as np
import random



class Character:
    def __init__(self, pos):
        self.pos = np.array(pos, float)
        self.prevPos = np.array(pos, float)
        self.acceleration = np.array((0, 0), float)

        speed = 1
        self.pos += (
            random.random() * speed * 2 - speed,
            random.random() * speed * 2 - speed
        )

        self.color = [random.randint(0, 100), random.randint(0, 255), random.randint(155, 255)]
        random.shuffle(self.color)
    
    def vel(self):
        return self.pos - self.prevPos
    
    def update(self, characters):


        sep_weight = 300
        ali_weight = 1
        coh_weight = 1.4

        sep_exponent = 1.1


        acceleration = 0.5

        drag_scale = 100
        drag_exponent = 2






        vel = self.vel()
        vel = vel + self.acceleration

        # drag force
        vm = np.linalg.norm(vel)
        vu = vel / vm
        vel -= vu * vm**drag_exponent / drag_scale

        self.prevPos = self.pos * 1
        self.pos += vel





        



        
        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[1] < 0:
            self.pos[1] = 0
        if self.pos[0] > 1500:
            self.pos[0] = 1500
        if self.pos[1] > 750:
            self.pos[1] = 750


        self.acceleration *= 0

        for c in characters:
            if c == self:
                continue

            dx = c.pos - self.pos
            dxm = np.linalg.norm(dx)
            dxu = dx / dxm

            dv = c.vel() - self.vel()
            dvm = np.linalg.norm(dv)
            dvu = dv / dvm


            # separation
            # if dm < 50:
            self.acceleration -= dxu / dxm ** sep_exponent * sep_weight

            # alignment
            self.acceleration += dvu * ali_weight

            # cohesion
            self.acceleration += dxu * coh_weight

        # # boundaries
        # if self.pos[0] < 100:
        #     self.acceleration[0] += 1000
        # if self.pos[1] < 100:
        #     self.acceleration[1] += 1000
        # if self.pos[0] > 600:
        #     self.acceleration[0] -= 1000
        # if self.pos[1] > 600:
        #     self.acceleration[1] -= 1000

        if self.acceleration.any():
            self.acceleration /= np.linalg.norm(self.acceleration) / acceleration
            print(np.linalg.norm(self.vel()))

    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, np.array(self.pos, int), 5)




characters = []


# c = Character((300, 300))
# c.pos -= 1
# characters.append(c)


for i in range(25):
    c = Character((random.random()*1500, random.random()*750))
    characters.append(c)




import pygame

pygame.init()

SCREEN = pygame.display.set_mode((1500, 750))
pygame.display.set_caption(__name__)
CLOCK = pygame.time.Clock()


# held_character = None


while pygame.get_init():
    CLOCK.tick(60)


    SCREEN.fill("black")

    for c in characters:
        c.draw(SCREEN)

    pygame.display.flip()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        elif event.type == pygame.KEYDOWN:
            pass

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # held_character = None
        
        # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            held_character = Character(pygame.mouse.get_pos())
            characters.append(held_character)

    # if held_character:
    #     held_character.pos *= 0
    #     held_character.pos += pygame.mouse.get_pos()


    for c in characters:
        c.update(characters)
