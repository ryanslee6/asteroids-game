from circleshape import *
from main import *

class Asteroid(CircleShape):
    containers = None
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            "white",
            (int(self.x), int(self.y)),
            self.radius,
            2
        )

    def update(self, dt):
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt