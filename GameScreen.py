import pygame
import random
from Text import Text
from Controls import Controls
import config


class GameScreen():
    def __init__(self):
        self.textFont = pygame.font.SysFont(config.FONT, 13)
        self.game_over = False
        self.gameOverMsg = Text(self.textFont, "You Lost! Press C-Play Again or Q-Quit", config.WHITE)
        self.gameOverMsg.center()
        self.controls = Controls()
        self.x1 = round(config.DIS_WIDTH / 2)
        self.y1 = round(config.DIS_HEIGHT / 2)
        self.snake_list = []
        self.Length_of_snake = 1
        self.foodx = round(random.randrange(0, config.DIS_WIDTH - config.SNAKE_BLOCK_SIZE)/config.SNAKE_BLOCK_SIZE)*config.SNAKE_BLOCK_SIZE
        self.foody = round(random.randrange(0, config.DIS_HEIGHT - config.SNAKE_BLOCK_SIZE)/config.SNAKE_BLOCK_SIZE)*config.SNAKE_BLOCK_SIZE
        self.scoreText = Text(self.textFont, "Your Score: {:}".format(self.Length_of_snake-1), config.WHITE)
        self.eatSound = pygame.mixer.Sound("sounds/eat.wav")
        self.nextScene = self
        self.menuScene = None

    def update_score(self, display):
        self.scoreText.text = "Score: {:}".format((self.Length_of_snake-1)*10)
        self.scoreText.tX, self.scoreText.tY = (3, 3)
        self.scoreText.reRender()
        self.scoreText.update(display)

    def debug_output(self, strings, display):
        debugText = Text(self.textFont, strings, config.WHITE)
        debugText.center(offY=40)
        debugText.update(display)

    def update_snake(self, display):
        bodyColor = config.WHITE
        headColor = config.YELLOW
        for idx, x in enumerate(self.snake_list):
            if idx == len(self.snake_list)-1:
                color = headColor
            else:
                color = bodyColor
            pygame.draw.rect(
                display, color,
                [x[0], x[1], config.SNAKE_BLOCK_SIZE, config.SNAKE_BLOCK_SIZE]
            )

    def render(self):

        if self.game_over:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.nextScene = self.menuScene
                    if event.key == pygame.K_c:
                        self.game_over = False

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.nextScene = None

            self.controls.handleInput()

            if self.x1 >= config.DIS_WIDTH:
                self.x1 = 0
            elif self.x1 < 0:
                self.x1 = config.DIS_WIDTH - config.SNAKE_BLOCK_SIZE
            else:
                self.x1 += self.controls.x1_change

            if self.y1 >= config.DIS_HEIGHT:
                self.y1 = 0
            elif self.y1 < 0:
                self.y1 = config.DIS_HEIGHT - config.SNAKE_BLOCK_SIZE
            else:
                self.y1 += self.controls.y1_change

            self.snake_Head = []
            self.snake_Head.append(self.x1)
            self.snake_Head.append(self.y1)
            self.snake_list.append(self.snake_Head)
            if len(self.snake_list) > self.Length_of_snake:
                del self.snake_list[0]

            for bodyCoord in self.snake_list[:-1]:  # Checks if it eats itself
                if bodyCoord == self.snake_Head:
                    self.game_over = True

            if self.x1 == self.foodx and self.y1 == self.foody:
                self.eatSound.play()
                self.foodx = round(random.randrange(
                    0, config.DIS_WIDTH - config.SNAKE_BLOCK_SIZE) / 10.0) * 10
                self.foody = round(random.randrange(
                    0, config.DIS_HEIGHT - config.SNAKE_BLOCK_SIZE) / 10.0) * 10
                self.Length_of_snake += 1

    def update(self, display):
        if self.game_over:
            self.gameOverMsg.update(display)
        else:
            # Background
            display.fill(config.BLACK)
            #pygame.draw.rect(display, config.BLACK, [0, 0, config.DIS_WIDTH, 20])
            # Food
            pygame.draw.rect(
                display, config.GREEN,
                [self.foodx, self.foody, config.SNAKE_BLOCK_SIZE, config.SNAKE_BLOCK_SIZE]
                )
            # Snake
            self.update_snake(display)
            # Score
            self.update_score(display)
            # Debug
            # self.debug_output(
            #     "x1: {:}, x2: {:}, slist: {:}".format(self.x1, self.y1, self.snake_list),
            #     display)
