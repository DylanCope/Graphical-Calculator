import pygame, sys, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

class InteractiveTextBox:

    def __init__(self, tag, eqn = "", colour=(0,0,0)):
        self.tag = tag
        self.colour = colour
        self.characters = eqn
        self.position = (0, 0)
        self.dimensions = (0, 0)
        self.isSelected = False
        self.font = pygame.font.SysFont("Bebas Neue", 28)
        self.compute = False
        self.shiftNextChr = False

    def getString(self):
        return string.join(self.characters, "")

    def computeLocus(self):
        return self.compute

    def setPosition(self, x, y):
        self.position = (x, y)

    def setDimensions(self, width, height):
        self.dimensions = (width, height)

    def update(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                (x, y) = self.position
                (w, h) = self.dimensions
                (xm, ym) = event.pos
                withinXBound = x < xm and xm < x + w
                withinYBound = y < ym and ym < y + h
                self.isSelected = withinXBound and withinYBound

            if event.type == KEYDOWN and self.isSelected:
                inKey = event.key

                if inKey == K_BACKSPACE and len(self.characters) > 0:
                    self.characters = self.characters[0:-1]
                elif inKey == K_RETURN:
                    self.compute = True
                    self.isSelected = False
                elif inKey == K_LSHIFT or inKey == K_RSHIFT:
                    self.shiftNextChr = True
                elif self.shiftNextChr:
                    if inKey == K_0:
                        self.characters += ')'
                    elif inKey == K_9:
                        self.characters += '('
                    elif inKey == K_8:
                        self.characters += '*'
                    elif inKey == K_6:
                        self.characters += '^'
                    elif inKey == K_5:
                        self.characters += '%'
                    elif inKey == K_PLUS:
                        self.characters += '+'
                    elif inKey == K_MINUS:
                        self.characters += '-'
                    self.shiftNextChr = False
                elif inKey <= 127:
                    self.characters += chr(inKey)

    def render(self, screen):

        (x, y) = self.position
        (w, h) = self.dimensions

        if self.isSelected:
            (r, g, b) = self.colour
            bound = lambda x : x if x < 256 else 255
            f = lambda x : bound(3*int(100*x / 255))
            colour = (f(r), f(g), f(b))

            pygame.draw.rect(
                screen,
                colour,
                ((x - 5, y - h/4), (x + w - 15, 30))
            )

        text = self.font.render(self.tag + self.characters, 1, (255, 255, 255))
        screen.blit(text, (x, y - h/4))
