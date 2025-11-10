import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("Pacman")


Black = (0,0,0)
Yellow = (255,255,0)
Blue = (0,0,255)
White = (255,255,255)

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
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                Pacman_x -= pacman_speed
                if keys [pygame.K_RIGHT]:
                    Pacman_x += pacman_speed
                    if keys[pygame.K_UP]:
                        Pacman_y -= pacman_speed
                        if keys[pygame.K_DOWN]:
                            Pacman_y += pacman_speed
                            screen.fill(Black)

                            for row_idx, row in enumerate(Maze):
                                for col_idx, tile in enumerate(row):
                                    if tile == 1: 
                                        pygame.draw.rect(sceen, Blue, (col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE))

                                        pygame.draw.cicrle(screen, Yellow, (Pacman_x, Pacman_y), 20)
                                        pygame.display.flip()
                                        clock.tick(30)