
import math
import random
import pygame
from collections import deque

TILE = 32
COLS = 25
ROWS = 18
WIDTH = COLS * TILE
HEIGHT = ROWS * TILE
FPS = 60
PLAYER_MOVE_DELAY = 0.12

BLACK = (15, 15, 20)
WHITE = (240, 240, 240)
GREEN = (60, 220, 100)
RED = (240, 70, 70)
YELLOW = (255, 220, 50)
BLUE = (80, 150, 255)

particles = []


def dirt_color(row):
    """Return a dirt colour based on underground depth."""
    if row <= 3:
        return (170, 110, 60)
    elif row <= 6:
        return (150, 90, 50)
    elif row <= 9:
        return (125, 75, 45)
    elif row < ROWS:
        return (100, 60, 40)
    return None


def on_enemy_popped(enemy, score):
    """Create a particle burst when an enemy is popped."""
    center_x = enemy.x + TILE // 2
    center_y = enemy.y + TILE // 2

    for _ in range(18):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(45, 150)

        particles.append({
            "x": float(center_x),
            "y": float(center_y),
            "vx": math.cos(angle) * speed,
            "vy": math.sin(angle) * speed,
            "life": random.uniform(0.3, 0.7),
            "max_life": 0.7,
            "color": random.choice([YELLOW, WHITE, RED]),
        })


def enemy_speed_multiplier(level):
    """Make enemies faster as the level increases."""
    return 1 + 0.1 * level


def bfs_path(start, goal, grid):
    """Find a shortest path through the grid using BFS."""
    queue = deque([start])
    came_from = {start: None}

    while queue:
        cell = queue.popleft()

        if cell == goal:
            break

        x, y = cell

        for nx, ny in [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]:
            if (
                0 <= nx < COLS
                and 0 <= ny < ROWS
                and grid[ny][nx] == 0
                and (nx, ny) not in came_from
            ):
                came_from[(nx, ny)] = cell
                queue.append((nx, ny))

    if goal not in came_from:
        return []

    path = []
    cell = goal

    while cell is not None:
        path.append(cell)
        cell = came_from[cell]

    path.reverse()
    return path


class Enemy:
    def __init__(self, x, y):
        self.x = x * TILE
        self.y = y * TILE
        self.pumped = 0
        self.direction = random.choice([
            (1, 0), (-1, 0), (0, 1), (0, -1)
        ])
        self.move_timer = 0

    def draw(self, screen):
        color = RED if self.pumped == 0 else YELLOW

        pygame.draw.ellipse(
            screen,
            color,
            (
                int(self.x + 3),
                int(self.y + 3),
                TILE - 6,
                TILE - 6,
            ),
        )


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dig Dug")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)

        self.reset()

    def reset(self):
        particles.clear()

        self.player_x = COLS // 2
        self.player_y = 2

        self.player_move_timer = 0

        self.grid = [
            [0 if row < 3 else 1 for col in range(COLS)]
            for row in range(ROWS)
        ]

        self.enemies = [
            Enemy(4, 7),
            Enemy(18, 8),
            Enemy(8, 13),
        ]

        self.score = 0
        self.lives = 3
        self.level = 1
        self.state = "play"
        self.pump_timer = 0
        self.pumping = False

    def update_particles(self, dt):
        """Move particles and remove expired ones."""
        for particle in particles[:]:
            particle["x"] += particle["vx"] * dt
            particle["y"] += particle["vy"] * dt
            particle["vy"] += 180 * dt
            particle["life"] -= dt

            if particle["life"] <= 0:
                particles.remove(particle)

    def update(self, dt):
        self.update_particles(dt)

        if self.state != "play":
            return

        keys = pygame.key.get_pressed()

        self.player_move_timer += dt

        dx = (
            int(keys[pygame.K_RIGHT])
            - int(keys[pygame.K_LEFT])
        )
        dy = (
            int(keys[pygame.K_DOWN])
            - int(keys[pygame.K_UP])
        )

        if (dx or dy) and self.player_move_timer >= PLAYER_MOVE_DELAY:
            self.player_move_timer = 0

            self.player_x = max(
                0, min(COLS - 1, self.player_x + dx)
            )
            self.player_y = max(
                0, min(ROWS - 1, self.player_y + dy)
            )

            self.grid[self.player_y][self.player_x] = 0

        self.pumping = keys[pygame.K_SPACE]
        self.pump_timer += dt

        if self.pumping and self.pump_timer > 0.25:
            self.pump_timer = 0

            for enemy in self.enemies[:]:
                distance = (
                    abs(enemy.x // TILE - self.player_x)
                    + abs(enemy.y // TILE - self.player_y)
                )

                if distance <= 2:
                    enemy.pumped += 1

                    if enemy.pumped >= 3:
                        self.enemies.remove(enemy)
                        self.score += 100
                        on_enemy_popped(enemy, self.score)

        self.update_enemies(dt)

        if not self.enemies:
            self.level += 1

            self.enemies = [
                Enemy(
                    random.randint(1, COLS - 2),
                    random.randint(5, ROWS - 2),
                )
                for _ in range(2 + self.level)
            ]

    def update_enemies(self, dt):
        for enemy in self.enemies:
            enemy.move_timer += dt

            move_delay = (
                0.35 / enemy_speed_multiplier(self.level)
            )

            if enemy.move_timer < move_delay:
                continue

            enemy.move_timer = 0

            start = (
                int(enemy.x // TILE),
                int(enemy.y // TILE),
            )

            goal = (self.player_x, self.player_y)
            path = bfs_path(start, goal, self.grid)

            if len(path) > 1:
                next_x, next_y = path[1]
                enemy.x = next_x * TILE
                enemy.y = next_y * TILE

            if start == goal:
                self.lives -= 1

                enemy.x = random.randint(0, COLS - 1) * TILE
                enemy.y = random.randint(4, ROWS - 1) * TILE

                if self.lives <= 0:
                    self.state = "over"

    def draw(self):
        self.screen.fill(BLACK)

        for row in range(ROWS):
            for col in range(COLS):
                if self.grid[row][col] == 1:
                    color = dirt_color(row)

                    if color is not None:
                        pygame.draw.rect(
                            self.screen,
                            color,
                            (
                                col * TILE,
                                row * TILE,
                                TILE,
                                TILE,
                            ),
                        )

        pygame.draw.rect(
            self.screen,
            GREEN,
            (
                self.player_x * TILE + 5,
                self.player_y * TILE + 5,
                TILE - 10,
                TILE - 10,
            ),
        )

        for enemy in self.enemies:
            enemy.draw(self.screen)

        for particle in particles:
            radius = max(
                1,
                int(
                    4 * particle["life"]
                    / particle["max_life"]
                ),
            )

            pygame.draw.circle(
                self.screen,
                particle["color"],
                (
                    int(particle["x"]),
                    int(particle["y"]),
                ),
                radius,
            )

        info = self.font.render(
            f"Score: {self.score}  Lives: {self.lives}  Level: {self.level}",
            True,
            WHITE,
        )

        self.screen.blit(info, (8, 8))

        if self.state == "over":
            message = self.font.render(
                "GAME OVER - Press R to restart",
                True,
                WHITE,
            )

            self.screen.blit(
                message,
                message.get_rect(
                    center=(WIDTH // 2, HEIGHT // 2)
                ),
            )

        pygame.display.flip()

    def run(self):
        running = True

        while running:
            dt = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    elif (
                        event.key == pygame.K_r
                        and self.state == "over"
                    ):
                        self.reset()

            self.update(dt)
            self.draw()

        pygame.quit()


if __name__ == "__main__":
    Game().run()