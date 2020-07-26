"""
Class representing the in-game menus
"""
import pygame
from text import Text
import config


class Menu():

    def __init__(self, font, title, option1, option2, border=10, alpha=100):
        self.textFont = font
        self.border = border
        self.alpha = alpha
        self.minX = self.minY = self.maxW = self.maxH = 0
        self.menuText = [
            Text(self.textFont, *title),
            Text(self.textFont, *option1),
            Text(self.textFont, *option2)]
        self._get_rectange_parametes()
        self._set_menu_surface()

    def _get_rectange_parametes(self):
        '''
        Gets the parameter for positioning the menu items
        '''
        for idx, button in enumerate(self.menuText):
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

        self.minX = minX - self.border
        self.minY = minY - self.border
        self.maxW = maxW + 2*self.border
        self.maxH = maxH - self.minY + 2*self.border

    def _set_menu_surface(self):
        self.menuSurface = pygame.Surface((self.maxW, self.maxH))
        self.menuSurface.fill(config.BLACK)
        self.menuSurface.set_alpha(self.alpha)

    def update(self, display, cursor_pos):
        display.blit(self.menuSurface, [self.minX, self.minY])
        for idx, button in enumerate(self.menuText):
            if idx == 0:
                button.alpha = 255
            elif idx - 1 == cursor_pos:
                button.alpha = 255
            else:
                button.alpha = 125
            button.reRender()
            button.update(display)
