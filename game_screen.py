import pygame
from text import Text
from food import Food
from menu import Menu
from snake import Snake
from controls import Controls
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
        self.snake = Snake()
        self.controls = Controls()
        self.textFont = pygame.font.Font(config.FONT, 13)
        self.game_over = False
        self.textOffset = (3, 3)
        self.scoreText = Text(
            self.textFont,
            "Your Score: {:}".format(self.snake.snake_length-1),
            config.BLACK, tX=self.textOffset[0], tY=self.textOffset[0]
            )
        self.spawnTime = 50  # In frames
        self.foodSmall = Food(
            (config.DIS_WIDTH, config.DIS_HEIGHT-self.scoreText.tH-self.textOffset[1]),
            2
            )
        self.foodBig = Food(
            (config.DIS_WIDTH, config.DIS_HEIGHT-self.scoreText.tH-self.textOffset[1]),
            3, self.spawnTime, 0.5, config.GREEN, blink_rate=2
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
            ('Retry', config.WHITE),
            ('Exit', config.WHITE))

    def restart(self):
        self.snake.snake_length = 1
        self.snake.snake_list = []
        self.snake.x1 = round(config.DIS_WIDTH / 2)
        self.snake.y1 = round(config.DIS_HEIGHT / 2)
        self.controls.stop()
        self.screen_shake = 0
        self.foodSmall.spawn()
        self.foodBig.spawn()

    def update_score(self, display):
        self.scoreText.text = "Score: {:}".format((self.snake.snake_length-1)*10)
        self.scoreText.reRender()
        self.scoreText.update(display)

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

            self.snake.move(
                self.controls.x1_change,
                self.controls.y1_change,
                self.scoreText.tH + self.textOffset[1]
                )

            self.snake.render()

            if self.snake.eats_itself():
                self.game_over = True

            if self.foodSmall.is_eaten(self.snake.x1, self.snake.y1):
                self.eatSound.play()
                self.foodSmall.spawn()
                if self.foodBig.isIdle:
                    self.foodBig.spawn()
                self.snake.snake_length += 2

            if self.foodBig.is_eaten(self.snake.x1, self.snake.y1):
                self.eatBigSound.play()
                self.foodBig.turn_idle()
                self.snake.snake_length += 6
                self.screen_shake = 13

    def update(self, display):
        offset = [0, 0]
        if self.screen_shake:
            offset[0] = randint(0, 14) - 7
            offset[1] = randint(0, 14) - 7
            self.screen_shake -= 1
        # Background
        display.fill(config.BLACK)
        # Snake
        self.snake.update(display, offset)
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
        elif self.game_over:
            self.gameOverMenu.update(display, self.cursorPos)
