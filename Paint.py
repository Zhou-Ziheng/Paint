# -----------------------------------------------------------------
# Name: Tony Zhou
# Date: June 11, 2021
# Class Code: ICS4U

# -----------------------------------------------------------------

import traceback
import pygame
import random
from pathlib import Path

def drawToolBar():
    pygame.draw.rect(screen, THEME, (0, 0, 50, 600))
    pygame.draw.rect(screen, LINE, (0, 0, 50, 600), 1)

    pygame.draw.rect(screen, THEME, (0, 0, 800, 20))
    pygame.draw.rect(screen, LINE, (0, 0, 800, 20), 1)

    pygame.draw.rect(screen, THEME, (0, 520, 800, 80))
    pygame.draw.rect(screen, LINE, (0, 520, 800, 80), 1)


def selectTool(mx, my, currentTool):
    global initialX, initialY, currentThickness
    if 10 < mx < 40:

        deltaY = my - 30
        if deltaY < 230 and deltaY % 40 < 30:
            initialX, initialY = None, None
            if int(deltaY / 40) == 4:
                currentThickness = 14
            return int(deltaY / 40)

        elif 300 < my < 333:
            if (currentTool < 2 or currentTool == 4) and currentThickness <= 1:
                currentThickness = 1
            elif (currentTool == 2 or currentTool == 3) and currentThickness <= 0:
                currentThickness = 0
            else:
                currentThickness -= 1
            return currentTool

        elif 367 < my < 400:
            currentThickness += 1
            return currentTool
        elif 500 > my > 470:
            pygame.draw.rect(screen, WHITE, (50, 20, 750, 500))
            return currentTool
        else:
            return currentTool
    else:
        return currentTool


def getHover(mx, my):
    if 10 < mx < 40:

        deltaY = my - 30
        if deltaY < 230 and deltaY % 40 < 30:
            return int(deltaY / 40)
        elif 300 < my < 333:
            return 97
        elif 367 < my < 400:
            return 98
        elif 500 > my > 470:
            return 99
        else:
            return None
    else:
        return None


def drawTool(currentTool, currentSize, currentHover):
    counter = 0
    for y in range(30, 260, 40):
        color = THEME
        if counter == currentTool:
            color = LINE
        elif counter == currentHover:
            color = HOVER
        pygame.draw.rect(screen, color, (10, y, 30, 30), 1)
        screen.blit(images[counter], (12, y + 2))
        counter += 1

    myFont = pygame.font.SysFont(None, 30)

    if currentSize == 0:
        currentSize = "FILL"
    else:
        currentSize = str(currentSize)
    textSurface = myFont.render(currentSize, False, (0, 0, 0))
    width = textSurface.get_width()
    extra = (50 - width) / 2
    screen.blit(textSurface, (extra, 342))

    minus = pygame.image.load("minus.png")
    minus = pygame.transform.scale(minus, (20, 20))
    screen.blit(minus, (15, 305))

    plus = pygame.image.load("plus.png")
    plus = pygame.transform.scale(plus, (20, 20))
    screen.blit(plus, (15, 372))

    color = THEME
    if currentHover == 97:
        color = HOVER
    pygame.draw.rect(screen, color, (10, 300, 30, 33), 1)

    color = THEME
    if currentHover == 98:
        color = HOVER
    pygame.draw.rect(screen, color, (10, 367, 30, 33), 1)

    if currentHover == 99:
        pygame.draw.rect(screen, HOVER, (10, 470, 30, 30), 1)
    else:
        pygame.draw.rect(screen, THEME, (10, 470, 30, 30), 1)
    screen.blit(getCorrectImage("clear.png"), (12, 472))


