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
        self.rotation = 0
        self.rotation_speed = random.uniform(-250, 250)

    def draw(self, screen):
        rotated_points = []
        for (x, y) in self.points:
            vec = pygame.Vector2(x, y).rotate(self.rotation)
            rotated_points.append((self.position.x + vec.x, self.position.y + vec.y))
        pygame.draw.polygon(
            screen,
            "white",
            rotated_points,
            2
        )

    def update(self, dt):
        self.position += self.velocity * dt
        self.rotation += self.rotation * dt

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

    def explode(self):
        for _ in range(20):
            Particle(self.position, color="orange")

class Particle(pygame.sprite.Sprite):
    def __init__(self, position, color="white"):
        super().__init__(self.containers)
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)) * random.uniform(50, 150)
        self.radius = random.randint(2, 4)
        self.lifetime = random.uniform(0.5, 1.0)
        self.color = color

    def update(self, dt):
        self.position += self.velocity * dt
        self.radius -= dt * 4
        self.lifetime -= dt
        if self.radius <= 0 or self.lifetime <= 0:
            self.kill()

    def draw(self, screen):
        if self.radius > 0:
            pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), int(self.radius))