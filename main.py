import sys
import pygame
import math
import random

FPS = 60
WIDTH, HEIGHT = 680, 480
BORDER_DELTA = min(WIDTH, HEIGHT) / 4

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TILE = 50
world = []

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rays")

clock = pygame.time.Clock()

pygame.mouse.set_visible(False)


class Player:
    def __init__(self, width, height):
        self.x = width / 2
        self.y = height / 2
        self.angle = 0
        self.fov = math.pi / 3
        self.rays = 120
        self.delta_angle = self.fov / self.rays
        self.max_depth = 600
        self.speed = 1

    def cast_ray(self, angle):
        x, y = self.x, self.y
        for _ in range(self.max_depth):
            x += math.cos(angle)
            y += math.sin(angle)
            if self.check_collision(x, y):
                return (x, y)
        return (x, y)

    def check_collision(self, x, y):
        for tile in world:
            if tile[0] < x < tile[0] + TILE and tile[1] < y < tile[1] + TILE:
                return True
        return False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle -= 0.05
        if keys[pygame.K_RIGHT]:
            self.angle += 0.05
        if keys[pygame.K_w]:
            self.x += self.speed * math.cos(self.angle)
            self.y += self.speed * math.sin(self.angle)
        if keys[pygame.K_s]:
            self.x -= self.speed * math.cos(self.angle)
            self.y -= self.speed * math.sin(self.angle)
        if keys[pygame.K_a]:
            self.x += self.speed * math.sin(self.angle)
            self.y -= self.speed * math.cos(self.angle)
        if keys[pygame.K_d]:
            self.x -= self.speed * math.sin(self.angle)
            self.y += self.speed * math.cos(self.angle)

    def update_mouse_rotation(self):
        max_distance = min(WIDTH, HEIGHT) / 2
        mouse_x, mouse_y = pygame.mouse.get_pos()

        mouse_x = max(0, min(mouse_x, WIDTH))
        mouse_y = max(0, min(mouse_y, HEIGHT))

        if mouse_x < BORDER_DELTA or mouse_x > WIDTH - BORDER_DELTA or mouse_y < BORDER_DELTA or mouse_y > HEIGHT - BORDER_DELTA:
            pygame.mouse.set_pos(WIDTH / 2, HEIGHT / 2)
            return

        center_x = self.x + WIDTH / 2
        center_y = self.y + HEIGHT / 2

        dx = mouse_x - center_x
        dy = mouse_y - center_y

        distance = math.hypot(dx, dy)

        if distance > max_distance:
            dx = dx * max_distance / distance
            dy = dy * max_distance / distance

        self.angle = math.atan2(dy, dx)

    def draw_player(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 3)

    def draw_walls(self, screen):
        screen.fill(BLACK)

        for i in range(self.rays):
            ray_angle = self.angle - self.fov / 2 + i * self.delta_angle
            end_point = self.cast_ray(ray_angle)
            distance = math.sqrt(
                (end_point[0] - self.x) ** 2 + (end_point[1] - self.y) ** 2
            )

            # fish_eye = math.cos(ray_angle - self.angle)

            wall_height = min(int(HEIGHT / distance) * 2, HEIGHT)
            wall_color = (
                0,
                min(255, int(255 / (1 + distance * distance * 0.00005))),
                0,
            )

            pygame.draw.rect(
                screen,
                wall_color,
                (
                    i * WIDTH // self.rays,
                    (HEIGHT - wall_height) // 2,
                    WIDTH // self.rays + 1,
                    wall_height,
                ),
            )


player = Player(WIDTH, HEIGHT)

for _ in range(15):
    tile_x = random.randint(0, WIDTH - TILE)
    tile_y = random.randint(0, HEIGHT - TILE)
    world.append((tile_x, tile_y))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    player.update()
    # player.update_mouse_rotation()
    player.draw_walls(screen)
    pygame.display.flip()
    clock.tick(FPS)
