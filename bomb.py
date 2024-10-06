from circleshape import *

class Bomb(CircleShape):
    def __init__(self, x, y):
        super().__init__(x,y,BOMB_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen,(0,0,0),self.position,self.radius)
        pygame.draw.circle(screen,(255,255,255),self.position,self.radius,2)