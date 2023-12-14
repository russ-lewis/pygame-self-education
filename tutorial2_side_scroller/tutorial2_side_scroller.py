#! /usr/bin/python3

# https://www.geeksforgeeks.org/creating-a-scrolling-background-in-pygame/

import pygame
import math



clock = pygame.time.Clock()

FRAME_HEI = 600
FRAME_WID = 800

pygame.display.set_caption("Tutorial2 - Side Scroller")
screen = pygame.display.set_mode( (FRAME_WID,FRAME_HEI) )

bg = pygame.image.load("russ_costume_1.jpg").convert()   # TODO: do we need to optimize, like in tutorial1?

# scale the image so that its height matches the window.  It will be scrolled
# in both dimensions, but regulated only in the height
bg = pygame.transform.smoothscale_by(bg, FRAME_HEI / bg.get_height())



scroll_pos = 0
tiles = math.ceil(FRAME_WID / bg.get_width()) + 1



running = True
while running:
    clock.tick(50)


    screen.fill( (0,0,0) )

    # THE BACKGROUND IS MADE OF MANY COPIES OF bg
    for i in range(tiles):
        x_offset = bg.get_width()*i - scroll_pos
        screen.blit(bg, (x_offset,0))

        if screen.get_height() > bg.get_height()+10:
            pygame.draw.line(screen, (0,255,0), (x_offset, bg    .get_height()+10),
                                                (x_offset, screen.get_height()),
                             width=4)

    # UPDATE THE SCROLL POSITION FOR NEXT TIME.  LOOP WHEN YOU HIT
    # THE WIDTH OF A bg TILE
    scroll_pos += 6
    if scroll_pos >= bg.get_width():
        scroll_pos -= bg.get_width()



    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = FALSE

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.VIDEORESIZE:
            tiles = math.ceil(event.w / bg.get_width()) + 1


    pygame.display.flip()

pygame.quit()

