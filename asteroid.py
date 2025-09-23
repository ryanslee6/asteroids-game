from circleshape import *
from main import *
from constants import *
from player import *
import random
import math

def generate_lumpy_shape(radius, irregularity = 0.4, num_points = 12):
    points = []
    for i in range(num_points):
        angle = (i / num_points) * 2 * math.pi
        offset = random.uniform(-irregularity, irregularity) * radius
        r = radius + offset
        x = math.cos(angle) * r
        y = math.sin(angle) * r
        points.append((x, y))
    return points

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.points = generate_lumpy_shape(radius)
        self.x = x
        self.y = y

    def draw(self, screen):
        translated_points = [
            (self.position.x + x, self.position.y + y) for (x, y) in self.points
        ]
        pygame.draw.polygon(
            screen,
            "white",
            translated_points,
            2
        )

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        random_angle = random.uniform(20, 50)
        new_velocity1 = self.velocity.rotate(random_angle)
        new_velocity2 = self.velocity.rotate(-random_angle)

        old_radius = self.radius
        new_radius = old_radius - ASTEROID_MIN_RADIUS

        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = new_velocity1 * 1.2
        
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = new_velocity2 * 1.2

