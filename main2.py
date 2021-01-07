import pygame
import math

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1200
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)


class Particle(pygame.sprite.Sprite):

    def __init__(self, size, name):
        super().__init__()

        self.size = size
        self.name = name
        self.image = pygame.surface.Surface((size, size))
        self.rect = self.image.get_rect()

        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))

        self.color = (255, 0, 0)
        pygame.draw.circle(self.image, self.color, (self.size // 2, self.size // 2), self.size // 2)

        self.direction = 90 * math.pi / 180
        self.speed = 10

    def update(self, particle1, *args, **kwargs):
        if self.name == 2:
            self.direction = math.atan2(-(particle1.rect.y - self.rect.y), (particle1.rect.x - self.rect.x))
            # print(round(self.direction * 180/math.pi))
        self.rect.x += self.speed * math.cos(self.direction)
        self.rect.y += self.speed * math.sin(self.direction + math.pi)


def main():
    global DISPLAY_SURFACE, CLOCK, WINDOW_SIZE
    pygame.init()
    CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode(WINDOW_SIZE)
    mouse_position = (0, 0)
    result = 1
    speed = 1.467
    while result > 0:
        speed += 0.0001
        result = test(speed)
    print(speed, result)


def test(speed):
    particle1 = Particle(10, 1)
    particle1.rect.center = (200, 1000)

    particle2 = Particle(10, 2)
    particle2.rect.center = (1000, 1000)
    particle2.speed *= speed

    particles = pygame.sprite.Group()
    particles.add(particle1)
    particles.add(particle2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEMOTION:
                mouse_position = pygame.mouse.get_pos()

        DISPLAY_SURFACE.fill((100, 100, 100))
        particles.update(particle1)
        particles.draw(DISPLAY_SURFACE)
        if pygame.sprite.collide_mask(particle1, particle2):
            return 100 - particle1.rect.y

        pygame.display.update()
        CLOCK.tick(30)


if __name__ == '__main__':
    main()
