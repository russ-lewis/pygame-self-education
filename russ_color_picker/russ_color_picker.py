#! /usr/bin/python3

import pygame



BORDER = 3
SLIDER_SPACING = 20
SLIDER_HEIGHT  = 20
MAIN_SPACING   = 40



SCREEN_WID = 50+256+MAIN_SPACING+256+50
SCREEN_HEI = 50+256+SLIDER_SPACING+SLIDER_HEIGHT+MAIN_SPACING+256+SLIDER_SPACING+SLIDER_HEIGHT+50
screen = pygame.display.set_mode( (SCREEN_WID,SCREEN_HEI) )



color = (0,0,0)



clock = pygame.time.Clock()

running = True
button_down = False
while running:
    screen.fill("black")


    def draw_picker(lft,top, sq_color, slider_color):
        pygame.draw.rect(screen, "white",
                                 pygame.Rect((lft-BORDER,top-BORDER),
                                             (256+2*BORDER,256+2*BORDER)),
                                 width=BORDER)
        pygame.draw.rect(screen, "white",
                                  pygame.Rect((lft-BORDER,top+256+SLIDER_SPACING-BORDER),
                                              (256+2*BORDER, SLIDER_HEIGHT+2*BORDER)),
                                  width=BORDER)

        for x in range(0,256):
            for y in range(0,256):
                screen.set_at((lft+x,top+y), sq_color(x,y))
            pygame.draw.line(screen, slider_color(x),
                                     (lft+x,top+256+SLIDER_SPACING),
                                     (lft+x,top+256+SLIDER_SPACING+SLIDER_HEIGHT-1))

    # the top-left picker is R.  This means that the square has gradients of
    # G,B, and the slider on the bottom has a gradient of R.
    draw_picker(50,50,
                lambda g,b: (color[0],g,b), lambda r: (r,0,0))

    # top-right is G
    draw_picker(50+256+MAIN_SPACING, 50,
                lambda r,b: (r,color[1],b), lambda g: (0,g,0))

    # bottom-left is B
    draw_picker(50, 50+256+SLIDER_SPACING+SLIDER_HEIGHT+MAIN_SPACING,
                lambda r,g: (r,g,color[2]), lambda b: (0,0,b))

    # the color display is on the bottom-right
    pygame.draw.rect(screen, "white",
                             pygame.Rect((50+256+MAIN_SPACING-BORDER, 50+256+SLIDER_SPACING+SLIDER_HEIGHT+MAIN_SPACING-BORDER),
                                         (256+2*BORDER,256+2*BORDER)),
                             width=BORDER)
    pygame.draw.rect(screen, color,
                             pygame.Rect((50+256+MAIN_SPACING, 50+256+SLIDER_SPACING+SLIDER_HEIGHT+MAIN_SPACING),
                                         (256,256)))

    pygame.display.flip()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and (e.key == pygame.K_ESCAPE or e.unicode == 'q'):
            running = False

        if e.type == pygame.KEYDOWN and e.unicode == 'm':
            cur_mode,alt_mode = alt_mode,cur_mode

        def try_set_color():
            pos = pygame.mouse.get_pos()

            def maybe_sq(lft,top, dim1,dim2):
                x = pos[0]-lft
                y = pos[1]-top

                if x < 0 or x >= 256 or y < 0 or y >= 256:
                    return False

                global color
                lst_color = list(color)
                lst_color[dim1] = x
                lst_color[dim2] = y
                color = tuple(lst_color)
                return True

            def maybe_slider(lft,top, dim):
                x = pos[0]-lft
                y = pos[1]-top

                if x < 0 or x >= 256 or y < 0 or y >= SLIDER_HEIGHT:
                    return False

                global color
                lst_color = list(color)
                lst_color[dim] = x
                color = tuple(lst_color)
                return True


            maybe_sq(50                 , 50, 1,2) or \
            maybe_sq(50+256+MAIN_SPACING, 50, 0,2) or \
            maybe_sq(50                 , 50+256+SLIDER_SPACING+SLIDER_HEIGHT+MAIN_SPACING, 0,1) or \
            maybe_slider(50                 , 50+256+SLIDER_SPACING, 0) or \
            maybe_slider(50+256+MAIN_SPACING, 50+256+SLIDER_SPACING, 1) or \
            maybe_slider(50                 , 50+256+SLIDER_SPACING+SLIDER_HEIGHT+MAIN_SPACING+256+SLIDER_SPACING, 2) 

        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            try_set_color()
            button_down = True
        if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            button_down = False
        if e.type == pygame.MOUSEMOTION and button_down:
            try_set_color()


    clock.tick(30)

pygame.quit()

