#! /usr/bin/python3

import numpy as np



points = [
    (500, 500),
    (550, 400),
    (600, 500),
]
connections = []
fixed_points = []
forces_at_points = []


def draw():
    SCREEN.fill("black")

    # for c in characters:
    #     c.draw(SCREEN)
    for p in points:
        pygame.draw.circle(SCREEN, "white", p, 3)

    pygame.display.flip()

def user_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        elif event.type == pygame.KEYDOWN:
            pass

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pass
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pass

def update():
    pass


import pygame

pygame.init()

SCREEN = pygame.display.set_mode((1500, 750))
pygame.display.set_caption(__name__)
clock = pygame.time.Clock()

while pygame.get_init():
    clock.tick(60)

    draw()

    user_input()

    update()

# if __name__ == "__main__":
#     main()
