import pygame
import sys
import os
from constants import *
from player import *
from asteroid import *
from asteroidfield import *

def load_high_score():
    if not os.path.exists(HIGH_SCORE_FILE):
        return 0
    with open(HIGH_SCORE_FILE, "r") as f:
        try:
            return int(f.read())
        except ValueError:
            return 0
        
def save_high_score(score):
    high_score = load_high_score()
    if score > high_score:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(score))

def reset_game(player, asteroids, shots, particles, updatable, drawable):

    score = 0

    player.position = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    player.rotation = 0

    for group in [asteroids, shots, particles, updatable, drawable]:
        group.empty()

    updatable.add(player)
    drawable.add(player)

    asteroid_field = AsteroidField()

    return score


def end_game_screen(screen, player, asteroids, shots, particles, updatable, drawable, score):
    save_high_score(score)
    high_score = load_high_score()


    #score = reset_game(player, asteroids, shots, particles, updatable, drawable)

    font = pygame.font.SysFont(None, 50)
    small_font = pygame.font.SysFont(None, 36)

    running = True
    while running:
        screen.fill((0, 0, 0))
        

        text = font.render("Game Over!", True, (255, 0, 0))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, 100))

        score_text = small_font.render(f"Your Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (screen.get_width()//2 - score_text.get_width()//2, 200))

        high_text = small_font.render(f"High Score: {high_score}", True, (0, 255, 0))
        screen.blit(high_text, (screen.get_width()//2 - high_text.get_width()//2, 250))

        restart_text = small_font.render(f"Press r to Restart or q to Quit", True, (255, 255, 255))
        screen.blit(restart_text, (screen.get_width()//2 - restart_text.get_width()//2, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    running = False
                    score = reset_game(player, asteroids, shots, particles, updatable, drawable)
                    return score

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
    particles = pygame.sprite.Group()
    
    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)
    AsteroidField.containers = (updatable, )
    Shot.containers = (shots, updatable, drawable)
    Particle.containers = (particles, )
    
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
            particles.update(dt)

        if paused:
            font = pygame.font.SysFont(None, 74)
            text = font.render("Paused. Press 'p' to continue.", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
        
        for sprite in drawable:
            sprite.draw(screen)

        for particle in particles:
            particle.draw(screen)

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                #end_game_screen(screen, score)
                score = end_game_screen(screen, player, asteroids, shots, particles, updatable, drawable, score)

        for asteroid in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid):
                    shot.kill()
                    asteroid.explode()
                    asteroid.split()
                    score += 1

        #save_high_score(score)
        #high_score = load_high_score

        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 50))

        pygame.display.flip()
        dt = clock.tick(60) / 1000
    


if __name__ == "__main__":
    main()
    