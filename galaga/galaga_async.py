#! /usr/bin/python3

import asyncio

import pygame
import random

from galaga_common import *



class AsyncTicks:
    def __init__(self, tick_time):
        self.tick_time = tick_time
        self.cur_task = None

    def get_task(self):
        if self.cur_task is None:
            self.cur_task = asyncio.create_task(self.one_tick())
        return self.cur_task

    async def one_tick(self):
        await asyncio.sleep(self.tick_time)
        self.cur_task = None
        return True

    async def sleep(self, ticks):
        assert ticks >= 0
        if ticks == 0:
            return asyncio.sleep(0)

        # TODO: make this more advanced than a loop.  Just wait, and get woken
        # by some sleeper task.

        for i in range(ticks):
            await self.get_task()



class AsyncPygame:
    def __init__(self, wid,hei, tick_time):
        self.clock    = AsyncTicks(tick_time)

        self.screen = pygame.display.set_mode( (wid,hei) )

        self.cur_mode = None       # must be overridden by child before calling mainloop()
        self.new_mode = None

    def sleep(self, ticks):
        return self.clock.sleep(ticks)

    def mainloop(self):
        async def both():
            await asyncio.gather(self.modeloop(), self.utilloop())
        asyncio.run(both())

    async def modeloop(self):
        while self.cur_mode is not None:
            self.cur_mode = await self.cur_mode.main()

    async def utilloop(self):
        while self.cur_mode is not None:
            self.cur_mode.draw(self.screen)
            self.cur_mode.dispatch_events()

            await self.sleep(1)

    def push_mode(self, new_mode):
        TODO    # critical do not change the mode immediately, or pending events being dispatched by the for loop in the mode's dispatch_events() might get lost!

        TODO    #  maybe push_mode() should be a method of the Mode class???

        assert self.new_mode == new_mode
        self.new_mode = new_mode



class Galaga(AsyncPygame):
    def __init__(self):
        super(Galaga,self).__init__(SCREEN_WID,SCREEN_HEI, CLOCK_TICK)
        self.cur_mode = Galaga_LoadingScreen(self)



class Galaga_LoadingScreen(Galaga_ModeBase):
    def __init__(self, game):
        super(Galaga_LoadingScreen,self).__init__(game)
        self.msg = ms_font.render("Click mouse or hit ENTER to start game", False, "white")


    async def main(self):
        self.mode_complete = asyncio.get_event_loop().create_future()
        return await self.mode_complete


    def draw(self, surf):
        window_center = surf.get_rect().center
        msg_size      = self.msg.get_rect()

        lft = window_center[0] - msg_size.width  / 2
        top = window_center[1] - msg_size.height / 2

        surf.fill("black")
        surf.blit(self.msg, (lft,top))
        pygame.display.flip()


    def quit(self):
        self.mode_complete.set_result(None)

    def start_game(self):
        self.mode_complete.set_result( Galaga_LoadStage(self.game, 1) )

    def key_down(self, key):
        if key == pygame.K_ESCAPE or key == ord('q'):
            self.quit()
        if key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
            self.start_game()

    def mouse_button_down_left(self):
        self.start_game()



class Galaga_LoadStage(Galaga_ModeBase):
    def __init__(self, game,stage_num):
        super(Galaga_LoadStage,self).__init__(game)
        self.stage_num = stage_num
        self.msg       = ms_font.render(f"Stage {stage_num} - Ready!", False, "white")

    async def main(self):
        await asyncio.sleep(2)
        return Galaga_Stage(self.game, self.stage_num)

    def draw(self, surf):
        window_center = surf.get_rect().center
        msg_size      = self.msg.get_rect()

        lft = window_center[0] - msg_size.width  / 2
        top = window_center[1] - msg_size.height / 2

        surf.fill( (0,0,0) )
        surf.blit(self.msg, (lft,top))
        pygame.display.flip()

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

    async def main(self):
        await asyncio.sleep(2)
        print("TODO")
        return None

    def draw(self, surf):
        surf.fill("black")

        self.stars  .draw()
        self.enemies.draw()
        self.bullets.draw()

        pygame.display.flip()

    def key_down(self, key):
        if key == pygame.K_ESCAPE:
            self.game.push_mode( Galaga_PauseMenu() )



class Galaga_PauseMenu(Galaga_ModeBase):
    def __init__(self, game):
        super(Galaga_PauseMenu,self).__init__(game)

    

Galaga().mainloop()
pygame.quit()

