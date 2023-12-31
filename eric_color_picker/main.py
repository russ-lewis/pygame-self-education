import numpy as np
import pygame

pygame.init()

SCREEN = pygame.display.set_mode((1200, 750))
pygame.display.set_caption(__name__)
CLOCK = pygame.time.Clock()


# r = 50
# g = 200
# b = 100




# np.matmul :)

def rotation_matrix(theta):
    c = np.cos(theta)
    s = np.sin(theta)
    matrix = (
        (c, -s),
        (s, c)
    )
    return np.array(matrix)

def rotate_vector(v, theta):
    return np.matmul(rotation_matrix(theta), v)

# print(rotate_vector((2, 3), np.pi/2))
# print()


# m = (
#     (2, 0),
#     (0, 1)
# )
# print(np.matmul(m, (2, 3)))
# print(m[0])
# print(m[1])








# held_character = None


angle = np.pi*2/3

rotate_120_deg = rotation_matrix(angle)

# rv = np.array((1, 0))
# gv = rotate_vector(rv, angle)
# bv = rotate_vector(gv, angle)

m_rg_to_xy = np.array((
    (1, np.cos(np.pi*2/3)),
    (0, np.sin(np.pi*2/3))
)) / 255
m_gb_to_xy = np.matmul(rotate_120_deg, m_rg_to_xy)
m_br_to_xy = np.matmul(rotate_120_deg, m_gb_to_xy)

m_xy_to_rg = np.linalg.inv(m_rg_to_xy)
m_xy_to_gb = np.linalg.inv(m_gb_to_xy)
m_xy_to_br = np.linalg.inv(m_br_to_xy)

def rg_to_xy(r, g):
    # m = np.array((
    #     (1, np.cos(np.pi*2/3)),
    #     (0, np.sin(np.pi*2/3))
    # )) / 255
    # return np.matmul(m, (r, g))
    return np.matmul(m_rg_to_xy, (r, g))

def gb_to_xy(g, b):
    # return np.matmul(rotate_120_deg, rg_to_xy(g, b))
    return np.matmul(m_gb_to_xy, (g, b))

def br_to_xy(b, r):
    # return np.matmul(rotate_120_deg, gb_to_xy(b, r))
    return np.matmul(m_br_to_xy, (b, r))



# wonder_hexagon = pygame.Surface()






center = 375, 375
scale = 250
screen_transform_matrix = (
    (scale, 0),
    (0, -scale)
)
# print(screen_transform_matrix)
screen_transform_matrix_inv = np.linalg.inv(screen_transform_matrix)

def screen_transform(v):
    return np.array(np.matmul(screen_transform_matrix, v) + center, dtype=int)

def screen_untransform(v):
    return np.matmul(screen_transform_matrix_inv, np.array(v) - center)


# def draw_line(v, color, start=(0, 0)):
#     start = np.array(start, dtype=int)
#     end = start + v
#     pygame.draw.line(SCREEN, color, screen_transform(start), screen_transform(end))


# def draw_face(id, step, pinned_color):
#     assert id in (0, 1, 2)
#     if id == 0:
#         fp = rg_to_xy
#         fr = lambda a, b: a
#         fg = lambda a, b: b
#         fb = lambda a, b: 0
#     elif id == 1:
#         fp = gb_to_xy
#         fr = lambda a, b: 0
#         fg = lambda a, b: a
#         fb = lambda a, b: b
#     elif id == 2:
#         fp = br_to_xy
#         fr = lambda a, b: b
#         fg = lambda a, b: 0
#         fb = lambda a, b: a

#     for a in range(0, 255, step):
#         for b in range(0, 255, step):
#             SCREEN.set_at(screen_transform(fp(a, b)), (fr(a, b), fg(a, b), fb(a, b)))



