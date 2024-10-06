import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from bomb import *
from powerups import *

def main():
    pygame.init()
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image = pygame.image.load("background.jpg")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids!")
    clock = pygame.time.Clock()
    dt = 0
    score = 0
    lives = LIVES
    up_timer = POWERUP_TIMER

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    Player.containers = (updatable)
    AsteroidField.containers = (updatable)
    Asteroid.containers = (updatable, drawable, asteroids)
    Shot.containers = (updatable, drawable, shots)
    Bomb.containers = (drawable, shots)
    Powerup.containers = (drawable, powerups) 
    
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.blit(background_image, (0, 0))
        for object in updatable:
            object.update(dt)
        for asteroid in asteroids:
            
            if player.immunity < 0 and player.collision(asteroid):
                if player.shield:
                    player.shield = 0
                else:
                    lives -= 1
                    player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                if lives == 0:
                    print("Game over!")
                    with open("max_score.txt","r") as f:
                        max_score = int(f.read())
                    if max_score < score:
                        print("New max score!")
                        max_score = score
                    else:
                        print(f"Max score: {max_score}")
                    print(f"Score: {score}")
                    with open("max_score.txt","w") as f:
                        f.write(str(max_score))
                    return
                player.immunity = 3
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collision(shot):
                    asteroid.split()
                    shot.kill()
                    score += 1
                    if score % 100 == 0:
                        lives += 1
        for powerup in powerups:
            if player.collision(powerup):
                if powerup.type:
                    player.speed = 20
                else:
                    player.shield = 1
                powerup.kill()
        up_timer -= dt
        if up_timer < 0:
            new_powerup = Powerup()
            up_timer = POWERUP_TIMER
        for object in drawable:
            object.draw(screen)
        player.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()