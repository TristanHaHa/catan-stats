import pygame, random, sys
from collections import namedtuple

def mainMenu():
    buttonWidth = 130
    buttonHeight = 50
    outlineWidth = 4
    buttonX = width/2 - buttonWidth/2
    buttonY = height/2

    screen.fill((191,25,25))

    button = pygame.Rect(buttonX,buttonY,buttonWidth,buttonHeight)
    makeButton(button,outlineWidth,"Start")

    titleFont = pygame.font.SysFont(None, 125)
    titleTxt = titleFont.render("Catan Stats", True, (255,230,0))
    screen.blit(titleTxt, [width/2-250,height/2 - 150, 500, 100])

    mainMenuRunning = True
    while mainMenuRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                   mainMenuRunning = False
        pygame.display.update()
    playerMenu()

def playerMenu():
    screen.fill((191,25,25))

    buttonWidth = 130
    buttonHeight = 50
    outlineWidth = 4
    margin = 25
    backButtonX = margin
    backButtonY = height - (margin + buttonHeight)
    nextButtonX = width - (margin + buttonWidth)
    nextButtonY = backButtonY

    backButton = pygame.Rect(backButtonX,backButtonY,buttonWidth,buttonHeight)
    nextButton = pygame.Rect(nextButtonX,nextButtonY,buttonWidth,buttonHeight)
    makeButton(backButton,outlineWidth,"Back")
    makeButton(nextButton,outlineWidth,"Next")

    titleFont = pygame.font.SysFont(None, 60)
    titleTxt1 = titleFont.render("Please enter the players' names", True, (255,230,0))
    titleTxt2 = titleFont.render("and colors in turn order", True, (255,230,0))
    screen.blit(titleTxt1, [width/2-325,height/2 - 300, 500, 100])
    screen.blit(titleTxt2, [width/2-250,height/2 - 250, 500, 100])

    TextBox = namedtuple("TextBox", "rect txt active")
    textBoxes = []
    for i in range(1,5):
        rect1 = pygame.Rect(width/2 - (140+50),150+ 75*i,140,30)
        rect2 = pygame.Rect(width/2 + 50,150+ 75*i,140,30)

        makeTextBox(rect1,f"Player {i}")
        makeTextBox(rect2,"Color")

        textBoxes.append(TextBox(rect1,"",False))
        textBoxes.append(TextBox(rect2,"",False))

    playerMenuRunning = True
    nextMenu = True
    activeTextBoxIndex = -1
    while playerMenuRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                clickedOnBox = False
                for i in range(len(textBoxes)):
                    if textBoxes[i].rect.collidepoint(event.pos):
                        clickedOnBox = True
                        if activeTextBoxIndex >= 0:
                            textBoxes[activeTextBoxIndex] = textBoxes[activeTextBoxIndex]._replace(active = False)
                        textBoxes[i] = textBoxes[i]._replace(active = True)
                        activeTextBoxIndex = i
                if clickedOnBox == False:
                    if activeTextBoxIndex >=0:
                        activeTextBoxIndex = -1
                else:
                    makeTextBox(textBoxes[activeTextBoxIndex].rect,textBoxes[activeTextBoxIndex].txt)
            if event.type == pygame.KEYDOWN and activeTextBoxIndex >= 0:
                newText = textBoxes[activeTextBoxIndex].txt
                if event.key == pygame.K_BACKSPACE:
                    newText = newText[:-1]
                else:
                    newText += event.unicode
                textBoxes[activeTextBoxIndex] = textBoxes[activeTextBoxIndex]._replace(txt=newText)
                makeTextBox(textBoxes[activeTextBoxIndex].rect,textBoxes[activeTextBoxIndex].txt)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if backButton.collidepoint(event.pos):
                    nextMenu = False
                    playerMenuRunning = False
                if nextButton.collidepoint(event.pos):
                    playerMenuRunning = False

        pygame.display.update()
    if (nextMenu):
        errorMessage = ""
        numPlayers = 0
        hasPlayer = False
        for i in range(len(textBoxes)):
            if i%2 == 0:
                if textBoxes[i].txt != "":
                    hasPlayer = True
                    numPlayers+=1
            else:
                if hasPlayer and textBox[i].txt == "":
                    errorMessage = "Error: must include a color for each player"
                hasPlayer = False

        if errorMessage == "" and numPlayers < 2:
            errorMessage = "Error: must have at least 2 players"
        if errorMessage == "": print("next menu")
        else:
            errorFont = pygame.font.SysFont(None, 30)
            errorTxt = errorFont.render(errorMessage, True, (255,230,0))
            screen.blit(errorTxt, [nextButtonX-(margin+errorTxt.get_width()),height-(margin+errorTxt.get_height()), 300, 100])
            print(errorMessage)
    else:
        mainMenu()

def makeButton(rectangle,outlineWidth,txt="",bkgcolor=(128,128,128),txtcolor=(255,255,255)):
    x = rectangle.left
    y = rectangle.top
    w = rectangle.w
    h = rectangle.h

    pygame.draw.rect(screen,(0,0,0),[x-outlineWidth,y-outlineWidth,w+2*outlineWidth,h+2*outlineWidth])
    pygame.draw.rect(screen,bkgcolor,[x,y,w,h])

    font = pygame.font.SysFont(None, 40)
    text = font.render(txt, True, txtcolor)
    screen.blit(text, [x+(w/2 - text.get_width()/2),y+(h/2-text.get_height()/2),text.get_width(),text.get_height()])

def makeTextBox(rectangle,txt="",color=(255,255,255),txtcolor=(0,0,0)):
    x = rectangle.left
    y = rectangle.top
    w = rectangle.w
    h = rectangle.h

    pygame.draw.rect(screen,color,[x,y,w,h])
    font = pygame.font.SysFont(None, 30)
    text = font.render(txt, True, txtcolor)
    screen.blit(text, [x+5,y+(h/2-text.get_height()/2+2),text.get_width(),text.get_height()])

def main():
    mainMenu()
    #playerMenu()

pygame.init()
size = width, height = 700,700
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Catan Stats")

Player = namedtuple("Player", "name color")
players = []
main()
