import pygame
from text import Text
from food import Food
from menu import Menu
from controls import Controls
from math import ceil
from random import randint
import config
# TODO:
# * Improve game over screen. Possibly reuse the pause menu screen
# Bug fixes:
# * Using escape to exit the pause menu is not possible give the current
#   input handling. Change it so that it uses the event queue
# * Big food is positioned in place near the border of the screen
#   where part of it is clipped
# * Create the snake class


class GameScreen():
    def __init__(self):
        self.textFont = pygame.font.Font(config.FONT, 13)
        self.game_over = False
        self.gameOverMsg = Text(
            self.textFont, "You Lost! Press C-Play Again or Q-Quit",
            config.YELLOW
            )
        self.gameOverMsg.center()
        self.controls = Controls()
        self.x1 = round(config.DIS_WIDTH / 2)
        self.y1 = round(config.DIS_HEIGHT / 2)
        self.snake_list = []
        self.Length_of_snake = 1
        self.textOffset = (3, 3)
        self.scoreText = Text(
            self.textFont,
            "Your Score: {:}".format(self.Length_of_snake-1),
            config.BLACK, tX=self.textOffset[0], tY=self.textOffset[0]
            )
        self.spawnTime = 50  # In frames
        self.foodSmall = Food(
            (config.DIS_WIDTH, config.DIS_HEIGHT-self.scoreText.tH-self.textOffset[1]),
            2
            )
        self.foodBig = Food(
            (config.DIS_WIDTH, config.DIS_HEIGHT-self.scoreText.tH-self.textOffset[1]),
            3, self.spawnTime, 0.5, config.GREEN, blinkRate=2
            )
        self.foodBig.turn_idle()
        self.cursorPos = 0
        self.eatSound = pygame.mixer.Sound("sounds/eat.wav")
        self.eatBigSound = pygame.mixer.Sound("sounds/eatBig_2.wav")
        self.selectSound = pygame.mixer.Sound("sounds/select.wav")
        self.nextScene = self
        self.screen_shake = 0
        self.menuScene = None
        self.pauseMenu = Menu(
            self.textFont,
            ('P A U S E', config.WHITE),
            ('Continue', config.WHITE),
            ('Exit', config.WHITE))
        self.gameOverMenu = Menu(
            self.textFont,
            ('G A M E   O V E R', config.RED),
            ('New Game', config.WHITE),
            ('Exit', config.WHITE))

    def restart(self):
        self.Length_of_snake = 1
        self.snake_list = []
        self.x1 = round(config.DIS_WIDTH / 2)
        self.y1 = round(config.DIS_HEIGHT / 2)
        self.controls.stop()
        self.screen_shake = 0
        self.foodSmall.spawn()
        self.foodBig.spawn()

    def update_score(self, display):
        self.scoreText.text = "Score: {:}".format((self.Length_of_snake-1)*10)
        self.scoreText.reRender()
        self.scoreText.update(display)

    def update_snake(self, display, offset=[0, 0]):
        bodyColor = config.WHITE
        headColor = config.YELLOW
        for idx, x in enumerate(self.snake_list):
            if idx == len(self.snake_list)-1:
                color = headColor
            else:
                color = bodyColor
            pygame.draw.rect(
                display, color,
                [
                    x[0]+offset[0], x[1]+offset[1],
                    config.SNAKE_BLOCK_SIZE, config.SNAKE_BLOCK_SIZE
                    ]
            )

    def _handle_menu_controls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.nextScene = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.cursorPos == 0:
                        if self.controls.pause:
                            self.controls.pause = False
                        elif self.game_over:
                            self.game_over = False
                            self.restart()
                    elif self.cursorPos == 1:
                        self.cursorPos = 0
                        self.controls.pause = False
                        self.game_over = False
                        self.nextScene = self.menuScene
                if event.key == pygame.K_DOWN:
                    if not self.cursorPos >= 1:
                        self.selectSound.play()
                        self.cursorPos += 1
                if event.key == pygame.K_UP:
                    if not self.cursorPos <= 0:
                        self.selectSound.play()
                        self.cursorPos -= 1
                if event.key == pygame.K_ESCAPE:
                    self.controls.pause = False

    def render(self):

        self.nextScene = self

        if self.controls.pause or self.game_over:
            self._handle_menu_controls()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.nextScene = None

            self.controls.handle_input()

            self.x1 += self.controls.x1_change
            if self.x1 >= config.DIS_WIDTH:
                self.x1 = 0
            elif self.x1 < 0:
                self.x1 = config.DIS_WIDTH - config.SNAKE_BLOCK_SIZE

            self.y1 += self.controls.y1_change
            if self.y1 >= config.DIS_HEIGHT:
                self.y1 = ceil((self.scoreText.tH + self.textOffset[1])/config.SNAKE_BLOCK_SIZE)*config.SNAKE_BLOCK_SIZE
            elif self.y1 < self.scoreText.tH + self.textOffset[1]:
                self.y1 = config.DIS_HEIGHT - config.SNAKE_BLOCK_SIZE

            self.snake_Head = []
            self.snake_Head.append(self.x1)
            self.snake_Head.append(self.y1)
            self.snake_list.append(self.snake_Head)
            if len(self.snake_list) > self.Length_of_snake:
                del self.snake_list[0]

            for bodyCoord in self.snake_list[:-1]:  # Checks if it eats itself
                if bodyCoord == self.snake_Head:
                    self.game_over = True

            if self.foodSmall.isEaten(self.x1, self.y1):
                self.eatSound.play()
                self.foodSmall.spawn()
                if self.foodBig.isIdle:
                    self.foodBig.spawn()
                self.Length_of_snake += 1

            if self.foodBig.isEaten(self.x1, self.y1):
                self.eatBigSound.play()
                self.foodBig.turn_idle()
                self.Length_of_snake += 5
                self.screen_shake = 13

    def update(self, display):
        if self.game_over:
            #self.gameOverMsg.update(display)
            self.gameOverMenu.update(display, self.cursorPos)
        else:
            offset = [0, 0]
            if self.screen_shake:
                offset[0] = randint(0, 14) - 7
                offset[1] = randint(0, 14) - 7
                self.screen_shake -= 1

            # Background
            display.fill(config.BLACK)
            # Snake
            self.update_snake(display, offset)
            # Score
            pygame.draw.rect(
                display, config.WHITE,
                [0, 0, config.DIS_WIDTH, self.scoreText.tH + self.textOffset[1]]
                )
            self.update_score(display)
            # Food
            self.foodSmall.update(display, offset)
            self.foodBig.update(display, offset)
            if self.controls.pause:
                self.pauseMenu.update(display, self.cursorPos)
