from circleshape import *

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x,y,SHOT_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen,(0,0,0),self.position,self.radius)
        pygame.draw.circle(screen,(255,255,255),self.position,self.radius,2)

    def update(self, dt):
        self.position += self.velocity * dt
        if self.position[0] + ASTEROID_MAX_RADIUS < 0:
            self.position[0] += SCREEN_WIDTH + 2*ASTEROID_MAX_RADIUS
        if self.position[0] - ASTEROID_MAX_RADIUS > SCREEN_WIDTH:
            self.position[0] -= SCREEN_WIDTH + 2*ASTEROID_MAX_RADIUS
        if self.position[1] + ASTEROID_MAX_RADIUS < 0:
            self.position[1] += SCREEN_HEIGHT + 2*ASTEROID_MAX_RADIUS
        if self.position[1] - ASTEROID_MAX_RADIUS > SCREEN_HEIGHT:
            self.position[1] -= SCREEN_HEIGHT + 2*ASTEROID_MAX_RADIUS