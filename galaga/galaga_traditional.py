#! /usr/bin/python3

import asyncio

import pygame
import random

import galaga_common
from galaga_common import *



screen = pygame.display.set_mode( (SCREEN_WID, SCREEN_HEI) )



class Galaga:
    def __init__(self):
        pass



class Galaga_LoadingScreen(Galaga_ModeBase):
    def __init__(self, game):
        super(Galaga_LoadingScreen,self).__init__(game)
        self.msg = ms_font.render("Click mouse or hit ENTER to start game", False, "white")


    def draw(self, surf):
        window_center = surf.get_rect().center
        msg_size      = self.msg.get_rect()

        lft = window_center[0] - msg_size.width  / 2
        top = window_center[1] - msg_size.height / 2

        surf.fill("black")
        surf.blit(self.msg, (lft,top))
        pygame.display.flip()


    def quit(self):
        global cur_mode
        cur_mode = None

    def start_game(self):
        global cur_mode
        cur_mode = Galaga_LoadStage(self.game, 1)

    def key_down(self, key):
        if key == pygame.K_ESCAPE or key == ord('q'):
            self.quit()
        if key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
            self.start_game()

    def mouse_button_down_left(self):
        self.start_game()

    def tick(self):
        pass



class Galaga_LoadStage(Galaga_ModeBase):
    def __init__(self, game,stage_num):
        super(Galaga_LoadStage,self).__init__(game)
        self.game      = game
        self.stage_num = stage_num
        self.msg       = ms_font.render(f"Stage {stage_num} - Ready!", False, "white")
        self.countdown = 2 * CLOCK_HZ

    def draw(self, surf):
        window_center = surf.get_rect().center
        msg_size      = self.msg.get_rect()

        lft = window_center[0] - msg_size.width  / 2
        top = window_center[1] - msg_size.height / 2

        surf.fill( (0,0,0) )
        surf.blit(self.msg, (lft,top))
        pygame.display.flip()

    def tick(self):
        assert self.countdown > 0
        self.countdown -= 1
        if self.countdown == 0:
            global cur_mode
            cur_mode = Galaga_Stage(self.game, self.stage_num)



class Galaga_Stage(Galaga_ModeBase):
    def __init__(self, game,stage_num):
        super(Galaga_Stage,self).__init__(game)
        self.stage_num = stage_num

        self.fighter_x = SCREEN_WID//2 - FIGHTER_WID//2

        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.stars   = pygame.sprite.Group()
        for i in range(100):
            self.stars.add(Galaga_Star())

        # the "script" tells you which enemies arrive on screen at what time,
        # and what path they take.  It only handles the initial "assembly" of
        # the enemies, it doesn't handle the dives that they perform later.
        self.script = Galaga_Script(stage_num, self)

        self.tick_count = 0

    def draw(self, surf):
        surf.fill("black")

        self.stars  .draw()
        self.enemies.draw()
        self.bullets.draw()

        pygame.display.flip()

    def key_down(self, key):
        if key == pygame.K_ESCAPE:
            self.game.push_mode( Galaga_PauseMenu() )

    def tick(self):
        pass



class Galaga_PauseMenu(Galaga_ModeBase):
    def __init__(self, game):
        super(Galaga_PauseMenu,self).__init__(game)

    def tick(self):
        pass



game = Galaga()

clock = pygame.time.Clock()
cur_mode = Galaga_LoadingScreen(game)

while cur_mode is not None:
    clock.tick(CLOCK_HZ)

    cur_mode.draw(screen)
    cur_mode.dispatch_events()

    if cur_mode is not None:
        cur_mode.tick()

pygame.quit()

