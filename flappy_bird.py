import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
bird_x = 50
bird_y = HEIGHT // 2
bird_radius = 15
bird_velocity = 0
gravity = 0.25
jump_strength = -4.5

pipes = []
pipe_gap = 200
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks()

score = 0
font = pygame.font.Font(None, 36)

# Functions
def draw_bird(x, y):
    pygame.draw.circle(WIN, BLACK, (x, y), bird_radius)

def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(WIN, BLACK, pipe)

def move_pipes():
    for pipe in pipes:
        pipe.x -= 1
    pipes[:] = [pipe for pipe in pipes if pipe.x > -50]

def generate_pipes():
    top_pipe_height = random.randint(50, 300)
    bottom_pipe_height = HEIGHT - top_pipe_height - pipe_gap
    top_pipe = pygame.Rect(WIDTH, 0, 50, top_pipe_height)
    bottom_pipe = pygame.Rect(WIDTH, HEIGHT - bottom_pipe_height, 50, bottom_pipe_height)
    pipes.extend([top_pipe, bottom_pipe])

def check_collision():
    for pipe in pipes:
        if pipe.colliderect(pygame.Rect(bird_x - bird_radius, bird_y - bird_radius, 2 * bird_radius, 2 * bird_radius)):
            return True
    if bird_y - bird_radius <= 0 or bird_y + bird_radius >= HEIGHT:
        return True
    return False

def update_score():
    global score
    for pipe in pipes:
        if pipe.x == bird_x:
            score += 1

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    WIN.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump_strength

    bird_velocity += gravity
    bird_y += bird_velocity

    if pygame.time.get_ticks() - last_pipe > pipe_frequency:
        generate_pipes()
        last_pipe = pygame.time.get_ticks()

    move_pipes()
    update_score()

    draw_pipes()
    draw_bird(bird_x, int(bird_y))

    if check_collision():
        running = False

    text = font.render(f"Score: {score}", True, BLACK)
    WIN.blit(text, (10, 10))

    pygame.display.update()

pygame.quit()
sys.exit()
