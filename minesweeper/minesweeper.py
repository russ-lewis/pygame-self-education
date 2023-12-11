#! /usr/bin/python3

# https://realpython.com/pygame-a-primer/

import pygame
from pygame.locals import (K_ESCAPE,
                           KEYDOWN, QUIT,
                           MOUSEBUTTONUP)

import random



pygame.init()



CELLS_WID = 30
CELLS_HEI = 16

BOMB_COUNT = 99

COLOR_UNEXPLORED = (128,128,128)
COLOR_BG         = (192,192,192)

CELL_SIZE = 40
CELL_BORDER = 2
CELL_SIZE2 = CELL_SIZE - 2*CELL_BORDER

SCREEN_WIDTH  = CELLS_WID * CELL_SIZE
SCREEN_HEIGHT = CELLS_HEI * CELL_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



pygame.font.init()
monospace = pygame.font.SysFont("Courier New", 48)
monospace.set_bold(True)

numbers = {}
for i in range(1,10):
    # TODO: center these
    numbers[i] = monospace.render(str(i), False, (0,0,255))

# TODO: make these bitmaps
flag = monospace.render("F", False, (255,0,0))
bomb = monospace.render("B", False, (255,0,0))




# this is what the user sees.  Empty means unexposed.  0 means
# open; integer in [1,8] means draw number.  "flag" means draw
# a flag.  "bomb" means bomb exposed (only used at end)
cells = {}



# this is the true (hidden) state a set of all of the bombs in
# the map
bombs = set()
while len(bombs) < BOMB_COUNT:
    x = random.randint(0,CELLS_WID-1)
    y = random.randint(0,CELLS_HEI-1)

    # duplicates are fine; they don't change the set!
    bombs.add( (x,y) )
bombs = frozenset(bombs)



def handle_click(cells, bombs, pos):
    x = pos[0] // CELL_SIZE
    y = pos[1] // CELL_SIZE

    if x < 0 or y < 0 or x >= CELLS_WID or y >= CELLS_HEI:
        print(f"BEEP mouse out of bounds.  x,y={x},{y}")
        return False

    return open_cell(cells, bombs, x,y)

def open_cell(cells, bombs, x,y):
    assert x >= 0 and y >= 0 and x < CELLS_WID and y < CELLS_HEI

    if (x,y) in cells:
        # ignore, already opened (or flagged)
        return False

    if (x,y) in bombs:
        cells[(x,y)] = "bomb"
        for x in range(0,CELLS_WID):
          for y in range(0,CELLS_HEI):
            if (x,y) not in bombs and (x,y) in cells and cells[(x,y)] == "flag":
                print("TODO: handle bad-flag")
        return True

    # the cell needs to be opened.  It is safe; how many adjacent
    # bombs do we find?
    count = 0
    for search_x in range(x-1,x+2):
      for search_y in range(y-1,y+2):
        # it's harmless if we search invalid coordinates, since we're doing an
        # in-search on a set
        if (search_x,search_y) in bombs:
            count += 1

    cells[(x,y)] = count

    # if the cell was 0, then open all adjacent cells.  This needs to be aware
    # of the edges, though, so this loop is a tiny bit more complex
    if count == 0:
        for recurse_x in range(x-1,x+2):
            if recurse_x < 0 or recurse_x == CELLS_WID:
                continue

            for recurse_y in range(y-1,y+2):
                if recurse_y < 0 or recurse_y == CELLS_HEI:
                    continue

                if (recurse_x,recurse_y) in cells:
                    continue    # this cell is already open (including the self-recurse case)

                retval = open_cell(cells, bombs, recurse_x,recurse_y)
                assert retval == False

    return False



def toggle_flag(cells, pos):
    x = pos[0] // CELL_SIZE
    y = pos[1] // CELL_SIZE

    if x < 0 or y < 0 or x >= CELLS_WID or y >= CELLS_HEI:
        print(f"BEEP mouse out of bounds.  x,y={x},{y}")
        return False

    if (x,y) not in cells:
        cells[(x,y)] = "flag"

    else:
        cell = cells[(x,y)]

        if cell == "flag":
            del cells[(x,y)]
        elif type(cell) == int:
            pass      # NOP
        else:
            assert cell == "bomb"



running = True
bomb_hit = False
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            else:
                print(f"BEEP key={event.key}=0x{event.key:02x}")   # TODO

        if event.type == MOUSEBUTTONUP:
            if bomb_hit:
                continue    # ignore the mouse once you hit

            if event.button == 1:
                if handle_click(cells, bombs, pygame.mouse.get_pos()) == True:
                    bomb_hit = True
                    bombs_all_revealed = False
                    revelation_clock = pygame.time.Clock()

            elif event.button == 3:   # right click
                toggle_flag(cells, pygame.mouse.get_pos())

            else:
                print(f"BEEP button={event.button}")    # TODO

    if bomb_hit and not bombs_all_revealed:
        found = False
        for b in bombs:
            if b not in cells:
                cells[b] = "bomb"
                found = True
                revelation_clock.tick(10)
                break                 # only reveal one bomb at a time
        if not found:
            bombs_all_revealed = True

    screen.fill( COLOR_BG )

    for x in range(CELLS_WID):
      for y in range(CELLS_HEI):
        top = y*CELL_SIZE + CELL_BORDER
        lft = x*CELL_SIZE + CELL_BORDER

        if (x,y) not in cells:
            pygame.draw.rect(screen, COLOR_UNEXPLORED, (lft,top, CELL_SIZE2,CELL_SIZE2) )

        else:
            cell = cells[(x,y)]

            if cell == 0:
                continue        # open cell, draw nothing

            elif cell == "flag":
                pygame.draw.rect(screen, COLOR_UNEXPLORED, (lft,top, CELL_SIZE2,CELL_SIZE2) )
                screen.blit(flag, (lft,top))
            elif cell == "bomb":
                screen.blit(bomb, (lft,top))
            else:
                assert(type(cell) == int)
                screen.blit(numbers[cell], (lft,top))


    # TODO

    pygame.display.flip()

pygame.quit()

