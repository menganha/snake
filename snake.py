import pygame
import config
from math import ceil


class Snake():

    def __init__(self):
        self.x1 = round(config.DIS_WIDTH / 2)
        self.y1 = round(config.DIS_HEIGHT / 2)
        self.snake_list = []
        self.snake_length = 1
        self.snake_list
        pass

    def move(self, x1_change, y1_change, y_offset):
        self.x1 += x1_change
        if self.x1 >= config.DIS_WIDTH:
            self.x1 = 0
        elif self.x1 < 0:
            self.x1 = config.DIS_WIDTH - config.SNAKE_BLOCK_SIZE

        self.y1 += y1_change
        if self.y1 >= config.DIS_HEIGHT:
            self.y1 = ceil(y_offset/config.SNAKE_BLOCK_SIZE)*config.SNAKE_BLOCK_SIZE
        elif self.y1 < y_offset:
            self.y1 = config.DIS_HEIGHT - config.SNAKE_BLOCK_SIZE

    def render(self):
        snake_head = [self.x1, self.y1]
        self.snake_list.append(snake_head)
        if len(self.snake_list) > self.snake_length:
            del self.snake_list[0]

    def eats_itself(self):
        snake_head = self.snake_list[-1]
        for bodyCoord in self.snake_list[:-1]:
            if bodyCoord == snake_head:
                return True
        return False

    def update(self, display, offset=[0, 0]):
        bodyColor = config.WHITE
        headColor = config.YELLOW
        for idx, x in enumerate(self.snake_list):
            if idx == len(self.snake_list)-1:
                color = headColor
            else:
                color = bodyColor
            pygame.draw.rect(
                display, color,
                [x[0]+offset[0], x[1]+offset[1], config.SNAKE_BLOCK_SIZE, config.SNAKE_BLOCK_SIZE]
            )