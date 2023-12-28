#! /usr/bin/python3

import asyncio

import pygame
import random



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
        TODO critical do not change the mode immediately, or pending events being dispatched by the for loop in the mode's dispatch_events() might get lost!

        TODO maybe push_mode() should be a method of the Mode class???

        assert self.new_mode = new_mode
        self.new_mode = new_mode



class AsyncPygame_Mode:
    def __init__(self, game):
        self.game     = game
        self.has_quit = False

    def dispatch_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                self.key_down(event.key)
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_motion(event.pos[0], event.pos[1])

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_button_down_left()
            elif event.type == pygame.MOUSEBUTTONUP   and event.button == 1:
                self.mouse_button_up_left()

            elif event.type in [pygame.WINDOWSHOWN,
                                pygame.WINDOWEXPOSED,
                                pygame.WINDOWFOCUSGAINED, pygame.WINDOWFOCUSLOST,
                                pygame.WINDOWTAKEFOCUS,
                                pygame.WINDOWENTER, pygame.WINDOWLEAVE,
                                pygame.WINDOWMOVED,
                                pygame.VIDEOEXPOSE,
                                pygame.ACTIVEEVENT]:
                pass    # TODO: add handlers

            else:
                print(event)

    def quit(self):
        self.has_quit = True

    def update(self):
        pass

    def key_down(self, key):
        pass

    def mouse_motion(self, x,y):
        pass

    def mouse_button_down_left(self):
        pass

    def mouse_button_up_left(self):
        pass



pygame.font.init()

ms_font = pygame.font.SysFont("monospace", 36)



SCREEN_WID = 800
SCREEN_HEI = 600

CLOCK_HZ   = 50
CLOCK_TICK = 1 / CLOCK_HZ

class Galaga(AsyncPygame):
    def __init__(self):
        super(Galaga,self).__init__(SCREEN_WID,SCREEN_HEI, CLOCK_TICK)
        self.cur_mode = Galaga_LoadingScreen(self)



class Galaga_LoadingScreen(AsyncPygame_Mode):
    def __init__(self, game):
        super(Galaga_LoadingScreen,self).__init__(game)
        self.msg = ms_font.render("Click mouse to start game", False, "white")


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

    def key_down(self, key):
        if key == pygame.K_ESCAPE:
            self.quit()

    def mouse_button_down_left(self):
        self.mode_complete.set_result( Galaga_LoadStage(self.game, 1) )



class Galaga_LoadStage(AsyncPygame_Mode):
    def __init__(self, game,stage_num):
        super(Galaga_LoadStage,self).__init__(game)
        self.stage_num = stage_num
        self.msg       = ms_font.render("Stage 1 - Ready!", False, "white")

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

class Galaga_Stage(AsyncPygame_Mode):
    def __init__(self, game,stage_num):
        super(Galaga_Stage,self).__init__(game)
        self.stage_num = stage_num

    async def main(self):
        await asyncio.sleep(2)
        print("TODO")
        return None

    def draw(self, surf):
        surf.fill("green")
        pygame.display.flip()

    def key_down(self, key):
        if key == pygame.K_ESCAPE:
            self.game.push_mode( Galaga_PauseMenu() )



class Galaga_PauseMenu(AsyncPygame_Mode):
    def __init__(self, game):
        super(Galaga_PauseMenu,self).__init__(game)

    

Galaga().mainloop()
pygame.quit()

