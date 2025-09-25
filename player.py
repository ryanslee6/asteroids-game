from circleshape import *
from constants import *
from main import *


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rotation = 0
        self.shoot_timer = 0

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(
            screen,
            "white",
            self.triangle(),
            2
        )

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
            
        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.move(-dt)
    
        if keys[pygame.K_SPACE] and self.shoot_timer <= 0:
            self.shoot()

        if self.shoot_timer > 0:
            self.shoot_timer -= dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        velocity = direction * PLAYER_SHOT_SPEED
        position = pygame.Vector2(self.position.x, self.position.y)
        Shot(position, velocity)

        self.shoot_timer = PLAYER_SHOOT_COOLDOWN

#    def shoot(self):
#        direction = pygame.Vector2(0, 1)
#        direction = direction.rotate(self.rotation)
#        velocity = direction * PLAYER_SHOT_SPEED
#
#        Shot(self.position.x, self.position.y, SHOT_RADIUS, velocity)
#        self.shoot_timer = PLAYER_SHOOT_COOLDOWN

class Shot(pygame.sprite.Sprite):
    def __init__(self, position, velocity, color=(0, 255, 0)):
        super().__init__(self.containers)
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.color = color
        self.length = 16
        self.width = 3
        self.radius = 2

    def update(self, dt):
        self.position += self.velocity * dt
    
    def draw(self, screen):
        end_pos = self.position + self.velocity.normalize() * self.length
        
        glow_surf = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        for i, alpha in enumerate([50, 30, 15], start = 1):
            pygame.draw.line(
                glow_surf,
                (*self.color, alpha),
                self.position,
                end_pos,
                self.width + i*2
            )
        screen.blit(glow_surf, (0, 0))
        
        pygame.draw.line(screen, self.color, self.position, end_pos, self.width)

    def collides_with(self, other):
        distance = self.position.distance_to(other.position)
        return distance <= (self.radius + other.radius)



#class Shot(CircleShape):
#    def __init__(self, x, y, radius, velocity):
#        super().__init__(x, y, radius)
#        pygame.sprite.Sprite.__init__(self, self.containers)
#        self.velocity = velocity
#
#    def draw(self, screen):
#        pygame.draw.circle(
#            screen,
#            "white",
#            (int(self.position.x), int(self.position.y)),
#            self.radius,
#            0
#        )
#
#    def update(self, dt):
#        self.position += self.velocity * dt