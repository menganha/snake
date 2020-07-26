import pygame
import random
import config
from math import ceil


class Food():
    # TODO: introduce typing information to enforce alway an int in unitSize
    def __init__(self, screen_size, unit_size=1, spawn_time=0, prob=1.1, color=config.GREEN, blink_rate=0):
        self.screenSize = screen_size
        self.posX = round(random.randrange(0, self.screenSize[0] - config.SNAKE_BLOCK_SIZE)/config.SNAKE_BLOCK_SIZE) \
            * config.SNAKE_BLOCK_SIZE
        self.posY = round(random.randrange(0, self.screenSize[1] - config.SNAKE_BLOCK_SIZE)/config.SNAKE_BLOCK_SIZE) \
            * config.SNAKE_BLOCK_SIZE \
            + ceil((config.DIS_HEIGHT - self.screenSize[1])/config.SNAKE_BLOCK_SIZE)*config.SNAKE_BLOCK_SIZE
        self.unitSize = unit_size
        self.size = self.unitSize * config.SNAKE_BLOCK_SIZE
        self.isAvailable = True
        self.spawnTime = spawn_time
        self.spawnCounter = 0
        self.prob = prob
        self.color = color
        self.blinkRate = blink_rate
        self.blinkCounter = 0
        self.isIdle = False

    def spawn(self):
        if random.randrange(1, 10)/10 <= self.prob:
            self.posX = round(random.randrange(0, self.screenSize[0] - self.unitSize*config.SNAKE_BLOCK_SIZE)/config.SNAKE_BLOCK_SIZE) \
                * config.SNAKE_BLOCK_SIZE
            self.posY = round(random.randrange(0, self.screenSize[1] - self.unitSize*config.SNAKE_BLOCK_SIZE)/config.SNAKE_BLOCK_SIZE) \
                * config.SNAKE_BLOCK_SIZE \
                + ceil((config.DIS_HEIGHT - self.screenSize[1])/config.SNAKE_BLOCK_SIZE)*config.SNAKE_BLOCK_SIZE
            self.spawnCounter = self.spawnTime
            self.isIdle = False

    def turn_idle(self):
        self.posX = config.DIS_WIDTH
        self.posY = config.DIS_HEIGHT
        self.isIdle = True

    def is_eaten(self, x, y):
        xMet = [x == self.posX+config.SNAKE_BLOCK_SIZE*idx for idx in range(self.unitSize)]
        yMet = [y == self.posY+config.SNAKE_BLOCK_SIZE*idx for idx in range(self.unitSize)]
        if any(xMet) and any(yMet):
            return True
        else:
            return False

    def blink(self, color1, color2=config.WHITE):
        '''
        Returns color based on time
        '''
        color = color1
        if self.blinkCounter > self.blinkRate and self.blinkCounter <= 2*self.blinkRate:
            self.blinkCounter -= 1
        elif self.blinkCounter <= self.blinkRate and self.blinkCounter > 0:
            color = color2
            self.blinkCounter -= 1

        if self.blinkCounter == 0:
            self.blinkCounter = 2*self.blinkRate

        return color

    def update(self, display, offset):

        if self.spawnCounter >= 0:

            color = self.color

            if self.blinkRate > 0:
                color = self.blink(self.color)
                #barColor = self.blink(config.GREEN)
            barColor = config.GREY
            if self.spawnTime > 0:
                if not self.isIdle:
                    pygame.draw.rect(
                        display, barColor,
                        [config.DIS_WIDTH-3, 3, -3*self.spawnCounter, 12])
                self.spawnCounter -= 1

            pygame.draw.rect(
                display, color,
                [self.posX+offset[0], self.posY+offset[1], self.size, self.size])

        elif not self.isIdle:
            self.turn_idle()