cube_render_step_size = 15
cube_render_step_offset = 0
cube_viewport = pygame.Surface((scale * 2, scale * 2))
def update_cube_viewport(
    pinned_color = (0, 0, 0), background_color=(100, 100, 100), force_pinned_color=True
):
    global cube_render_step_offset

    i_offset = cube_render_step_offset % cube_render_step_size
    j_offset = cube_render_step_offset // cube_render_step_size

    cube_render_step_offset += 1
    cube_render_step_offset %= cube_render_step_size * cube_render_step_size

    min_x, min_y = 0, 0
    max_x = min_x + scale * 2
    max_y = min_y + scale * 2

    for i in range(min_x + i_offset, max_x, cube_render_step_size):
        for j in range(min_y + j_offset, max_y, cube_render_step_size):
            ij = i, j
            xy = np.matmul(screen_transform_matrix_inv, np.array(ij) - (scale, scale))
            # input(xy)

            rg = np.array(np.matmul(m_xy_to_rg, xy), dtype=int)
            gb = np.array(np.matmul(m_xy_to_gb, xy), dtype=int)
            br = np.array(np.matmul(m_xy_to_br, xy), dtype=int)

            r = -1
            g = -1
            b = -1
            
            if rg[0] >= 0 and rg[1] >= 0 and rg[0] < 256 and rg[1] < 256:
                r, g = rg
                b = pinned_color[2]
            if gb[0] >= 0 and gb[1] >= 0 and gb[0] < 256 and gb[1] < 256:
                g, b = gb
                r = pinned_color[0]
            if br[0] >= 0 and br[1] >= 0 and br[0] < 256 and br[1] < 256:
                b, r = br
                g = pinned_color[1]
            
            if r + g + b == -3:
                # continue
                r, g, b = background_color
            else:
                if force_pinned_color:
                    if pinned_color[0]:
                        r = pinned_color[0]
                    if pinned_color[1]:
                        g = pinned_color[1]
                    if pinned_color[2]:
                        b = pinned_color[2]
                
            cube_viewport.set_at(ij, (r, g, b))


def draw_selected_color_lines(color, force_color=None):
    r, g, b = color

    if not r:
        if force_color:
            c1 = force_color
            c2 = force_color
        else:
            c1 = "blue"
            c2 = "green"
        pygame.draw.line(SCREEN, c1,
            screen_transform(gb_to_xy(g, 0)), screen_transform(gb_to_xy(g, 255))
        )
        pygame.draw.line(SCREEN, c2,
            screen_transform(gb_to_xy(0, b)), screen_transform(gb_to_xy(255, b))
        )

    if not g:
        if force_color:
            c1 = force_color
            c2 = force_color
        else:
            c1 = "red"
            c2 = "blue"
        pygame.draw.line(SCREEN, c1,
            screen_transform(br_to_xy(b, 0)), screen_transform(br_to_xy(b, 255))
        )
        pygame.draw.line(SCREEN, c2,
            screen_transform(br_to_xy(0, r)), screen_transform(br_to_xy(255, r))
        )

    if not b:
        if force_color:
            c1 = force_color
            c2 = force_color
        else:
            c1 = "green"
            c2 = "red"
        pygame.draw.line(SCREEN, c1,
            screen_transform(rg_to_xy(r, 0)), screen_transform(rg_to_xy(r, 255))
        )
        pygame.draw.line(SCREEN, c2,
            screen_transform(rg_to_xy(0, g)), screen_transform(rg_to_xy(255, g))
        )



hovered_color = (0, 0, 0)
pinned_color = (0, 0, 0)
force_color = False

