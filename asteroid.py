from circleshape import *
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x,y,radius)

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
    
    def split(self):
        self.kill()
        if self.radius < ASTEROID_MIN_RADIUS+10:
            return
        angle = random.uniform(20,50)
        asteroid1 = Asteroid(*self.position, self.radius - ASTEROID_MIN_RADIUS)
        asteroid1.velocity = self.velocity.rotate(angle)*1.2
        asteroid2 = Asteroid(*self.position, self.radius - ASTEROID_MIN_RADIUS)
        asteroid2.velocity = self.velocity.rotate(-angle)*1.2
        