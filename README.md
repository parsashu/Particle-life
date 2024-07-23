#Particle Life Simulation
This is a particle-based life simulation implemented using Pygame. The simulation demonstrates the interaction between different particles based on predefined forces. Each particle type interacts with others through attraction or repulsion, resulting in dynamic and emergent behavior.

Features
Particle Simulation: Simulates the movement and interaction of particles.
Force Matrix: Defines the attraction or repulsion between different particle types.
Spatial Partitioning: Efficiently calculates forces using spatial partitioning to handle a large number of particles.
Visualization: Displays the particles and the force matrix in real-time.
Requirements
Python 3.7+
Pygame 2.0+
Installation
Clone the repository:


git clone https://github.com/yourusername/particle-life-simulation.git
cd particle-life-simulation
Install the required packages:


pip install pygame
Usage
Run the simulation:


python main.py
Configuration
Force Matrix
The force matrix defines the interaction between different particle types. You can modify the force values in the FORCE_MATRIX dictionary:


FORCE_MATRIX = {
    PARTICLE_COLORS[0]: {PARTICLE_COLORS[0]: -0.1, PARTICLE_COLORS[1]: -0.05, PARTICLE_COLORS[2]: 0, PARTICLE_COLORS[3]: 0},
    PARTICLE_COLORS[1]: {PARTICLE_COLORS[0]: 0.04, PARTICLE_COLORS[1]: -0.1, PARTICLE_COLORS[2]: -0.06, PARTICLE_COLORS[3]: 0},
    PARTICLE_COLORS[2]: {PARTICLE_COLORS[0]: 0, PARTICLE_COLORS[1]: 0.05, PARTICLE_COLORS[2]: -0.1, PARTICLE_COLORS[3]: -0.07},
    PARTICLE_COLORS[3]: {PARTICLE_COLORS[0]: 0, PARTICLE_COLORS[1]: 0, PARTICLE_COLORS[2]: 0.06, PARTICLE_COLORS[3]: -0.1},
}
Simulation Parameters
You can adjust various parameters to change the behavior of the simulation:

WIDTH, HEIGHT: Screen dimensions.
BACKGROUND_COLOR: Background color of the simulation.
PARTICLE_COLORS: List of colors representing different particle types.
NUM_PARTICLES: Number of particles in the simulation.
MIN_DISTANCE, MAX_DISTANCE: Distance thresholds for force calculations.
FRICTION: Friction factor applied to particle movement.
REPULSIVE_FORCE: Strength of repulsive force when particles are too close.
Particle Class
The Particle class represents individual particles in the simulation:


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
Spatial Partitioning
The spatial partitioning technique is used to optimize the force calculations between particles:

def spatial_partition(particles, cell_size):
    grid_size_x = (WIDTH // cell_size) + 1
    grid_size_y = (HEIGHT // cell_size) + 1
    grid = defaultdict(list)
    for particle in particles:
        cell = (int(particle.x // cell_size), int(particle.y // cell_size))
        grid[cell].append(particle)
    return grid, grid_size_x, grid_size_y


Acknowledgements
Inspired by various particle life simulations and the emergent behavior of interacting particles.

Contributing
Contributions are welcome! Please feel free to submit a Pull Request or open an issue to discuss changes.
