import math
import random
import pygame, sys, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
from Locus import Locus
from InteractiveTextBox import InteractiveTextBox
from GraphManager import GraphManager

pygame.init()

winw = 1280
winh = 720

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
ORANGE = (232, 92, 0)

screen = pygame.display.set_mode((winw, winh), pygame.FULLSCREEN, 32)
pygame.display.set_caption("Graphing Calculator (Mark II)")
fontLarge = pygame.font.SysFont("Bebas Neue", 28)
fontSmall = pygame.font.SysFont("Bebas Neue", 25)

pygame.display.set_icon(pygame.image.load('res/icon.png'))
pygame.display.toggle_fullscreen()

unit = 38
centre = (2*winw/3 + 16, winh/2)

curve = Locus(
    "parametric",
    ("sin(t)*(e^(cos(t))-2*cos(4*t)-sin(t/12)^5)",
     "cos(t)*(e^(cos(t))-2*cos(4*t)-sin(t/12)^5)"),
    GREEN)
curve.calculate(-10, 10, 0.01)
# curve.pixelize(unit, centre)
# print(curve.adjustedPoints)

curve2 = Locus(
    "parametric",
    ("11*cos(t)-6*cos(11*t/6)", "11*sin(t)-6*sin(11*t/6)"),
    ORANGE)
curve2.calculate(0, 40, 0.01)

curve3 = Locus(
    "parametric",
    ("7*cos(t)-2*cos(7*t/2)", "7*sin(t)-2*sin(7*t/2)/t"),
    PURPLE)
curve3.calculate(0, 40, 0.01)

curve4 = Locus(
    "cartesian",
    "x",
    RED
)
curve4.calculate(-40, 40, 0.01)

graphManager = GraphManager(winw / 3, winh)
graphManager.addGraph(curve)
graphManager.addGraph(curve2)
graphManager.addGraph(curve3)
# graphManager.addGraph(curve4)

running = True
clock = pygame.time.Clock()

def drawGrid(centre, spacing, colour):
    for i in range(0, int(math.sqrt(winw*winh)/spacing)):

        pygame.draw.aaline(
            screen,
            colour,
            (0, centre[1] + i * spacing),
            (winw, centre[1] + i * spacing),
            True)

        pygame.draw.aaline(
            screen,
            colour,
            (0, centre[1] - i * spacing),
            (winw, centre[1] - i * spacing),
            True)

        pygame.draw.aaline(
            screen,
            colour,
            (centre[0] + i * spacing, 0),
            (centre[0] + i * spacing, winh),
            True)
        pygame.draw.aaline(
            screen,
            colour,
            (centre[0] - i * spacing, 0),
            (centre[0] - i * spacing, winh),
            True)

def translateGrid(x, y, centre):
    Ox = centre[0]
    Ox += x
    Oy = centre[1]
    Oy += y
    centre = (Ox, Oy)
    return centre

while running:

    clock.tick(10)

    events = []

    (dx, dy) = pygame.mouse.get_rel()
    if pygame.mouse.get_pressed() == (True, False, False):
        centre = translateGrid(dx, dy, centre)

    for event in pygame.event.get():
        events.append(event)
        if event.type == QUIT:
            running = False

        if event.type == MOUSEBUTTONDOWN:
            mouseDownPos = event.pos
            if event.dict['button'] == 4:
                unit += 8
            if event.dict['button'] == 5 and unit > 10:
                unit -= 8

        if event.type == KEYDOWN:
            if event.key == K_UP:
                unit += 8
                # centre = translateGrid(0, 5, centre)
            elif event.key == K_DOWN:
                unit -= 8
                # centre = translateGrid(0, -5, centre)
            # elif event.key == K_LEFT:
            #     centre = translateGrid(5, 0, centre)
            # elif event.key == K_RIGHT:
            #     centre = translateGrid(-5, 0, centre)
            elif event.key == K_ESCAPE:
                running = False


    screen.fill((10, 10, 10))

    # Drawing grid:
    drawGrid(centre, unit/2, (20, 20, 0))
    drawGrid(centre, unit, (50, 50, 0))

    # Drawing main axis:
    pygame.draw.aaline(
        screen,
        (255, 255, 0),
        (0, centre[1]),
        (winw, centre[1]),
        True)
    pygame.draw.aaline(
        screen,
        (255, 255, 0),
        (centre[0], 0),
        (centre[0], winh),
        True)

    #Drawing loci:
    graphManager.render(screen, unit, centre, events)

    pygame.display.update()

pygame.quit()
sys.exit
