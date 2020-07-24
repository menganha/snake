import pygame
from Text import Text
from Food import Food
from Controls import Controls
from math import ceil
from random import randint
import config
# TODO:
# * Improve game over screen. Possibly reuse the pause menu screen
# Bug fixes:
# * Big Food finite spawn should be paused both in pause screen and at the
#   beggining of the game where no key has been pressed
# * Using escape to exit the pause menu is not possible give the current
#   input handling. Change it so that it uses the event queue
# * Big food is positioned in place near the border of the screen
#   where part of it is clipped
# For Screen Shake: refactor all update functions to accept an offset which will
# create the shake


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
            (config.DIS_WIDTH, config.DIS_HEIGHT-self.scoreText.tH-self.textOffset[1])
            )
        self.foodBig = Food(
            (config.DIS_WIDTH, config.DIS_HEIGHT-self.scoreText.tH-self.textOffset[1]),
            3, self.spawnTime, 0.5
            )
        self.foodBig.turnIdle()
        self.cursorPos = 0
        self.eatSound = pygame.mixer.Sound("sounds/eat.wav")
        self.selectSound = pygame.mixer.Sound("sounds/select.wav")
        self.nextScene = self
        self.screen_shake = 0
        self.menuScene = None
        self.createPauseMenu()

    def createPauseMenu(self):
        self.pauseMenuText = [
            Text(self.textFont, "P A U S E", config.WHITE),
            Text(self.textFont, "Continue", config.WHITE),
            Text(self.textFont, "Exit", config.WHITE)]

        for idx, button in enumerate(self.pauseMenuText):
            button.center(offY=button.tH*2*(idx-1))
            if idx == 0:
                minX = button.tX
                minY = button.tY
                maxW = button.tW
                maxH = button.tH
            else:
                if button.tX < minX:
                    minX = button.tX
                if button.tY < minY:
                    minX = button.tX
                if button.tW > maxW:
                    maxW = button.tW
                if button.tY + button.tH > maxH:
                    maxH = button.tY + button.tH

        border = 10
        self.minX = minX - border
        self.minY = minY - border
        maxW = maxW + 2*border
        maxH = maxH - minY + 2*border
        self.menuSurface = pygame.Surface((maxW, maxH))
        self.menuSurface.fill(config.BLACK)
        self.menuSurface.set_alpha(100)

    def updatePauseMenu(self, display):
        display.blit(self.menuSurface, [self.minX, self.minY])
        for idx, button in enumerate(self.pauseMenuText):
            if idx == 0:
                button.alpha = 255
            elif idx - 1 == self.cursorPos:
                button.alpha = 255
            else:
                button.alpha = 125
            button.reRender()
            button.update(display)

    def reStart(self):
        self.Length_of_snake = 1
        self.snake_list = []
        self.x1 = round(config.DIS_WIDTH / 2)
        self.y1 = round(config.DIS_HEIGHT / 2)
        self.controls.stop()
        self.foodSmall.spawn()
        self.foodBig.spawn()

    def update_score(self, display):
        self.scoreText.text = "Score: {:}".format((self.Length_of_snake-1)*10)
        self.scoreText.reRender()
        self.scoreText.update(display)

    def debug_output(self, strings, display):
        debugText = Text(self.textFont, strings, config.WHITE)
        debugText.center(offY=40)
        debugText.update(display)

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

    def render(self):

        self.nextScene = self

        if self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.nextScene = self.menuScene
                    if event.key == pygame.K_c:
                        self.game_over = False
                        self.reStart()

        elif self.controls.pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.nextScene = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.cursorPos == 0:
                            self.controls.pause = False
                        elif self.cursorPos == 1:
                            self.controls.pause = False
                            self.cursorPos = 0
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

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.nextScene = None

            self.controls.handleInput()

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
                    self.foodBig.spawn(self.spawnTime)
                self.Length_of_snake += 1

            if self.foodBig.isEaten(self.x1, self.y1):
                self.eatSound.play()
                self.foodBig.turnIdle()
                self.Length_of_snake += 5
                self.screen_shake = 13

            if not self.foodBig.isIdle:
                self.foodBig.spawnTime -= 1

    def update(self, display):
        if self.game_over:
            self.gameOverMsg.update(display)
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
            # Food
            self.foodSmall.update(display, offset)
            self.foodBig.update(display, offset)
            # Score
            pygame.draw.rect(
                display, config.WHITE,
                [0, 0, config.DIS_WIDTH, self.scoreText.tH + self.textOffset[1]]
                )
            self.update_score(display)
            if self.controls.pause:
                self.updatePauseMenu(display)
            # Debug
            # self.debug_output(
            #     "x1: {:}, x2: {:}, slist: {:}".format(self.x1, self.y1, self.snake_list),
            #     display)