def drawColorPanel(currentColor):
    pygame.draw.rect(screen, currentColor, (10, 530, 60, 60))
    pygame.draw.rect(screen, LINE, (10, 530, 60, 60), 1)

    pygame.draw.rect(screen, THEME, (730, 540, 40, 40))
    pygame.draw.rect(screen, LINE, (730, 540, 40, 40), 1)
    image = pygame.image.load("dice.png")
    image = pygame.transform.scale(image, (30, 30))
    screen.blit(image, (735, 545))
    index = 0
    for i in range(80, 210, 30):
        for j in range(530, 570, 35):
            pygame.draw.rect(screen, color[index], (i, j, 25, 25))
            pygame.draw.rect(screen, LINE, (i, j, 25, 25), 1)
            index += 1
    posx = 250
    colorRGB = [255, 0, 0]
    while colorRGB[1] < 255:
        pygame.draw.rect(screen, (colorRGB[0], colorRGB[1], colorRGB[2]), (posx, 530, 1, 60))
        colorRGB[1] += 5
        posx += 1
    while colorRGB[0] > 0:
        pygame.draw.rect(screen, (colorRGB[0], colorRGB[1], colorRGB[2]), (posx, 530, 1, 60))
        colorRGB[0] -= 5
        posx += 1
    while colorRGB[2] < 255:
        pygame.draw.rect(screen, (colorRGB[0], colorRGB[1], colorRGB[2]), (posx, 530, 1, 60))
        colorRGB[2] += 5
        posx += 1
    while colorRGB[1] > 0:
        pygame.draw.rect(screen, (colorRGB[0], colorRGB[1], colorRGB[2]), (posx, 530, 1, 60))
        colorRGB[1] -= 5
        posx += 1
    while colorRGB[0] < 255:
        pygame.draw.rect(screen, (colorRGB[0], colorRGB[1], colorRGB[2]), (posx, 530, 1, 60))
        colorRGB[0] += 5
        posx += 1
    while colorRGB[2] > 0:
        pygame.draw.rect(screen, (colorRGB[0], colorRGB[1], colorRGB[2]), (posx, 530, 1, 60))
        colorRGB[2] -= 5
        posx += 1
    pygame.draw.rect(screen, LINE, (250, 530, 306, 60), 1)
    posx += 30
    colorRGB = [0, 0, 0]
    for i in range(127):
        for i in range(3):
            colorRGB[i] += 2
        pygame.draw.rect(screen, (colorRGB[0], colorRGB[1], colorRGB[2]), (posx, 530, 1, 60))
        posx += 1
    pygame.draw.rect(screen, LINE, (586, 530, 127, 60), 1)


def getState(mx, my):
    global initialX, initialY
    if my > 525:
        initialX, initialY = None, None
        return 2
    elif my <= 20:
        initialX, initialY = None, None
        return 3
    elif mx < 50 and 20 < my < 520:
        initialX, initialY = None, None
        return 4
    else:
        return 1


def drawMenu():
    myFont = myFont = pygame.font.SysFont(None, 25)
    titles = ["Save", "Load"]
    x = 0
    for i in range(len(titles)):
        textSurface = myFont.render(titles[i], False, (0, 0, 0))
        width = textSurface.get_width()
        extra = (80 - width) / 2
        screen.blit(textSurface, (x + extra, 2))
        x += 80
        pygame.draw.line(screen, LINE, (x, 5), (x, 15))


def selectMenu(mx, my):
    toolIndex = int(mx / 80)
    if toolIndex == 0:
        string = input("Please enter the file name: ")
        file = open(string, 'w')
        for i in range(51, 800):
            for j in range(21, 520):
                color = screen.get_at((i, j))
                line = str(i) + "," + str(j) + "," + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + "\n"
                file.write(line)
        print("Saved!")
        file.close()
    if toolIndex == 1:
        fileName = input("Please enter the file name: ")
        filePath = Path(fileName)
        while filePath.is_file() == False:
            fileName = input("File doesn't exist. Enter a valid file name (eg: words.txt): ")  # get file name
            filePath = Path(fileName)
        file = open(fileName, 'r')
        line = file.readline().rstrip('\n')
        while line != "":
            element = line.split(",")
            for i in range(len(element)):
                element[i] = int(element[i].rstrip(""))
            screen.set_at((element[0], element[1]), (element[2], element[3], element[4]))
            line = file.readline()
        print("File Loaded!")


pygame.init()
pygame.font.init()


def floodFill(x, y, color):
    stack = []
    stack.append((x, y))
    while len(stack) != 0:
        x, y = stack.pop(0)
        if x < 50 or x > 799 or 520 < y or y < 20:
            continue
        if screen.get_at((x, y)) != color:
            continue
        screen.set_at((x, y), currentColor)
        stack.append((x - 1, y))
        stack.append((x + 1, y))
        stack.append((x, y - 1))
        stack.append((x, y + 1))


def getCorrectImage(str):
    img = pygame.image.load(str)
    img = pygame.transform.scale(img, (25, 25))
    return img


width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Paint')
clock = pygame.time.Clock()
screen.fill((255, 255, 255))

pencil = getCorrectImage("pencil.png")
line = getCorrectImage("line.png")
rectangle = getCorrectImage("rectangle.png")
circle = getCorrectImage("circle.png")
eraser = getCorrectImage("eraser.png")
flood = getCorrectImage("flood.png")
images = [pencil, line, rectangle, circle, eraser, flood]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
BROWN = (150, 75, 0)
THEME = (250, 250, 250)
LINE = (200, 200, 200)
HOVER = (220, 220, 220)
color = [WHITE, BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, CYAN, BROWN]
running = True

