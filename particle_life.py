import pygame
import random
import numpy as np
from collections import defaultdict

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1550, 900

# Colors
BACKGROUND_COLOR = (11, 10, 34)
# Yellow, Blue, Pink, Green
PARTICLE_COLORS = [(255, 255, 0), (0, 255, 255), (255, 0, 255), (0, 255, 0)]
NUM_PARTICLES = 700

# Force matrix
max_random = 0.3
seed = 4     # (4), (8), (11)
random.seed(seed)  # Set the seed for reproducibility
# FORCE_MATRIX = {
#     PARTICLE_COLORS[0]: {
#         PARTICLE_COLORS[0]: random.uniform(-max_random, max_random),
#         PARTICLE_COLORS[1]: random.uniform(-max_random, max_random),
#         PARTICLE_COLORS[2]: random.uniform(-max_random, max_random),
#         PARTICLE_COLORS[3]: random.uniform(-max_random, max_random),
#     },
#     PARTICLE_COLORS[1]: {
#         PARTICLE_COLORS[0]: random.uniform(-max_random, max_random),
#         PARTICLE_COLORS[1]: random.uniform(-max_random, max_random),
#         PARTICLE_COLORS[2]: random.uniform(-max_random, max_random),
#         PARTICLE_COLORS[3]: random.uniform(-max_random, max_random),
#     },
#     PARTICLE_COLORS[2]: {
#         PARTICLE_COLORS[0]: random.uniform(-max_random, max_random),
#         PARTICLE_COLORS[1]: random.uniform(-max_random, max_random),
#         PARTICLE_COLORS[2]: random.uniform(-max_random, max_random),
#         PARTICLE_COLORS[3]: random.uniform(-max_random, max_random),
#     },
#     PARTICLE_COLORS[3]: {
#         PARTICLE_COLORS[0]: random.uniform(-max_random, max_random),
#         PARTICLE_COLORS[1]: random.uniform(-max_random, max_random),
#         PARTICLE_COLORS[2]: random.uniform(-max_random, max_random),
#         PARTICLE_COLORS[3]: random.uniform(-max_random, max_random),
#     },
# }


FORCE_MATRIX = {
    PARTICLE_COLORS[0]: {PARTICLE_COLORS[0]: -0.1, PARTICLE_COLORS[1]: -0.05, PARTICLE_COLORS[2]: 0, PARTICLE_COLORS[3]: 0},
    PARTICLE_COLORS[1]: {PARTICLE_COLORS[0]: 0.04, PARTICLE_COLORS[1]: -0.1, PARTICLE_COLORS[2]: -0.06, PARTICLE_COLORS[3]: 0},
    PARTICLE_COLORS[2]: {PARTICLE_COLORS[0]: 0, PARTICLE_COLORS[1]: 0.05, PARTICLE_COLORS[2]: -0.1, PARTICLE_COLORS[3]: -0.07},
    PARTICLE_COLORS[3]: {PARTICLE_COLORS[0]: 0, PARTICLE_COLORS[1]: 0, PARTICLE_COLORS[2]: 0.06, PARTICLE_COLORS[3]: -0.1},
}

# Minimum and maximum distance for forces
MIN_DISTANCE = 15
MAX_DISTANCE = 100
FRICTION = 0.8  # Friction factor
REPULSIVE_FORCE = 3

# Particle class
class Particle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vx = 0  # Initial velocity set to 0
        self.vy = 0  # Initial velocity set to 0

    def move(self):
        self.vx *= FRICTION  # Applying friction to velocity
        self.vy *= FRICTION  # Applying friction to velocity
        self.x += self.vx
        self.y += self.vy

        # Wrap around edges
        if self.x < 0:
            self.x += WIDTH
        elif self.x > WIDTH:
            self.x -= WIDTH
        if self.y < 0:
            self.y += HEIGHT
        elif self.y > HEIGHT:
            self.y -= HEIGHT

    def apply_force(self, fx, fy):
        self.vx += fx
        self.vy += fy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

def calculate_force(distance, max_force):
    if distance < MIN_DISTANCE:
        return -REPULSIVE_FORCE * (1 - distance / MIN_DISTANCE)
    elif distance < (MAX_DISTANCE + MIN_DISTANCE) / 2:
        return -2 * max_force * (distance - MIN_DISTANCE) / (MAX_DISTANCE - MIN_DISTANCE)
    elif distance < MAX_DISTANCE:
        return 2 * max_force * (distance - MAX_DISTANCE) / (MAX_DISTANCE - MIN_DISTANCE)
    else:
        return 0

def get_neighboring_cells(cell, grid_size):
    x, y = cell
    neighboring_cells = [
        ((x - 1) % grid_size, (y - 1) % grid_size),
        ((x - 1) % grid_size, y % grid_size),
        ((x - 1) % grid_size, (y + 1) % grid_size),
        (x % grid_size, (y - 1) % grid_size),
        (x % grid_size, (y + 1) % grid_size),
        ((x + 1) % grid_size, (y - 1) % grid_size),
        ((x + 1) % grid_size, y % grid_size),
        ((x + 1) % grid_size, (y + 1) % grid_size),
    ]
    return neighboring_cells

