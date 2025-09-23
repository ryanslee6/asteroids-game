import pygame
import sys
from constants import *
from player import *
from asteroid import *
from asteroidfield import *



def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)
    AsteroidField.containers = (updatable, )
    Shot.containers = (shots, updatable, drawable)
    
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        screen.fill((0, 0, 0))
        

        updatable.update(dt)
        
        for sprite in drawable:
            sprite.draw(screen)

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                print("Game over!")
                pygame.quit()
                sys.exit()

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    asteroid.kill()
                    shot.kill()

        pygame.display.flip()
        dt = clock.tick(60) / 1000
    


if __name__ == "__main__":
    main()
    