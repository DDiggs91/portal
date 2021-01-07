import pygame
import math

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1200
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)


class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.surface.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.image.fill((0, 0, 0))


class Particle(pygame.sprite.Sprite):

    def __init__(self, size):
        super().__init__()

        self.size = size
        self.image = pygame.surface.Surface((size, size))
        self.rect = self.image.get_rect()

        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))

        self.color = (255, 0, 0)
        pygame.draw.circle(self.image, self.color, (self.size // 2, self.size // 2), self.size // 2)

        self.mass = 1
        self.friction = .9
        self.elasticity = .5

        self.acceleration_x = 0
        self.acceleration_y = 0
        self.speed_x = 0
        self.speed_y = 0

        self.gravity = True

        self.collision_rectangle = None
        self.update_collision_rectangle()

    def update(self, collision_groups=None, *args, **kwargs):
        self.update_forces()

        self.speed_x += self.acceleration_x
        self.rect.centerx += self.speed_x
        self.update_collision_rectangle()

        for sprite in collision_groups[0]:
            collision = self.collision_rectangle.colliderect(sprite.rect)
            if collision:
                if self.speed_x > 0:
                    self.rect.right = sprite.rect.left - (self.collision_rectangle.right - sprite.rect.left)
                else:
                    self.rect.left = sprite.rect.right - (self.collision_rectangle.left - sprite.rect.right)
                self.speed_x = -self.elasticity * self.speed_x
        if abs(self.speed_x) < 1:
            self.speed_x = 0

        self.speed_y += self.acceleration_y
        self.rect.centery += self.speed_y
        self.update_collision_rectangle()

        # pygame.draw.rect(DISPLAY_SURFACE, (255, 255, 255), self.collision_rectangle)
        for sprite in collision_groups[0]:
            collision = self.collision_rectangle.colliderect(sprite.rect)
            if collision:
                if self.speed_y > 0:
                    self.rect.bottom = sprite.rect.top - (self.collision_rectangle.bottom - sprite.rect.top)
                else:
                    self.rect.top = sprite.rect.bottom - (self.collision_rectangle.top - sprite.rect.bottom)
                self.speed_y = -self.elasticity * self.speed_y
                self.speed_x *= self.friction

        self.speed_y = math.floor(self.speed_y)

        for sprite in collision_groups[1]:
            if self.collision_rectangle.colliderect(sprite.rect):
                velocity_angle = -1 * math.atan2(self.speed_y, self.speed_x) * 180 / math.pi
                velocity_magnitude = (self.speed_x ** 2 + self.speed_y ** 2) ** 0.5
                if velocity_angle < 0:
                    velocity_angle += 360
                relative_angle = sprite.direction - velocity_angle
                if relative_angle > 180:
                    relative_angle -= 180
                elif relative_angle < 0:
                    relative_angle += 180
                self.rect.center = sprite.partner.rect.center
                new_velocity_angle = (sprite.direction - sprite.partner.direction - velocity_angle + 180) % 360
                self.speed_y = velocity_magnitude * math.sin(new_velocity_angle * math.pi / 180)
                self.speed_x = velocity_magnitude * math.cos(new_velocity_angle * math.pi / 180)

                self.rect.centerx += self.speed_x
                self.rect.centery += self.speed_y


    def update_collision_rectangle(self):

        if self.speed_x > 0:
            left = self.rect.x
            width = self.rect.width + self.speed_x
        else:
            left = self.rect.x + self.speed_x
            width = self.rect.width - self.speed_x

        if self.speed_y > 0:
            top = self.rect.y
            height = self.rect.height + self.speed_y
        else:
            top = self.rect.y + self.speed_y
            height = self.rect.height - self.speed_y

        self.collision_rectangle = pygame.Rect(left, top, width, height)

    def update_forces(self):
        force_x = 0
        force_y = 0

        if self.gravity:
            force_y = self.mass * 1

        self.acceleration_x = force_x / self.mass
        self.acceleration_y = force_y / self.mass


class Portal(pygame.sprite.Sprite):

    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface([100, 25])
        if self.color == 'blue':
            pygame.draw.ellipse(self.image, '#ffffff', [0, 0, 100, 25])
            pygame.draw.ellipse(self.image, '#0065ff', [5, 1, 90, 23])
        elif self.color == 'orange':
            pygame.draw.ellipse(self.image, '#ffffff', [0, 0, 100, 25])
            pygame.draw.ellipse(self.image, '#ff9a00', [5, 1, 90, 23])
        self.image.set_colorkey('#000000')
        self.rect = self.image.get_rect()
        self.direction = 270
        self.partner = None

    def rotate(self, angle):
        self.direction = angle
        center = self.rect.center
        self.image = pygame.Surface([100, 25])
        if self.color == 'blue':
            pygame.draw.ellipse(self.image, '#ffffff', [0, 0, 100, 25])
            pygame.draw.ellipse(self.image, '#0065ff', [5, 1, 90, 23])
        elif self.color == 'orange':
            pygame.draw.ellipse(self.image, '#ffffff', [0, 0, 100, 25])
            pygame.draw.ellipse(self.image, '#ff9a00', [5, 1, 90, 23])
        self.image.set_colorkey('#000000')
        self.rect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.image, self.direction)

        self.rect.center = center


def main():
    global DISPLAY_SURFACE, CLOCK, WINDOW_SIZE
    pygame.init()
    CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode(WINDOW_SIZE)
    mouse_position = (0, 0)

    physics_objects = pygame.sprite.Group()
    new_particle = Particle(25)
    new_particle.rect.center = (350, 199)
    new_particle.speed_x = 5
    new_particle.speed_y = 0
    physics_objects.add(new_particle)

    new_particle2 = Particle(25)
    new_particle2.rect.center = (350, 199)
    new_particle2.speed_x = 15
    new_particle2.speed_y = 0
    physics_objects.add(new_particle2)

    walls = pygame.sprite.Group()
    floor = Wall(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH, 10)
    walls.add(floor)
    right_wall = Wall(WINDOW_WIDTH - 10, 0, 10, WINDOW_HEIGHT)
    walls.add(right_wall)
    left_wall = Wall(0, 0, 10, WINDOW_HEIGHT)
    walls.add(left_wall)

    points1 = []
    points2 = []

    portal_group = pygame.sprite.Group()

    portal_1 = Portal('blue')
    portal_1.rect.center = [150, WINDOW_HEIGHT  // 2]
    portal_1.rotate(90)
    portal_group.add(portal_1)

    portal_2 = Portal('orange')
    portal_2.rect.center = [600, WINDOW_HEIGHT - 40]
    portal_group.add(portal_2)

    portal_1.partner = portal_2
    portal_2.partner = portal_1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEMOTION:
                mouse_position = pygame.mouse.get_pos()

        DISPLAY_SURFACE.fill((100, 100, 100))

        walls.update()
        walls.draw(DISPLAY_SURFACE)

        physics_objects.update([walls, portal_group])
        physics_objects.draw(DISPLAY_SURFACE)

        portal_group.update()
        portal_group.draw(DISPLAY_SURFACE)

        points1.append((new_particle.rect.centerx, new_particle.rect.bottom))
        if len(points1) > 1:
            pygame.draw.lines(DISPLAY_SURFACE, (0, 0, 0), False, points1)

        points2.append((new_particle2.rect.centerx, new_particle2.rect.bottom))
        if len(points2) > 1:
            pygame.draw.lines(DISPLAY_SURFACE, (0, 0, 0), False, points2)

        pygame.display.update()
        CLOCK.tick(30)


if __name__ == '__main__':
    main()