while pygame.get_init():
    CLOCK.tick(60)


    SCREEN.fill("black")


    fps = CLOCK.get_fps()
    font = pygame.font.Font("freesansbold.ttf", 20)
    text = font.render(f"FPS: {int(fps)}", True, "white", "black")
    text_rect = text.get_rect()
    text_rect.topleft = (5, 5)
    SCREEN.blit(text, text_rect)



    # pygame.draw.rect(SCREEN, (r, g, b), (100, 100, 100, 100))
    # for x in range(radius):
    #     for y in range(radius):
    #         SCREEN.set_at((x + center[0], y + center[1]), (x, y, 0))

    # m = rotation_matrix(angle)
    # angle += 0.01

    # pygame.draw.circle(SCREEN, "white", screen_transform((0, 0)), 2)

    # pygame.draw.circle(SCREEN, (r, g, b), screen_transform(rg_to_xy(r, g)), 3)


    # pinned_color = 0, 0, 255

    update_cube_viewport(pinned_color, force_pinned_color=force_color)
    cube_blit_area = pygame.Rect((center[0] - scale, center[1] - scale, scale * 2, scale * 2))
    SCREEN.blit(cube_viewport, cube_blit_area)


    # pos = pygame.mouse.get_pos()
    # upos = screen_untransform(pos)

    # rg = np.matmul(m_xy_to_rg, upos)
    # gb = np.matmul(m_xy_to_gb, upos)
    # br = np.matmul(m_xy_to_br, upos)

    # rg = np.array(rg, dtype=int)
    # gb = np.array(gb, dtype=int)
    # br = np.array(br, dtype=int)

    # if rg[0] >= 0 and rg[1] >= 0 and rg[0] < 256 and rg[1] < 256:
    #     hovered_color = (rg[0], rg[1], 0)
    # if gb[0] >= 0 and gb[1] >= 0 and gb[0] < 256 and gb[1] < 256:
    #     hovered_color = (0, gb[0], gb[1])
    # if br[0] >= 0 and br[1] >= 0 and br[0] < 256 and br[1] < 256:
    #     hovered_color = (br[1], 0, br[0])
    
    # # font = pygame.font.Font("freesansbold.ttf", 20)
    # # text = font.render(str(hovered_color), True, "white", "black")
    # # text_rect = text.get_rect()
    # # text_rect.topleft = (5, 55)
    # # SCREEN.blit(text, text_rect)

    mouse_pos = pygame.mouse.get_pos()
    if cube_blit_area.contains((mouse_pos, (0, 0))):
        hovered_color = SCREEN.get_at(mouse_pos)[:3]
    # input(hovered_color)


    pygame.draw.circle(SCREEN, hovered_color, (800, 300), 50)
    pygame.draw.circle(SCREEN, "white", (800, 300), 50, 1)
    
    font = pygame.font.Font("freesansbold.ttf", 20)
    text = font.render("hovered", True, "white", "black")
    text_rect = text.get_rect()
    text_rect.center = (800, 375)
    SCREEN.blit(text, text_rect)


    pygame.draw.circle(SCREEN, pinned_color, (1000, 300), 50)
    pygame.draw.circle(SCREEN, "white", (1000, 300), 50, 1)
    
    font = pygame.font.Font("freesansbold.ttf", 20)
    text = font.render("pinned", True, "white", "black")
    text_rect = text.get_rect()
    text_rect.center = (1000, 375)
    SCREEN.blit(text, text_rect)



    

    if sum(hovered_color) > 0:
        draw_selected_color_lines(pinned_color, "white")
        draw_selected_color_lines(hovered_color)
            
    pygame.draw.line(SCREEN, "red",
        screen_transform(rg_to_xy(0, 0)), screen_transform(rg_to_xy(255, 0))
    )
    pygame.draw.line(SCREEN, "green",
        screen_transform(gb_to_xy(0, 0)), screen_transform(gb_to_xy(255, 0))
    )
    pygame.draw.line(SCREEN, "blue",
        screen_transform(br_to_xy(0, 0)), screen_transform(br_to_xy(255, 0))
    )

    pygame.draw.rect(
        SCREEN, "white",(center[0] - scale, center[1] - scale, scale * 2, scale * 2), 1
    )
    





    pygame.display.flip()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        elif event.type == pygame.KEYDOWN:
            pass

        # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        #     if pinned_color == (0, 0, 0):
        #         pinned_color = hovered_color
        #     else:
        #         pinned_color = (0, 0, 0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pinned_color = hovered_color
            elif event.button == 3:
                pinned_color = (0, 0, 0)
            else:
                force_color = not force_color

            # held_character = None
        
        # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # held_character = Character(pygame.mouse.get_pos())
            # characters.append(held_character)

    # if held_character:
    #     held_character.pos *= 0
    #     held_character.pos += pygame.mouse.get_pos()


    # for c in characters:
    #     c.update(characters)
