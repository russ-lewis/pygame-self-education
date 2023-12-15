import numpy as np
import random
# from numpy.linalg import norm as magnitude


def rotateVector(vector, theta):
    s = np.sin(theta)
    c = np.cos(theta)

    matrix = np.array((
        (c, -s),
        (s, c)
    ))

    return np.dot(matrix, vector)


class Character:
    def __init__(self):
        self.pos = np.array((0, 0), float)
        self.velocity = np.array((0, 0), float)
        self.AI = None
        self.force = None

        self.color = "pink"
    
    def updateAI(self, characters):
        if self.AI:
            self.velocity = self.AI(self, characters)
    
    def updateGame(self, characters):
        self.pos += self.velocity
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, np.array(self.pos, int), 10)

player_speed = 2
def playerAI(self, characters):
    while True:
        try:
            keys = pygame.key.get_pressed()
            break
        except pygame.error:
            pass

    # self.velocity *= 0

    vel = np.array((0, 0), float)

    vel[1] -= keys[pygame.K_w]
    vel[0] -= keys[pygame.K_a]
    vel[1] += keys[pygame.K_s]
    vel[0] += keys[pygame.K_d]

    mag = np.linalg.norm(vel) / player_speed
    if mag:
        vel /= mag
    return vel


characters = []



player = Character()
characters.append(player)

player.AI = playerAI
player.force = "player"
player.color = "blue"
player.pos += (400, 400)



enemySpeed = 2
def enemyAI(self, characters):
    vel = np.array((0, 0), float)

    # dist = np.inf
    # target = None
    for c in characters:
        if c == self:
            continue

        disp = c.pos - self.pos
        dist = np.linalg.norm(disp)
        dx = disp / dist


        # pursuit
        if c.force != self.force:
            if dist > 200:
                vel += dx
            elif dist < 150:
                vel -= dx

        # collision avoidance and turning
        collisionMax = 50
        collisionMin = 30
        if dist < collisionMin:
            vel -= 1000 * dx
        # if dist < collisionMax:
        #     vel += 0.1 * rotateVector(dx, np.pi/2)
        #     pass

        # spread out
        vel -= 0.01 * dx
    


    # directions = np.array(range(32), int)
    

    # dx = (target.pos - self.pos) / dist
    
    # self.velocity *= 0
    
    # self.velocity += dx
    
    # if dist < 100:
    #     self.velocity -= dx
    #     self.velocity += rotateVector(dx, np.pi/2)

    # self.velocity *= enemySpeed

    mag = np.linalg.norm(vel) / enemySpeed
    if mag:
        vel /= mag
    return vel


for i in range(5):
    characters.append(Character())
    enemy = characters[-1]

    enemy.AI = enemyAI
    enemy.force = "enemy"
    enemy.color = "red"
    enemy.pos += (500, 200)
    enemy.pos += (random.random()*300, random.random()*500)





import pygame

pygame.init()

SCREEN = pygame.display.set_mode((1000, 750))
pygame.display.set_caption(__name__)
CLOCK = pygame.time.Clock()


while pygame.get_init():
    CLOCK.tick(60)


    SCREEN.fill("black")

    for c in characters:
        c.draw(SCREEN)

    pygame.display.flip()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        elif event.type == pygame.KEYDOWN:
            # match event.key:
            #     case pygame.K_w:
            #         player.velocity[1] -= 1
            #     case pygame.K_a:
            #         player.velocity[0] -= 1
            #     case pygame.K_s:
            #         player.velocity[1] += 1
            #     case pygame.K_d:
            #         player.velocity[0] += 1

            # if event.key == pygame.K_r:
            #     reload()
            
            # elif event.key == pygame.K_SPACE:
            #     controller.next()
            pass
    
    # while True:
    #     try:
    #         keys = pygame.key.get_pressed()
    #         break
    #     except pygame.error:
    #         pass

    # player.velocity *= 0

    # player.velocity[1] -= keys[pygame.K_w]
    # player.velocity[0] -= keys[pygame.K_a]
    # player.velocity[1] += keys[pygame.K_s]
    # player.velocity[0] += keys[pygame.K_d]

    # mag = np.linalg.norm(player.velocity) / player_speed
    # if mag:
    #     player.velocity /= mag
    

    for c in characters:
        c.updateAI(characters)

    for c in characters:
        c.updateGame(characters)