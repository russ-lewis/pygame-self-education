#! /usr/bin/python3

import random

import pygame
pygame.init()



SCREEN_WID = 800
SCREEN_HEI = 600
screen = pygame.display.set_mode( (SCREEN_WID,SCREEN_HEI) )



PT_SZ = 20
class Point(pygame.sprite.Sprite):
    def __init__(self):
        super(Point,self).__init__()
        self.image = pygame.Surface( (PT_SZ,PT_SZ) )

        # fill the point with a random color
        rgb = [random.randint(64,255) for i in range(3)]
        self.image.fill(rgb)

        # move the point to a random location
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(10, SCREEN_WID-10-PT_SZ)
        self.rect.top  = random.randint(10, SCREEN_HEI-10-PT_SZ)
        


pts = []
pts_group = pygame.sprite.Group()
for i in range(10):
    p = Point()
    pts   .append(p)
    pts_group.add(p)

cur_pt = None



# https://courses.engr.illinois.edu/cs418/sp2009/notes/12-MoreSplines.pdf
BEZIER_MATRIX = [[ 1, 0, 0, 0],
                 [-3, 3, 0, 0],
                 [ 3,-6, 3, 0],
                 [-1, 3,-3, 1]]
B_SPLINE_MATRIX = [[ 1/6, 4/6, 1/6, 0  ],
                   [-3/6, 0  , 3/6, 0  ],
                   [ 3/6,-6/6, 3/6, 0  ],
                   [-1/6, 3/6,-3/6, 1/6]]

def apply_matrix(pts, matrix):
    assert len(pts) == 4

    x_coeffs = [pts[0][0]*matrix[0][0] +    # top row of martix, times the x coords of the points
                pts[1][0]*matrix[0][1] +
                pts[2][0]*matrix[0][2] +
                pts[3][0]*matrix[0][3],

                pts[0][0]*matrix[1][0] +
                pts[1][0]*matrix[1][1] +
                pts[2][0]*matrix[1][2] +
                pts[3][0]*matrix[1][3],

                pts[0][0]*matrix[2][0] +
                pts[1][0]*matrix[2][1] +
                pts[2][0]*matrix[2][2] +
                pts[3][0]*matrix[2][3],

                pts[0][0]*matrix[3][0] +
                pts[1][0]*matrix[3][1] +
                pts[2][0]*matrix[3][2] +
                pts[3][0]*matrix[3][3] ]

    y_coeffs = [pts[0][1]*matrix[0][0] +    # top row of martix, times the y coords of the points
                pts[1][1]*matrix[0][1] +
                pts[2][1]*matrix[0][2] +
                pts[3][1]*matrix[0][3],

                pts[0][1]*matrix[1][0] +
                pts[1][1]*matrix[1][1] +
                pts[2][1]*matrix[1][2] +
                pts[3][1]*matrix[1][3],

                pts[0][1]*matrix[2][0] +
                pts[1][1]*matrix[2][1] +
                pts[2][1]*matrix[2][2] +
                pts[3][1]*matrix[2][3],

                pts[0][1]*matrix[3][0] +
                pts[1][1]*matrix[3][1] +
                pts[2][1]*matrix[3][2] +
                pts[3][1]*matrix[3][3] ]

    # return a callable, which evaluates the polynomial for both (x,y)
    def evaluate(t):
        return ( x_coeffs[0] +       \
                 x_coeffs[1]*t +     \
                 x_coeffs[2]*t*t +   \
                 x_coeffs[3]*t*t*t,
                 y_coeffs[0] +       \
                 y_coeffs[1]*t +     \
                 y_coeffs[2]*t*t +   \
                 y_coeffs[3]*t*t*t )

    return evaluate



class Bezier:
    def group_pts(self, pts):
        for i in range(0,len(pts),3):
            these_pts = pts[i:i+4]
            if len(these_pts) < 4:
                return
            yield these_pts
    def get_matrix(self):
        return BEZIER_MATRIX

class B_Spline:
    def group_pts(self, pts):
        for i in range(0,len(pts)-3):
            these_pts = pts[i:i+4]
            assert len(these_pts) == 4
            yield these_pts
    def get_matrix(self):
        return B_SPLINE_MATRIX

cur_mode = Bezier()
alt_mode = B_Spline()



clock = pygame.time.Clock()

running = True
while running:
    screen.fill("black")

    # draw the polygon
    prev_pt = None
    for this_pt in pts:
        if prev_pt is not None:
            pygame.draw.line(screen, "green",
                             prev_pt.rect.center, this_pt.rect.center,
                             width=PT_SZ//10)
        prev_pt = this_pt

    # draw a highlight around the current point, if any
    if cur_pt is not None:
        pygame.draw.circle(screen, "red", cur_pt.rect.center, PT_SZ, width=PT_SZ//5)

    # draw the points themselves
    pts_group.draw(screen)

    # generate the Bezier polynomials for (x,y), reflected as a function that
    # saves the generated coefficients
    for selected_pts in cur_mode.group_pts([pt.rect for pt in pts]):
        func = apply_matrix(selected_pts, cur_mode.get_matrix())

        # now, evaluate it and draw the points.
        STEPS = 32
        for i in range(STEPS+1):
            t = i/STEPS
            curve_pt = func(t)
            pygame.draw.circle(screen, "blue", curve_pt, 5)

    pygame.display.flip()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and (e.key == pygame.K_ESCAPE or e.unicode == 'q'):
            running = False

        if e.type == pygame.KEYDOWN and e.unicode == 'm':
            cur_mode,alt_mode = alt_mode,cur_mode

        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            assert cur_pt is None

            mouse_pos = pygame.mouse.get_pos()
            for pt in pts:
                if pt.rect.collidepoint(mouse_pos):
                    cur_pt = pt
                    break

        if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            cur_pt = None

        if e.type == pygame.MOUSEMOTION and cur_pt is not None:
            cur_pt.rect.center = pygame.mouse.get_pos()

    clock.tick(30)

pygame.quit()

