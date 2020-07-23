import pygame
import random
import config
from math import ceil


class Food():
    # TODO: introduce typing information to enforce alway an int in unitSize
    def __init__(self, playScreenSize, unitSize=1, spawnTime=0, prob=1.1):
        self.playScreenSize = playScreenSize
        self.posX = round(random.randrange(0, self.playScreenSize[0] - config.SNAKE_BLOCK_SIZE)/config.SNAKE_BLOCK_SIZE)*config.SNAKE_BLOCK_SIZE
        self.posY = round(random.randrange(0, self.playScreenSize[1] - config.SNAKE_BLOCK_SIZE)/config.SNAKE_BLOCK_SIZE)*config.SNAKE_BLOCK_SIZE \
            + ceil((config.DIS_HEIGHT - self.playScreenSize[1])/config.SNAKE_BLOCK_SIZE)*config.SNAKE_BLOCK_SIZE
        self.unitSize = unitSize
        self.size = self.unitSize * config.SNAKE_BLOCK_SIZE
        self.isAvailable = True
        self.spawnTime = spawnTime
        self.prob = prob
        self.isIdle = False

    def spawn(self, spawnTime=0):
        if random.randrange(1, 10)/10 <= self.prob:
            self.posX = round(random.randrange(0, self.playScreenSize[0] - self.unitSize*config.SNAKE_BLOCK_SIZE)/config.SNAKE_BLOCK_SIZE)*config.SNAKE_BLOCK_SIZE
            self.posY = round(random.randrange(0, self.playScreenSize[1] - self.unitSize*config.SNAKE_BLOCK_SIZE)/config.SNAKE_BLOCK_SIZE)*config.SNAKE_BLOCK_SIZE \
                + ceil((config.DIS_HEIGHT - self.playScreenSize[1])/config.SNAKE_BLOCK_SIZE)*config.SNAKE_BLOCK_SIZE
            self.spawnTime = spawnTime
            self.isIdle = False

    def turnIdle(self):
        self.posX = config.DIS_WIDTH
        self.posY = config.DIS_HEIGHT
        self.isIdle = True

    def isEaten(self, x, y):
        xMet = [x == self.posX+config.SNAKE_BLOCK_SIZE*idx for idx in range(self.unitSize)]
        yMet = [y == self.posY+config.SNAKE_BLOCK_SIZE*idx for idx in range(self.unitSize)]
        if any(xMet) and any(yMet):
            return True
        else:
            return False

    def update(self, display, offset):
        if self.spawnTime >= 0:
            pygame.draw.rect(
                display, config.GREEN,
                [self.posX+offset[0], self.posY+offset[1], self.size, self.size])
        elif not self.isIdle:
            self.turnIdle()
