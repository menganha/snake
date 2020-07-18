import pygame
import random
import config


class Food():
    # TODO: introduce typing information to enforce alway an int in unitSize
    def __init__(self, unitSize=1, spawnTime=10):
        self.posX = round(random.randrange(0, config.DIS_WIDTH - config.SNAKE_BLOCK_SIZE)/config.SNAKE_BLOCK_SIZE)*config.SNAKE_BLOCK_SIZE
        self.posY = round(random.randrange(0, config.DIS_HEIGHT - config.SNAKE_BLOCK_SIZE)/config.SNAKE_BLOCK_SIZE)*config.SNAKE_BLOCK_SIZE
        self.unitSize = unitSize
        self.size = self.unitSize * config.SNAKE_BLOCK_SIZE
        self.isAvailable = True
        self.spawnTime = spawnTime
        self.counter = 0

    def spawn(self):
        self.posX = round(random.randrange(0, config.DIS_WIDTH - self.unitSize*config.SNAKE_BLOCK_SIZE)/config.SNAKE_BLOCK_SIZE)*config.SNAKE_BLOCK_SIZE
        self.posY = round(random.randrange(0, config.DIS_HEIGHT - self.unitSize*config.SNAKE_BLOCK_SIZE)/config.SNAKE_BLOCK_SIZE)*config.SNAKE_BLOCK_SIZE
        self.counter = 0

    def isIdle(self):
        return self.counter > self.spawnTime

    def turnIdle(self):
        self.posX = config.DIS_WIDTH
        self.posY = config.DIS_HEIGHT

    def isEaten(self, x, y):
        xMet = [x == self.posX+config.SNAKE_BLOCK_SIZE*idx for idx in range(self.unitSize)]
        yMet = [y == self.posY+config.SNAKE_BLOCK_SIZE*idx for idx in range(self.unitSize)]
        if any(xMet) and any(yMet):
            return True
        else:
            return False

    def update(self, display):
        if self.counter < self.spawnTime:
            pygame.draw.rect(display, config.GREEN, [self.posX, self.posY, self.size, self.size])
        else:
            self.turnIdle()
