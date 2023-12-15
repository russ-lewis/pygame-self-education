import numpy as np
import random



class Character:
    def __init__(self, pos):
        self.pos = np.array(pos, float)
        self.prevPos = np.array(pos, float)
        self.acceleration = np.array((0, 0), float)

        self.color = [random.randint(0, 100), random.randint(0, 255), random.randint(155, 255)]
        random.shuffle(self.color)
    
    def vel(self):
        return self.pos - self.prevPos
    
    def update(self, characters):
        vel = self.vel()
        vel = vel + self.acceleration

        vm = np.linalg.norm(vel)
        # if vm > 5:
        #     vel /= vm
        vel /= vm / 2

        self.prevPos = self.pos * 1
        self.pos += vel

        
        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[1] < 0:
            self.pos[1] = 0
        if self.pos[0] > 1500:
            self.pos[0] = 1500
        if self.pos[1] > 750:
            self.pos[1] = 750


        self.acceleration *= 0

        for c in characters:
            if c == self:
                continue

            disp = c.pos - self.pos
            dist = np.linalg.norm(disp)
            # dx = disp / dist

            dv = c.vel() - self.vel()


            # separation
            # if dist < 50:
            self.acceleration -= disp * 10000 / dist ** 2

            # alignment
            self.acceleration += 4 * dv * 10000 / dist ** 2

            # cohesion
            self.acceleration += disp * 1

        # # boundaries
        # if self.pos[0] < 100:
        #     self.acceleration[0] += 1000
        # if self.pos[1] < 100:
        #     self.acceleration[1] += 1000
        # if self.pos[0] > 600:
        #     self.acceleration[0] -= 1000
        # if self.pos[1] > 600:
        #     self.acceleration[1] -= 1000

        if self.acceleration.any():
            self.acceleration /= np.linalg.norm(self.acceleration) / 0.1

    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, np.array(self.pos, int), 5)




characters = []


# c = Character((300, 300))
# c.pos -= 1
# characters.append(c)


for i in range(25):
    c = Character((random.random()*1500, random.random()*750))
    characters.append(c)

    speed = 1
    c.pos += (
        random.random() * speed * 2 - speed,
        random.random() * speed * 2 - speed
    )





import pygame

pygame.init()

SCREEN = pygame.display.set_mode((1500, 750))
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
            pass

    for c in characters:
        c.update(characters)
