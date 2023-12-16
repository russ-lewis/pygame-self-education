#! /usr/bin/python3

import asyncio
import pygame
import random
import math



SCREEN_WID = 800
SCREEN_HEI = 600

MAX_RAD = 100

CLOCK_HZ   = 50
CLOCK_TICK = 1 / CLOCK_HZ

RAD_2_DEG = math.pi / 180



class Clock:
    def __init__(self):
        self.radius = random.randint(10,MAX_RAD)

        self.color = [random.randint(10,255) for i in range(3)]

        self.clock_pos = random.randint(0, 12*360-1)
        self.clock_vel = random.randint(1,10)

        self.pos    = [random.randint(self.radius, SCREEN_WID-self.radius),
                       random.randint(self.radius, SCREEN_HEI-self.radius)]
        self.vel    = [random.randint(-5,5),
                       random.randint(-5,5)]

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, self.pos, self.radius, width=3)

        hour_ang = self.clock_pos / 12 * RAD_2_DEG
        min_ang  = self.clock_pos      * RAD_2_DEG

        hour_hand = [ self.pos[0] + math.cos(hour_ang)*self.radius*3/4,
                      self.pos[1] + math.sin(hour_ang)*self.radius  /2 ]
        min_hand  = [ self.pos[0] + math.cos( min_ang)*self.radius*3/4,
                      self.pos[1] + math.sin( min_ang)*self.radius  /2 ]

        pygame.draw.line(surf, (0,0,0), self.pos, hour_hand)
        pygame.draw.line(surf, (0,0,0), self.pos,  min_hand)

    async def run(self):
        tick = asyncio.sleep(0)
        while True:
            await tick
            tick = asyncio.sleep(CLOCK_TICK)

            self.clock_pos += self.clock_vel

            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]

            if self.pos[0] - self.radius <= 0 or self.pos[0] + self.radius >= SCREEN_WID:
                self.vel[0] *= -1
            if self.pos[1] - self.radius <= 0 or self.pos[1] + self.radius >= SCREEN_HEI:
                self.vel[1] *= -1



screen = pygame.display.set_mode( (SCREEN_WID, SCREEN_HEI) )

loop = asyncio.get_event_loop()

clocks = []
background_tasks = [loop.create_task(c.run()) for c in clocks]



def add_clock():
    new_clock = Clock()
    clocks.append(new_clock)
    background_tasks.append( loop.create_task(new_clock.run()) )

async def clock_creator_thread():
    add_clock()
    while True:
        await asyncio.sleep( random.randint(2,5) )
        add_clock()

background_tasks.append( loop.create_task(clock_creator_thread()) )



running = True
while running:
    screen.fill( (255,255,255) )

    for c in clocks:
        c.draw(screen)

    pygame.display.flip()


    # this is a total hack, but according to
    #     https://blubberquark.tumblr.com/post/177559279405/asyncio-for-the-working-pygame-programmer-part-i
    # it's the "correct" way to "run one iteration of the event loop"
    loop.call_soon(loop.stop)
    loop.run_forever()








