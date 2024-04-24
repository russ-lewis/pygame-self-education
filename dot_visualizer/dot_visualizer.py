#! /usr/bin/python3

import math

import pygame
pygame.init()



graph_line = input().split()
assert len(graph_line) == 4
assert     graph_line[0] == "graph"
assert     graph_line[1] == "1"

GRAPH_WID = float(graph_line[2])
GRAPH_HEI = float(graph_line[3])



graph_geom_mean  = math.sqrt(GRAPH_WID * GRAPH_HEI)
SCREEN_GEOM_MEAN = 500
SCREEN_SCALE     = SCREEN_GEOM_MEAN / graph_geom_mean

SCREEN_WID = SCREEN_GEOM_MEAN * GRAPH_WID
SCREEN_HEI = SCREEN_GEOM_MEAN * GRAPH_HEI

screen = pygame.display.set_mode( (SCREEN_WID,SCREEN_HEI) )



nodes = []
edges = []
while True:
    line = input().split()

    if line == ["stop"]:
        break

    if line[0] == "node":
        assert len(edges) == 0    # is this a true assertion?  I'm not at all sure
        nodes.append(line[1:])
    elif line[0] == "edge":
        edges.append(line[1:])
    else:
        assert False



screen.fill("white")



for n in nodes:
    name,x,y,wid,hei,label,style,shape,color,fillcolor = n

    x   = float( x ) * SCREEN_SCALE
    y   = float( y ) * SCREEN_SCALE
    wid = float(wid) * SCREEN_SCALE
    hei = float(hei) * SCREEN_SCALE

    # pygame has origin at top-left; dot is bottom-left
    y = SCREEN_HEI-y

    if color == "lightgrey":
        color = (128,128,128)

    rect = pygame.Rect( x - wid/2,
                        y - hei/2,
                        wid,hei )
    print(rect)
    pygame.draw.rect(screen, fillcolor, rect)
    pygame.draw.rect(screen,     color, rect, width=3)



for e in edges:
    tail = e[0]
    head = e[1]
    n    = int(e[2])
    coords_raw = e[3:3+2*n]
    last   = e[3+2*n:]
    assert len(last) in [2,4]
    style = e[-2]
    color = e[-1]

    coords = []
    for i in range(n):
        x = float(coords_raw[i*2  ]) * SCREEN_SCALE
        y = float(coords_raw[i*2+1]) * SCREEN_SCALE

        # pygame has origin at top-left; dot is bottom-left
        y = SCREEN_HEI-y

        coords.append( (x,y) )

    print(coords)
    pygame.draw.lines(screen, color, False, coords)



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
    pygame.display.flip()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and (e.key == pygame.K_ESCAPE or e.unicode == 'q'):
            running = False

    clock.tick(30)

pygame.quit()

