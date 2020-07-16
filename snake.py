import pygame
import yaml
import sys
import random
from Controls import Controls
from Text import Text
import config as cnfg


class Game:
    def __init__(self, config):
        pygame.init()
        pygame.display.set_caption('Snake and Jerry')
        pygame.mouse.set_visible(True)
        self.colors = config['colors']
        self.dim = config['disSize']
        self.snakeBlockSize = config['gameOpt']['snakeBlockSize']
        self.snakeSpeed = config['gameOpt']['snakeSpeed']
        self.display = pygame.display.set_mode((cnfg.DIS_WIDTH, cnfg.DIS_HEIGHT))
        self.font_style = pygame.font.SysFont(config['font']['default'], 13)
        self.score_font = pygame.font.SysFont(config['font']['score'], 13)
        self.clock = pygame.time.Clock()
        self.controls = Controls()
        self.inMenu = True

    def your_score(self, score):
        value = self.score_font.render("Your Score: {:}".format(score), True, self.colors['white'])
        self.display.blit(value, [3, 3])

    def our_snake(self, snake_block, snake_list):
        bodyColor = cnfg.WHITE
        headColor = cnfg.YELLOW
        for idx, x in enumerate(snake_list):
            if idx == len(snake_list)-1:
                color = headColor
            else:
                color = bodyColor
            pygame.draw.rect(
                self.display, color,
                [x[0], x[1], snake_block, snake_block]
            )

    def message(self, msg, color, background=None):
        mesg = self.font_style.render(msg, True, color, background)
        mW, mH = mesg.get_size()
        cX, cY = self.get_coordinates_to_center(mW, mH, self.dim['width'], self.dim['height'])
        self.display.blit(mesg, [cX, cY])

    def menuScreen(self):
        # Initialization
        playButton = Text(self.font_style, "Play Game", cnfg.WHITE, cnfg.RED)
        playButton.center()
        while self.inMenu:
            # Logic
            self.controls.handleInput()
            if playButton.isMousein(self.controls.mx, self.controls.my):
                playButton.reRender(cnfg.GREEN, cnfg.RED)
            else:
                playButton.reRender()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.gameLoop()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

            # Render
            self.display.fill(cnfg.BLACK)
            playButton.update(self.display)
            pygame.display.update()


    def gameLoop(self):
        game_exit = False
        game_over = False

        gameOverMsg = Text(self.font_style, "You Lost! Press C-Play Again or Q-Quite", cnfg.WHITE)
        gameOverMsg.center()

        x1 = round(self.dim['width'] / 2)
        y1 = round(self.dim['height'] / 2)

        snake_List = []
        Length_of_snake = 1

        foodx = round(random.randrange(0, self.dim['width'] - cnfg.SNAKE_BLOCK_SIZE)/cnfg.SNAKE_BLOCK_SIZE)*cnfg.SNAKE_BLOCK_SIZE
        foody = round(random.randrange(0, self.dim['height'] - cnfg.SNAKE_BLOCK_SIZE)/cnfg.SNAKE_BLOCK_SIZE)*cnfg.SNAKE_BLOCK_SIZE

        while not game_exit:

            while game_over:
                #self.display.fill(self.colors['blue'])
                self.your_score(Length_of_snake - 1)
                gameOverMsg.update(self.display)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_exit = True
                            game_over = False
                        if event.key == pygame.K_c:
                            self.gameLoop()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    game_exit = True

            self.controls.handleInput()

            if x1 >= self.dim['width']:
                x1 = 0
            elif x1 < 0:
                x1 = self.dim['width'] - self.snakeBlockSize
            else:
                x1 += self.controls.x1_change

            if y1 >= self.dim['height']:
                y1 = 0
            elif y1 < 0:
                y1 = self.dim['height'] - self.snakeBlockSize
            else:
                y1 += self.controls.y1_change

            self.display.fill(cnfg.GREY)
            pygame.draw.rect(self.display, cnfg.BLACK, [0, 0, cnfg.DIS_WIDTH, 20])

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

            for x in snake_List[:-1]:  # Checks if it eats itself
                if x == snake_Head:
                    game_over = True

            self.our_snake(self.snakeBlockSize, snake_List)
            self.your_score(Length_of_snake - 1)

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
    gameApp.menuScreen()
