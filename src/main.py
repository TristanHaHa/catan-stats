import pygame, random, sys

def mainMenu():
    global mainMenuRunning

    buttonX = width/2
    buttonY = height/2 + 50
    buttonWidth = 130
    buttonHeight = 50

    screen.fill((191,25,25))

    outlineWidth = 4
    pygame.draw.rect(screen,(0,0,0),[buttonX-buttonWidth/2-outlineWidth,buttonY-buttonHeight/2-outlineWidth,buttonWidth+outlineWidth*2,buttonHeight+outlineWidth*2])
    pygame.draw.rect(screen,(128,128,128),[buttonX-buttonWidth/2,buttonY-buttonHeight/2,buttonWidth,buttonHeight])

    buttonFont = pygame.font.SysFont(None, 40)
    startTxt = buttonFont.render('Start', True, (255,255,255))
    screen.blit(startTxt, [buttonX-startTxt.get_rect().width/2,buttonY-startTxt.get_rect().height/2,buttonWidth,buttonHeight])

    titleFont = pygame.font.SysFont(None, 125)
    titleTxt = titleFont.render('Catan Stats', True, (255,230,0))
    screen.blit(titleTxt, [width/2-250,height/2 - 150, 500, 100])

    while mainMenuRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttonX-buttonWidth/2-outlineWidth <= pygame.mouse.get_pos()[0] <= (buttonX-buttonWidth/2-outlineWidth)+(buttonWidth+outlineWidth*2):
                    if buttonY-buttonHeight/2-outlineWidth <= pygame.mouse.get_pos()[0] <= (buttonY-buttonHeight/2-outlineWidth)+(buttonHeight+outlineWidth*2):
                        mainMenuRunning = False
        pygame.display.update()
    print("clicked button")

def main():
    mainMenu()

pygame.init()
size = width, height = 700,700
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Catan Stats")

mainMenuRunning = True

main()
