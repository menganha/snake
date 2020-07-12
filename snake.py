import pygame
import yaml
import sys
import random


class Game:
    def __init__(self, config):
        pygame.init()
        pygame.display.set_caption('Snake Game by Edureka')
        self.colors = config['colors']
        self.dim = config['disSize']
        self.snakeBlockSize = config['gameOpt']['snakeBlockSize']
        self.snakeSpeed = config['gameOpt']['snakeSpeed']
        self.display = pygame.display.set_mode((self.dim['width'], self.dim['height']))
        self.font_style = pygame.font.SysFont(config['font']['default'], 25)
        self.score_font = pygame.font.SysFont(config['font']['score'], 35)
        self.clock = pygame.time.Clock()

    def debug_display(self, x, y):
        value = self.font_style.render("x: {:}, y: {:}".format(x, y), True, self.colors['white'])
        self.display.blit(value, [0, self.dim['height']-20])

    def your_score(self, score):
        value = self.score_font.render("Your Score: " + str(score), True, self.colors['yellow'])
        self.display.blit(value, [0, 0])

    def our_snake(self, snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(
                self.display, self.colors['black'],
                [x[0], x[1], snake_block, snake_block]
            )

    def message(self, msg, color):
        mesg = self.font_style.render(msg, True, color)
        self.display.blit(mesg, [self.dim['width'] // 6, self.dim['height'] // 3])

    def gameLoop(self):
        game_over = False
        game_close = False

        x1 = round(self.dim['width'] / 2)
        y1 = round(self.dim['height'] / 2)

        x1_change = 0
        y1_change = 0

        snake_List = []
        Length_of_snake = 1

        foodx = int(round(random.randrange(0, self.dim['width'] - self.snakeBlockSize) / 10.0) * 10.0)
        foody = int(round(random.randrange(0, self.dim['height'] - self.snakeBlockSize) / 10.0) * 10.0)

        while not game_over:

            while game_close:
                self.display.fill(self.colors['blue'])
                self.message("You Lost! Press C-Play Again or Q-Quit", self.colors['red'])
                self.your_score(Length_of_snake - 1)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            self.gameLoop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x1_change = -self.snakeBlockSize
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = self.snakeBlockSize
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -self.snakeBlockSize
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = self.snakeBlockSize
                        x1_change = 0

            #if x1 >= self.dim['width'] or x1 < 0 or y1 >= self.dim['height'] or y1 < 0:
                #game_close = True
            if x1 >= self.dim['width']:
                x1 = 0
            elif x1 < 0:
                x1 = self.dim['width'] - self.snakeBlockSize
            else:
                x1 += x1_change

            if y1 >= self.dim['height']:
                y1 = 0
            elif y1 < 0:
                y1 = self.dim['height'] - self.snakeBlockSize
            else:
                y1 += y1_change

            self.display.fill(self.colors['blue'])
            pygame.draw.rect(
                self.display, self.colors['green'],
                [foodx, foody, self.snakeBlockSize, self.snakeBlockSize]
                )
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True

            self.our_snake(self.snakeBlockSize, snake_List)
            self.your_score(Length_of_snake - 1)
            self.debug_display(x1, y1)

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(
                    0, self.dim['width'] - self.snakeBlockSize) / 10.0) * 10
                foody = round(random.randrange(
                    0, self.dim['height'] - self.snakeBlockSize) / 10.0) * 10
                Length_of_snake += 1

            self.clock.tick(self.snakeSpeed)

        pygame.quit()
        sys.exit(0)


if __name__ == '__main__':
    config = yaml.load(open("./config.yaml"), Loader=yaml.CLoader)
    gameApp = Game(config)
    gameApp.gameLoop()
