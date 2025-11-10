import pygame
import sys

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("Pacman")

# Pacman properties
pacman_speed = 5
pacman_x = 0
pacman_y = 0

# Colors
Black = (0,0,0)
Yellow = (255,255,0)
Blue = (0,0,255)
White = (255,255,255)

# Maze layout (1 = wall, 0 = path)
Maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1]
]
TILE_SIZE = 50

clock = pygame.time.Clock()
# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    screen.fill(Black)
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        pacman_x -= pacman_speed
    if keys [pygame.K_RIGHT]:
        pacman_x += pacman_speed
    if keys[pygame.K_UP]:
        pacman_y -= pacman_speed
    if keys[pygame.K_DOWN]:
        pacman_y += pacman_speed
    
    for row_idx, row in enumerate(Maze):
        for col_idx, tile in enumerate(row):
            if tile == 1: 
                pygame.draw.rect(screen, Blue, (col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE))

                pygame.draw.circle(screen, Yellow, (pacman_x, pacman_y), 20)
                pygame.display.flip()
                clock.tick(30)