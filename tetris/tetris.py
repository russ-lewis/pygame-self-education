#! /usr/bin/python3

import asyncio

import pygame
import random



SQUARE_SIZE = 40
SQUARE_PAD  = 2
SQUARE_DRAW_SIZE = SQUARE_SIZE - 2*SQUARE_PAD

CELLS_WID = 8
CELLS_HEI = 16

EDGE = 25

SCREEN_WID = EDGE + CELLS_WID*SQUARE_SIZE + EDGE
SCREEN_HEI = EDGE + CELLS_HEI*SQUARE_SIZE + EDGE



patterns = [ {"cells": [(0,0),(0, 1),( 0,-1),( 0,-2)], "color": (255,  0,  0), "rot":2},    # line
             {"cells": [(0,0),(0,-1),( 1, 0),( 1,-1)], "color": (  0,  0,255), "rot":1},    # square
             {"cells": [(0,0),(0, 1),(-1, 0),( 1, 0)], "color": (  0,255,  0), "rot":4},    # T
             {"cells": [(0,0),(0, 1),( 0, 2),( 1, 0)], "color": (255,  0,255), "rot":4},    # L
             {"cells": [(0,0),(0, 1),( 0, 2),(-1, 0)], "color": (255,255,  0), "rot":4},    # J
             {"cells": [(0,0),(0, 1),( 1, 0),( 1,-1)], "color": (  0,255,255), "rot":2},    # S
             {"cells": [(0,0),(0, 1),(-1, 0),(-1,-1)], "color": (255,255,255), "rot":2} ]   # Z

cells = [ [] for col in range(CELLS_WID) ]
def get_cell(x,y):
    assert x>=0 and x<CELLS_WID
    if len(cells[x]) <= y:
        return None
    return cells[x][y]



class Piece:
    def __init__(self):
        indx = random.randint(0,len(patterns)-1)

        self.cells = patterns[indx]["cells"]
        self.color = patterns[indx]["color"]
        self.rot   = patterns[indx]["rot"]

        self.rot_count  = 0
        self.cells_orig = self.cells

        self.center_x = CELLS_WID // 2
        self.center_y = CELLS_HEI-1 - max(c[1] for c in self.cells)
        assert self.check()

    def check(self):
        for c in self.cells:
            x = self.center_x + c[0]
            y = self.center_y + c[1]
            if x < 0 or x >= CELLS_WID or y < 0 or y >= CELLS_HEI:
                return False
            if get_cell(x,y) not in ["empty",None]:
                return False
        return True

    def draw(self, surf, validate=True):
        for c in self.cells:
            x = self.center_x + c[0]
            y = self.center_y + c[1]
            if validate:
                assert x >= 0 and x < CELLS_WID
                assert y >= 0 and y < CELLS_HEI

            draw_on_board(surf, x,y, self.color)

    def spin(self):
        self.rot_count += 1
        if self.rot_count == self.rot:
            # reset to original cells.  The square never rotates, and the line
            # S and Z pieces only rotate once before returning to their start.
            self.cells = self.cells_orig
            self.rot_count = 0

        else:
            new_cells = []
            for c in self.cells:
                x = c[0]
                y = c[1]
                new_cells.append( (y,-x) )

            # apply the change - but save the old position, just in case we
            # have to revert.  If you spin in some circumstances, part of the
            # piece goes off the board, and that isn't allowed
            save_cells = self.cells
            self.cells = new_cells
            if self.check() == False:
                self.cells = save_cells



def draw_on_board(surf, x_cells,y_cells, color):
    # in our internal representation, y=0 is the bottom row, but
    # when drawing, y=0 is the top pixel
    y_cells = CELLS_HEI-1 - y_cells

    # turn the x,y values (which were in units of cells) into pixels
    x = EDGE + x_cells*SQUARE_SIZE
    y = EDGE + y_cells*SQUARE_SIZE

    rect = pygame.Rect( (x+SQUARE_PAD,     y+SQUARE_PAD),
                        (SQUARE_DRAW_SIZE, SQUARE_DRAW_SIZE) )
    pygame.draw.rect(surf, color, rect)



game_over    = False
active_piece = None



async def flash_line(y):
    for i in range(5):
        for x in range(CELLS_WID):
            cells[x][y] = (255,255,255)
        await asyncio.sleep(.02)

        for x in range(CELLS_WID):
            cells[x][y] = (0,0,0)
        await asyncio.sleep(.02)



async def remove_complete_lines():
    rows = []

    for y in range(min(len(col) for col in cells)):
        hole_found = False
        for x in range(CELLS_WID):
            if cells[x][y] == "empty":
                hole_found = True
                break
        if not hole_found:
            rows.append(y)

    if len(rows) > 0:
        print("REMOVING", rows)
        actions = [flash_line(y) for y in rows]
        await asyncio.gather(*actions)

        # remove the rows, in reverse order
        for y in sorted(rows, reverse=True):
            for x in range(CELLS_WID):
                cells[x].pop(y)

        for x in range(CELLS_WID):
            while len(cells[x]) > 0 and cells[x][-1] == "empty":
                cells[x].pop()



async def piece_loop():
    global active_piece
    while True:
        active_piece = Piece()
        await one_piece_lifetime(active_piece)
        await remove_complete_lines()

async def one_piece_lifetime(piece):
    timer = asyncio.sleep(0)    # NOP

    while True:    # break out manually when we lock the piece
        await timer
        timer = asyncio.sleep(.5)    # TODO: increase speed over time

        piece.center_y -= 1
        if piece.check() == False:    # can't fall anymore
            piece.center_y += 1
            assert piece.check()

            # lock the piece in place, and we're done
            for c in sorted(piece.cells, key = lambda c: c[1]):
                x = piece.center_x + c[0]
                y = piece.center_y + c[1]
                assert get_cell(x,y) in [None, "empty"]

                assert y >= len(cells[x])   # can only add on top
                while len(cells[x]) < y:
                    cells[x].append("empty")

                cells[x].append(piece.color)

            # the piece dies
            break

    await timer     # TODO: is there a better way to clean this up?



def drop():
    active_piece.center_y -= 1
    if active_piece.check() == False:
        active_piece.center_y += 1
    # TODO: make it drop the whole way, but quickly

def move_LR(dir_):
    active_piece.center_x += dir_
    if active_piece.check() == False:
        active_piece.center_x -= dir_



async def pygame_main_loop():
    running = True

    screen = pygame.display.set_mode( (SCREEN_WID,SCREEN_HEI) )

    asyncio.create_task(piece_loop())

    timer = asyncio.sleep(0)    # NOP
    while running:

        # block until the previous timer has expired, representing one frame of
        # time.  Then set up another.  This should adapt well to heavy-CPU and
        # light-CPU circumstances.
        await timer
        timer = asyncio.sleep(.02)

        screen.fill( (0,0,0) )

        if active_piece:
            active_piece.draw(screen)

        for x in range(CELLS_WID):
            for y in range(len(cells[x])):
                color = cells[x][y]
                if color == "empty":
                    continue
                draw_on_board(screen, x,y, color)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if active_piece:
                    if event.key == ord('a') or event.key == pygame.K_LEFT:
                        move_LR(-1)
                    if event.key == ord('d') or event.key == pygame.K_RIGHT:
                        move_LR(1)
                    if event.key == ord('w') or event.key == pygame.K_UP:
                        active_piece.spin()
                    if event.key == ord('s') or event.key == pygame.K_DOWN:
                        drop()

    await timer   # to remove the warning.  TODO: can I just kill this?
    pygame.quit()

asyncio.run(pygame_main_loop())

