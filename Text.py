import pygame
from config import DIS_WIDTH, DIS_HEIGHT


class Text():
    def __init__(self, font: pygame.font.Font, text, color, background=None):
        self.font = font
        self.text = text
        self.color = color
        self.background = background
        self.textS = self.font.render(self.text, True, color, background)
        self.tW, self.tH = self.textS.get_size()
        self.tX = 0
        self.tY = 0

    def center(self):
        self.tX, self.tY = self.get_coordinates_to_center(
            self.tW, self.tH, DIS_WIDTH, DIS_HEIGHT
            )

    def reRender(self, color=None, background=None):
        if not color:
            color = self.color
        if not background:
            background = self.background
        self.textS = self.font.render(self.text, True, color, background)

    def isMousein(self, mx, my):
        textR = self.textS.get_rect(x=self.tX, y=self.tY)
        return textR.collidepoint(mx, my)

    def update(self, display: pygame.Surface):
        display.blit(self.textS, [self.tX, self.tY])

    @staticmethod
    def get_coordinates_to_center(objWidth, objHeight, disWidth, disHeight):
        centerX = round(disWidth/2 - objWidth/2)
        centerY = round(disHeight/2 - objHeight/2)
        return centerX, centerY