currentColor = (0, 0, 0)
currentState = 0
currentTool = 0  # 0: pencil, 1: line, 2: rectangle
currentThickness = 2
initialX, initialY = None, None

while running:
    try:
        mx, my = pygame.mouse.get_pos()
        currentState = getState(mx, my)

        for evt in pygame.event.get():
            currentHover = None
            if evt.type == pygame.QUIT:
                running = False

            if currentState == 1:
                if currentTool == 0:
                    pygame.mouse.set_cursor(*pygame.cursors.tri_left)
                    if evt.type == pygame.MOUSEBUTTONDOWN or evt.type == pygame.MOUSEMOTION:
                        mx, my = evt.pos
                        if pygame.mouse.get_pressed()[0]:
                            if initialX is not None:
                                pygame.draw.line(screen, currentColor, (initialX, initialY), (mx, my), currentThickness)
                            initialX, initialY = mx, my
                    elif evt.type == pygame.MOUSEBUTTONUP:
                        initialX, initialY = None, None
                elif currentTool == 1:
                    pygame.mouse.set_cursor(*pygame.cursors.tri_left)
                    if evt.type == pygame.MOUSEBUTTONDOWN:
                        initialX, initialY = evt.pos
                        screen.set_at(evt.pos, currentColor)
                    elif evt.type == pygame.MOUSEBUTTONUP and initialX is not None:
                        finalX, finalY = evt.pos
                        pygame.draw.line(screen, currentColor, (initialX, initialY), (finalX, finalY), currentThickness)

                elif currentTool == 2:
                    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                    if evt.type == pygame.MOUSEBUTTONDOWN:
                        initialX, initialY = evt.pos
                        screen.set_at(evt.pos, currentColor)
                    elif evt.type == pygame.MOUSEBUTTONUP and initialX is not None:
                        finalX, finalY = evt.pos
                        tempX = min(initialX, finalX)
                        tempY = min(initialY, finalY)
                        pygame.draw.rect(screen, currentColor,
                                         (tempX, tempY, max(initialX, finalX) - tempX, max(initialY, finalY) - tempY),
                                         currentThickness)
                elif currentTool == 3:
                    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                    if evt.type == pygame.MOUSEBUTTONDOWN:
                        initialX, initialY = evt.pos
                        screen.set_at(evt.pos, currentColor)
                    elif evt.type == pygame.MOUSEBUTTONUP and initialX is not None:
                        finalX, finalY = evt.pos
                        midX, midY = (initialX + finalX) / 2, (initialY + finalY) / 2
                        radius = round(((midY - initialY) ** 2 + (midX - initialX) ** 2) ** (1 / 2))
                        pygame.draw.circle(screen, currentColor, (midX, midY), radius, currentThickness)
                elif currentTool == 4:
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                    if evt.type == pygame.MOUSEBUTTONDOWN or evt.type == pygame.MOUSEMOTION:
                        mx, my = evt.pos
                        if pygame.mouse.get_pressed()[0]:
                            if initialX is not None:
                                pygame.draw.line(screen, WHITE, (initialX, initialY), (mx, my), currentThickness)
                            initialX, initialY = mx, my
                    elif evt.type == pygame.MOUSEBUTTONUP:
                        initialX, initialY = None, None
                elif currentTool == 5:
                    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                    if evt.type == pygame.MOUSEBUTTONDOWN:
                        x, y = evt.pos
                        floodFill(x, y, screen.get_at((x, y)))
            if currentState == 2:  # Color selection
                pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                if pygame.mouse.get_pressed()[0]:
                    mx, my = pygame.mouse.get_pos()
                    if 730 <= mx <= 770 and 540 <= my <= 580:
                        currentColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    else:
                        temp = screen.get_at(evt.pos)
                        if temp != THEME and temp != LINE:
                            currentColor = screen.get_at(evt.pos)
            if currentState == 3:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                if evt.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        mx, my = evt.pos
                        selectMenu(mx, my)
                if evt.type == pygame.MOUSEMOTION:
                    mx, my = evt.pos

            if currentState == 4:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                if evt.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        mx, my = evt.pos
                        currentTool = selectTool(mx, my, currentTool)
                if evt.type == pygame.MOUSEMOTION:
                    mx, my = evt.pos
                    currentHover = getHover(mx, my)

        drawToolBar()
        drawColorPanel(currentColor)
        drawTool(currentTool, currentThickness, currentHover)
        drawMenu()
        pygame.display.flip()
        clock.tick(144)
    except Exception:
        traceback.print_exc()
