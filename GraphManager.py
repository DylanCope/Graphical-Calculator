import pygame, sys, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
from Locus import Locus
from InteractiveTextBox import InteractiveTextBox

class GraphManager:

    def __init__(self, width, height):
        self.graphs = []

        self.tMax = 10
        self.tMin = -10
        self.xMax = 10
        self.xMin = -10

        self.width = width
        self.height = height

        self.menuPosition = 0
        self.font = pygame.font.SysFont("Bebas Neue", 28)
        self.font2 = pygame.font.SysFont("Nueva Std",25)

    def addGraph(self, graph):
        self.graphs.append(graph)

    def showMenu(self):
        self.menuPosition = 0

    def render(self, screen, unit, centre, events):

        for g in self.graphs:
            g.pixelize(unit, centre)
            pygame.draw.aalines(
                screen,
                g.getColour(),
                False,
                g.getPointsOnScreen(),
                True)

        pygame.draw.rect(
            screen,
            (15, 15, 0),
            ((self.menuPosition, 0),
             (self.menuPosition + self.width, self.height))
        )

        pygame.draw.aaline(
            screen,
            (50, 50, 0),
            (self.menuPosition + self.width, self.height),
            (self.menuPosition + self.width, 0),
            True)

        title = self.font.render("Graphical Calculator", 1, (255, 255, 255))
        screen.blit(title, (self.width/2 - title.get_width()/2, 10))

        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                mousePos = event.pos

        for i, g in enumerate(self.graphs):
            R = int(100 * g.getColour()[0] / 255)
            G = int(100 * g.getColour()[1] / 255)
            B = int(100 * g.getColour()[2] / 255)

            bounds = ((15, 50 + 90*i),
                 (self.width - 30, 80))

            pygame.draw.rect(
                screen,
                (R, G, B),
                bounds)

            pygame.draw.rect(
                screen,
                (R*2, G*2, B*2),
                bounds,
                2)

            if g.getForm() == "parametric":

                display = g.getDisplay()[0]

                display.setPosition(
                    bounds[0][0] + 10,
                    bounds[0][1] + 20)
                display.setDimensions(
                    bounds[1][0] - 20,
                    40)

                display = g.getDisplay()[1]

                display.setPosition(
                    bounds[0][0] + 10,
                    bounds[0][1] + 50)
                display.setDimensions(
                    bounds[1][0] - 20,
                    40)

            elif g.getForm() == "cartesian":

                display = g.getDisplay()

                display.setPosition(
                    bounds[0][0] + 10,
                    bounds[0][1] + 20)
                display.setDimensions(
                    bounds[1][0] - 20,
                    40)

            g.updateDisplay(screen, events)
