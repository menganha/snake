import pygame
from config import SNAKE_BLOCK_SIZE


class Controls():
    """
    This class handles the inputs translating them into gameplay related
    output
    """
    def __init__(self):
        self.x1_change = 0
        self.y1_change = 0
        self.pause = False

    def handleInput(self):
        keys = pygame.key.get_pressed()
        x1_change_old = self.x1_change
        y1_change_old = self.y1_change
        if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
            self.x1_change = -SNAKE_BLOCK_SIZE
            self.y1_change = -SNAKE_BLOCK_SIZE
        elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
            self.x1_change = -SNAKE_BLOCK_SIZE
            self.y1_change = SNAKE_BLOCK_SIZE
        elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            self.x1_change = SNAKE_BLOCK_SIZE
            self.y1_change = -SNAKE_BLOCK_SIZE
        elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
            self.x1_change = SNAKE_BLOCK_SIZE
            self.y1_change = SNAKE_BLOCK_SIZE
        elif keys[pygame.K_LEFT]:
            self.x1_change = -SNAKE_BLOCK_SIZE
            self.y1_change = 0
        elif keys[pygame.K_RIGHT]:
            self.x1_change = SNAKE_BLOCK_SIZE
            self.y1_change = 0
        elif keys[pygame.K_UP]:
            self.x1_change = 0
            self.y1_change = -SNAKE_BLOCK_SIZE
        elif keys[pygame.K_DOWN]:
            self.x1_change = 0
            self.y1_change = SNAKE_BLOCK_SIZE
        elif keys[pygame.K_ESCAPE]:
            self.pause = True

        if y1_change_old == -self.y1_change and x1_change_old == -self.x1_change:
            self.y1_change = y1_change_old
            self.x1_change = x1_change_old
