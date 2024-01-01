#! /usr/bin/python3

import numpy as np
np.set_printoptions(linewidth=1000)



points = [
    (0, 0),
    (1, 1),
    (2, 0),
    (3, 1),
    (4, 0),

    # (2, 1),
]
connections = [
    (0, 1),
    (0, 2),
    (1, 2),
    (1, 3),
    (2, 3),
    (2, 4),
    (3, 4),

    # (2, 5),
]
fixed_points = [
    0,
    4
]
forces_at_points = [
    (2, (0, -10))
]




def get_system_matrix(points, connections, fixed_points, forces_at_points):
    rows = len(points) * 2
    columns = len(connections)

    v_external_forces = np.zeros(rows)
    m_system = np.zeros((rows, columns))

    # todo external forces
        # todo forces at points
        # todo fixed point reaction forces
    
    # todo connections into matrix
    for i, c in enumerate(connections):
        a, b = c
        displacement = np.subtract(points[b], points[a])
        assert len(displacement) == 2
        magnitude = np.linalg.norm(displacement)
        assert magnitude > 0
        direction = displacement / magnitude

        m_system[a*2][i] = direction[0]
        m_system[a*2+1][i] = direction[1]
        
        m_system[b*2][i] = -direction[0]
        m_system[b*2+1][i] = -direction[1]

    # m_system[2][3] = 1


    print(v_external_forces)
    print()
    print(m_system)

def get_system_inverse_matrix():
    return np.linalg.inv(get_system_matrix())


get_system_matrix(points, connections, fixed_points, forces_at_points)
input()



view_zoom = 0.75
# view_offset = np.array((0, 0), dtype=float)


def get_points_rect(points):
    point_min = (0, 0)
    point_max = (1, 1)

    if len(points) > 1:
        point_min = points[1]
    if len(points) > 0:
        point_max = points[0]

    for p in points:
        point_min = np.minimum(point_min, p)
        point_max = np.maximum(point_max, p)

    size = point_max - point_min
    # # size = space / view_zoom
    # size = space

    # margin = (size - space) / 2
    # corner = point_min

    # corner -= view_offset * view_zoom

    return tuple(point_min) + tuple(size)

def get_view_rect(points_rect, zoom):
    assert zoom > 0

    point_min = points_rect[:2]
    size = points_rect[2:]

    view_size = np.divide(size, zoom)

    margin = (view_size - size) / 2
    corner = point_min - margin

    # corner -= view_offset * view_zoom

    return tuple(corner) + tuple(view_size)


# def scale_to_view_rect(output_rect, view_rect, scalar):


def transform_to_view_rect(output_rect, view_rect, p, invert_y=True):
    v = np.array(p, dtype=float)

    if invert_y:
        v[1] = view_rect[1] * 2 + view_rect[3] - v[1] 

    v -= view_rect[:2]# + output_rect[:2]
    v = np.matmul((
        (output_rect[2] / view_rect[2], 0),
        (0, output_rect[3] / view_rect[3])
    ),
        v
    )
    v += output_rect[:2]

    return v

def draw(surface):
    screen_rect = SCREEN.get_rect()


    points_rect = get_points_rect(points)
    max_force_length = min(points_rect[2:]) / 10

    view_rect = get_view_rect(points_rect, view_zoom)

    max_force = 0
    for i, f in forces_at_points:
        max_force = max(max_force, np.linalg.norm(f))

    force_scale = max_force_length / max_force
    # print(max_force_length)
    # force_scale = 0.01
    # print(force_scale)

    # force_ends = []
    # for i, f in forces_at_points:




    surface.fill("black")

    for i, p in enumerate(points):
        if i in fixed_points:
            c = "green"
        else:
            c = "white"
        pygame.draw.circle(surface, c, transform_to_view_rect(screen_rect, view_rect, p), 5)
    
    for c in connections:
        pygame.draw.aaline(surface, "white",
            transform_to_view_rect(screen_rect, view_rect, points[c[0]]),
            transform_to_view_rect(screen_rect, view_rect, points[c[1]])
        )
    
    for i, f in forces_at_points:
        start = points[i]
        end = np.multiply(f, force_scale) + start
        pygame.draw.aaline(surface, "green",
            transform_to_view_rect(screen_rect, view_rect, start),
            transform_to_view_rect(screen_rect, view_rect, end)
        )

    pygame.display.flip()

def user_input():
    global view_zoom, view_offset

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        elif event.type == pygame.KEYDOWN:
            pass

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pass
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pass
            
        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[1]:
                rel = np.array(event.rel)
                rel[1] *= -1
                view_offset += rel / 100
            
        elif event.type == pygame.MOUSEWHEEL:
            # print(event.y)
            view_zoom *= 1.1 ** event.y

def update():
    pass


import pygame

pygame.init()

SCREEN = pygame.display.set_mode((700, 700), pygame.RESIZABLE)
pygame.display.set_caption(__name__)
clock = pygame.time.Clock()

while pygame.get_init():
    clock.tick(60)

    draw(SCREEN)

    user_input()

    update()

# if __name__ == "__main__":
#     main()
