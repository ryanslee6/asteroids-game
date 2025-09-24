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
    font = pygame.font.Font(None, 36)
    background = pygame.image.load("Nebula_in_the_Cosmos.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    dt = 0
    score = 0
    
    
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

    paused = False
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
        
        screen.blit(background, (0, 0))
        
        if not paused:
            updatable.update(dt)

        if paused:
            font = pygame.font.SysFont(None, 74)
            text = font.render("Paused. Press 'p' to continue.", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
        
        for sprite in drawable:
            sprite.draw(screen)

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                print("Game over!")
                pygame.quit()
                sys.exit()

        #for asteroid in asteroids:
        #    for shot in shots:
        #        if asteroid.collides_with(shot):
        #            asteroid.kill()
        #            shot.kill()

        for asteroid in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid):
                    shot.kill()
                    asteroid.split()
                    score += 1

        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 50))

        pygame.display.flip()
        dt = clock.tick(60) / 1000
    


if __name__ == "__main__":
    main()
    