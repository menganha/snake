import pygame
import sys
from menu_screen import MenuScreen
from game_screen import GameScreen
import config


class Game:
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption('S N A K E')
        pygame.mouse.set_visible(True)
        self.snakeSpeed = config.SNAKE_SPEED
        self.display = pygame.display.set_mode((config.DIS_WIDTH, config.DIS_HEIGHT))
        self.clock = pygame.time.Clock()
        self.menuScreen = MenuScreen()
        self.gameScreen = GameScreen()
        self.menuScreen.gameScene = self.gameScreen
        self.gameScreen.menuScene = self.menuScreen

    def game_loop(self):
        activeScene = self.menuScreen
        while activeScene:
            activeScene.render()
            activeScene.update(self.display)
            activeScene = activeScene.nextScene
            pygame.display.update()
            self.clock.tick(self.snakeSpeed)

        pygame.quit()
        sys.exit(0)


if __name__ == '__main__':
    game_app = Game()
    game_app.game_loop()
