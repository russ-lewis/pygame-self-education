import pygame

import random



pygame.font.init()



ms_font = pygame.font.SysFont("monospace", 36)

SCREEN_WID = 800
SCREEN_HEI = 600

CLOCK_HZ   = 50
CLOCK_TICK = 1 / CLOCK_HZ



FIGHTER_WID = 50    # TODO: figure out what this really should be
FIGHTER_HEI = 50    # TODO: figure out what this really should be



class Galaga_ModeBase:
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



class Galaga_Star(pygame.sprite.Sprite):
    def __init__(self):
        super(Galaga_Star,self).__init__()
        self.surf = pygame.Surface((2,2))
        self.surf.fill( [random.randint(0,32) for i in range(3)] )
        self.surf.set_colorkey((0,0,0), pygame.RLEACCEL)

        self.left   = random.randint( 5, SCREEN_WID-5)
        self.bottom = random.randint(10, SCREEN_HEI-3*FIGHTER_HEI)

    def update(self):
        self.top += STAR_SPEED
        if self.bottom >= SCREEN_HEI-3*FIGHTER_HEI:
            self.kill()



class Galaga_Script:
    # the "script" tells us how the aliens arrive on the board.  (It does not
    # describe how they fight once they reach formation.)  Each alien's path
    # can be described in 3 parts:
    #     1) A "swooping in," defined by a 4-point Bezier curve
    #     2) An optional single loop.  Radius and angular velocity is configurable
    #     3) A destination point; the alien flies there linearly.  Velocity is configurable
    #          - If the location is off the board, then the alien leaves and does not return
    #
    # Many aliens follow the same paths (except for their destinations), and so
    # we want to be able to share (1)+(2).  So a Script is defined as:
    #   - A list of aliens, each of which has:
    #       - An arrival time (in ticks)
    #       - A type
    #       - A final destination (can be off the board)
    #       - A pathID
    #   - A dictionary of paths, keyed by path IDs, each of which has:
    #       - Bezier points, first must be off the board, rest must be on
    #       - (A loop radius & angular velocity) or None

    def __init__(self, stage_num, game):
        my_script = scripts[stage_num]

        paths  = my_script["paths" ]
        aliens = my_script["aliens"]

        self.pending_aliens = []

        for a in aliens:
            delay   = a["delay"  ]
            path_ID = a["path_ID"]
            species = a["species"]
            station = a["station"]

            alien = Galaga_Alien(species, paths[path_ID], station)

            # scale the delay so that one step of delay is .25 second
            delay *= HZ/4

            self.pending_aliens.append( (delay,alien) )
        sorted(self.pending_aliens)



# ALIEN TYPES:
#
# There are three alien types: Bosses, Guards, and Grunts (https://galaga.com/en/history/galaga.php)
#
# The ones on top (which can capture the player) are "Bosses" (https://en.wikipedia.org/wiki/Galaga)
#
# I'm not sure which is which of the other two types.  Until I can find out
# more information, I'm going to call the red-winged, four-winged ones
# "butterflies" and the yellow-bodied, two-winged ones "bees."  I'll do a
# search-and-replace once I know the proper names.



scripts = [ None,
            {"paths" : [ {"ID": "high_L",
                          "bezier": [ (-1,-1),(0,2),(20,5),(20,1) ],
                          "loop"  : None    # {"center":(20,3), "rad":2, "spd":15}
                         },
                       ],
             "aliens": [ {"delay"  : 0,
                          "path_ID": "high_L",
                          "species": "butterfly",
                          "station": (2,1)
                         },
                         {"delay"  : 1,
                          "path_ID": "high_L",
                          "species": "butterfly",
                          "station": (2,2)
                         },
                         {"delay"  : 2,
                          "path_ID": "high_L",
                          "species": "butterfly",
                          "station": (1,3)
                         },
                         {"delay"  : 3,
                          "path_ID": "high_L",
                          "species": "butterfly",
                          "station": (2,3)
                         },
                       ]
            },
          ]



class Galaga_Alien:
    def __init__(self, species, path, station):
        self.path    = path
        self.station = station

        self.frames = []    # TODO

    def draw(self, surf):
        pass

