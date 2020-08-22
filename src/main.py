import pygame, random, sys

def mainMenu():
    buttonX = width/2
    buttonY = height/2 + 50
    buttonWidth = 130
    buttonHeight = 50
    outlineWidth = 4

    screen.fill((191,25,25))

    makeButton(buttonX,buttonY,buttonWidth,buttonHeight,outlineWidth,"Start")

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
                if buttonX-buttonWidth/2-outlineWidth <= pygame.mouse.get_pos()[0] <= (buttonX-buttonWidth/2-outlineWidth)+(buttonWidth+outlineWidth*2):
                    if buttonY-buttonHeight/2-outlineWidth <= pygame.mouse.get_pos()[1] <= (buttonY-buttonHeight/2-outlineWidth)+(buttonHeight+outlineWidth*2):
                        mainMenuRunning = False
        pygame.display.update()
    playerMenu()

def makeButton(x,y,w,h,outlineWidth,txt):
    pygame.draw.rect(screen,(0,0,0),[x-w/2-outlineWidth,y-h/2-outlineWidth,w+outlineWidth*2,h+outlineWidth*2])
    pygame.draw.rect(screen,(128,128,128),[x-w/2,y-h/2,w,h])

    buttonFont = pygame.font.SysFont(None, 40)
    startTxt = buttonFont.render(txt, True, (255,255,255))
    screen.blit(startTxt, [x-startTxt.get_rect().width/2,y-startTxt.get_rect().height/2,w,h])

def playerMenu():
    screen.fill((191,25,25))

    titleFont = pygame.font.SysFont(None, 30)
    titleTxt = titleFont.render("Please enter the players' names and colors in turn order", True, (255,230,0))
    screen.blit(titleTxt, [width/2-250,height/2 - 150, 500, 100])

    playerMenuRunning = True
    while playerMenuRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.update()

def main():
    mainMenu()

pygame.init()
size = width, height = 700,700
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Catan Stats")
main()
