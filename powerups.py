from circleshape import *
from player import *
import random

class Powerup(CircleShape):
    def __init__(self):
        super().__init__(random.uniform(100,SCREEN_WIDTH-100),random.uniform(100,SCREEN_HEIGHT-100),POWERUP_RADIUS)
        self.type = random.randint(0,1)

    def draw(self, screen):
        if self.type:
            pygame.draw.circle(screen,(0,255,0),self.position,self.radius)
        else:
            pygame.draw.circle(screen,(100,100,255),self.position,self.radius)