def spatial_partition(particles, cell_size):
    grid_size_x = (WIDTH // cell_size) + 1
    grid_size_y = (HEIGHT // cell_size) + 1
    grid = defaultdict(list)
    for particle in particles:
        cell = (int(particle.x // cell_size), int(particle.y // cell_size))
        grid[cell].append(particle)
    return grid, grid_size_x, grid_size_y


def draw_force_matrix(screen, font):
    matrix_size = len(PARTICLE_COLORS)
    matrix_width = 150  # Width of the matrix area
    matrix_height = 150  # Height of the matrix area
    cell_width = matrix_width // (matrix_size + 1)  # Width of each cell
    cell_height = matrix_height // (matrix_size + 1)  # Height of each cell
    x_offset = 10  # Offset from the left
    y_offset = 10  # Offset from the top

    # Render matrix title
    title_text = font.render("Force Matrix", True, (255, 255, 255))
    screen.blit(title_text, (x_offset, y_offset))

    # Render headers
    circle_radius = 10
    headers = [""] + PARTICLE_COLORS  # Include an empty header for the first cell
    for i, color in enumerate(headers):
        if i > 0:  # Skip the first empty header
            # Draw circle for column headers
            pygame.draw.circle(screen, color, (x_offset + (i) * cell_width + cell_width // 2, y_offset + 20 + cell_height // 2), circle_radius)
            pygame.draw.circle(screen, (255, 255, 255), (x_offset + (i) * cell_width + cell_width // 2, y_offset + 20 + cell_height // 2), circle_radius, 1)
            
            # Draw circle for row headers
            pygame.draw.circle(screen, color, (x_offset + cell_width // 2, y_offset + 20 + (i) * cell_height + cell_height // 2), circle_radius)
            pygame.draw.circle(screen, (255, 255, 255), (x_offset + cell_width // 2, y_offset + 20 + (i) * cell_height + cell_height // 2), circle_radius, 1)

    # Render matrix cells with force values
    for i, color1 in enumerate(PARTICLE_COLORS):
        for j, color2 in enumerate(PARTICLE_COLORS):
            force = FORCE_MATRIX[color1][color2]

            # Draw cell outline
            pygame.draw.rect(screen, (255, 255, 255), (x_offset + (j + 1) * cell_width, y_offset + 20 + (i + 1) * cell_height, cell_width, cell_height), 1)

            # Render force value with background color
            text = f"{force:.2f}"
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(x_offset + (j + 1) * cell_width + cell_width // 2, y_offset + 20 + (i + 1) * cell_height + cell_height // 2))
            screen.blit(text_surface, text_rect)






# Main function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Particle Life Simulation")

    font = pygame.font.Font(None, 14)

    particles = [Particle(random.randint(0, WIDTH), random.randint(0, HEIGHT), 3, random.choice(PARTICLE_COLORS)) for _ in range(NUM_PARTICLES)]

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move particles
        for particle in particles:
            particle.move()

        # Spatial partitioning
        cell_size = MAX_DISTANCE // 2  # Make grid cells smaller
        grid, grid_size_x, grid_size_y = spatial_partition(particles, cell_size)

        # Apply forces with spatial partitioning
        for cell, cell_particles in grid.items():
            for i, particle in enumerate(cell_particles):
                for j in range(i+1, len(cell_particles)):
                    other = cell_particles[j]
                    dx = other.x - particle.x
                    dy = other.y - particle.y

                    # Wrap around distances
                    if abs(dx) > WIDTH / 2:
                        dx = -np.sign(dx) * (WIDTH - abs(dx))
                    if abs(dy) > HEIGHT / 2:
                        dy = -np.sign(dy) * (HEIGHT - abs(dy))

                    distance = np.hypot(dx, dy)
                    max_force1 = FORCE_MATRIX[particle.color][other.color]
                    max_force2 = FORCE_MATRIX[other.color][particle.color]

                    force1 = calculate_force(distance, max_force1)
                    force2 = calculate_force(distance, max_force2)

                    if force1 != 0:
                        fx1 = force1 * dx / distance
                        fy1 = force1 * dy / distance
                        particle.apply_force(fx1, fy1)

                    if force2 != 0:
                        fx2 = - force2 * dx / distance
                        fy2 = - force2 * dy / distance                          
                        other.apply_force(fx2, fy2)

                # Check neighboring cells
                for neighbor in get_neighboring_cells(cell, max(grid_size_x, grid_size_y)):
                    if neighbor in grid:
                        for other in grid[neighbor]:
                            dx = other.x - particle.x
                            dy = other.y - particle.y

                            # Wrap around distances
                            if abs(dx) > WIDTH / 2:
                                dx = -np.sign(dx) * (WIDTH - abs(dx))
                            if abs(dy) > HEIGHT / 2:
                                dy = -np.sign(dy) * (HEIGHT - abs(dy))

                            distance = np.hypot(dx, dy)
                            max_force1 = FORCE_MATRIX[particle.color][other.color]
                            max_force2 = FORCE_MATRIX[other.color][particle.color]

                            force1 = calculate_force(distance, max_force1)
                            force2 = calculate_force(distance, max_force2)

                            if force1 != 0:
                                fx1 = force1 * dx / distance
                                fy1 = force1 * dy / distance
                                particle.apply_force(fx1, fy1)

                            if force2 != 0:
                                fx2 = - force2 * dx / distance
                                fy2 = - force2 * dy / distance                          
                                other.apply_force(fx2, fy2)

        # Draw particles
        screen.fill(BACKGROUND_COLOR)
        # Draw force matrix on top left
        draw_force_matrix(screen, font)

        for particle in particles:
            particle.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
