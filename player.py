from circleshape import *
from shot import *
from bomb import *

class Player(CircleShape):
    def __init__(self,x,y):
        super().__init__(x,y,PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0
        self.bomb_cooldown = 0
        self.shot_type = 0
        self.e_hold = 0
        self.shield = 0
        self.speed = 0
        self.immunity = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self,screen):
        if self.immunity > 0:
            pygame.draw.polygon(screen,(100,100,255),self.triangle())
        else:
            pygame.draw.polygon(screen,(0,0,0),self.triangle())
        if self.speed > 0:
            pygame.draw.polygon(screen,(0,255,0),self.triangle(),2)
        else:
            pygame.draw.polygon(screen,(255,255,255),self.triangle(),2)
        if self.shield:
            pygame.draw.circle(screen,(100,100,255),self.position,self.radius+10,2)

    def rotate(self, dt):
        self.rotation += dt * PLAYER_TURN_SPEED
    
    def update(self, dt):
        keys = pygame.key.get_pressed()

        self.immunity -= dt
        self.speed -= dt

        if self.shot_type:
            self.shot_cooldown -= dt / 3
        else:
            self.shot_cooldown -= dt
        self.bomb_cooldown -= dt

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if self.bomb_cooldown < 0 and keys[pygame.K_q]:
            self.bomb_cooldown = PLAYER_BOMB_COOLDOWN
            new_bomb = Bomb(*self.position)
        if keys[pygame.K_e]:
            if self.e_hold == 0:
                self.shot_type = 1 - self.shot_type
                self.e_hold = 1
        else:
            self.e_hold = 0
        if self.shot_cooldown < 0 and keys[pygame.K_SPACE]:
            self.shot_cooldown = PLAYER_SHOOT_COOLDOWN
            self.shoot()

    def move(self,dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        if 0 < self.speed:
            self.position += forward * PLAYER_SPEED * dt * 1.5
        else:
            self.position += forward * PLAYER_SPEED * dt
        if self.position[0] + ASTEROID_MAX_RADIUS < 0:
            self.position[0] += SCREEN_WIDTH + 2*ASTEROID_MAX_RADIUS
        if self.position[0] - ASTEROID_MAX_RADIUS > SCREEN_WIDTH:
            self.position[0] -= SCREEN_WIDTH + 2*ASTEROID_MAX_RADIUS
        if self.position[1] + ASTEROID_MAX_RADIUS < 0:
            self.position[1] += SCREEN_HEIGHT + 2*ASTEROID_MAX_RADIUS
        if self.position[1] - ASTEROID_MAX_RADIUS > SCREEN_HEIGHT:
            self.position[1] -= SCREEN_HEIGHT + 2*ASTEROID_MAX_RADIUS

    def shoot(self):
        if self.shot_type:
            new_shot1 = Shot(*self.position)
            new_shot2 = Shot(*self.position)
            new_shot3 = Shot(*self.position)
            new_shot1.velocity = pygame.Vector2(0,1).rotate(self.rotation+20) * PLAYER_SHOOT_SPEED
            new_shot2.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            new_shot3.velocity = pygame.Vector2(0,1).rotate(self.rotation-20) * PLAYER_SHOOT_SPEED
        else:
            new_shot = Shot(*self.position)
            new_shot.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
    
    def collision(self,circle):
        if self.shield:
            if self.position.distance_to(circle.position) < self.radius + circle.radius + 10:
                return 1
            return 0
        points = self.triangle()
        for i in range(3):
            if circle.position.distance_to(points[i]) < circle.radius:
                return True
        for i in range(3):
            if circle.position.distance_to((points[i]+points[(i+1)%3])/2) < circle.radius:
                return True
        return 0
