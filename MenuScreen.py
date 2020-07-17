import pygame
from Text import Text
from Controls import Controls
import config


class MenuScreen():
    def __init__(self):
        titleFont = pygame.font.SysFont(config.FONT, 28)
        textFont = pygame.font.SysFont(config.FONT, 15)
        self.title = Text(titleFont, "S N A K E", config.WHITE)
        self.title.center(offY=-3*self.title.tH)
        self.playButton = Text(textFont, "Play Game", config.WHITE)
        self.playButton.center()
        self.scoreButton = Text(textFont, "High Scores", config.WHITE)
        self.scoreButton.center(offY=2*self.playButton.tH)
        self.creditsButton = Text(textFont, "Credits", config.WHITE)
        self.creditsButton.center(offY=4*self.playButton.tH)
        self.exitButton = Text(textFont, "Exit", config.WHITE)
        self.exitButton.center(offY=6*self.playButton.tH)
        self.gameScene = None
        self.nextScene = self
        self.soundMove = pygame.mixer.Sound("sounds/select.wav")
        self.soundSelect = pygame.mixer.Sound("sounds/start.wav")
        self.cursorPos = 0

    def render(self):
        # Event Handling
        startGame = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.cursorPos == 0:
                        self.soundSelect.play()
                        startGame = True
                    elif self.cursorPos == 1:
                        self.soundSelect.play()
                    elif self.cursorPos == 3:
                        self.nextScene = None
                if event.key == pygame.K_DOWN:
                    self.soundMove.play()
                    if not self.cursorPos >= 3:
                        self.cursorPos += 1
                if event.key == pygame.K_UP:
                    self.soundMove.play()
                    if not self.cursorPos <= 0:
                        self.cursorPos -= 1
            if event.type == pygame.QUIT:
                self.nextScene = None

        # Logic
        alphaVector = [100 if idx == self.cursorPos else 250 for idx in range(4)]
        self.playButton.alpha = alphaVector[0]
        self.scoreButton.alpha = alphaVector[1]
        self.creditsButton.alpha = alphaVector[2]
        self.exitButton.alpha = alphaVector[3]
        self.playButton.reRender()
        self.scoreButton.reRender()
        self.creditsButton.reRender()
        self.exitButton.reRender()
        if startGame:
            self.nextScene = self.gameScene

    def update(self, display):
        display.fill(config.BLACK)
        self.playButton.update(display)
        self.scoreButton.update(display)
        self.creditsButton.update(display)
        self.exitButton.update(display)
        self.title.update(display)
