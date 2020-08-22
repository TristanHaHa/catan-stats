import pygame, random, sys

def mainMenu():
    buttonX = width/2
    buttonY = height/2 + 50
    buttonWidth = 130
    buttonHeight = 50
    outlineWidth = 4

    screen.fill((191,25,25))

    makeRect(buttonX,buttonY,buttonWidth,buttonHeight,outlineWidth,"Start")

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

def playerMenu():
    screen.fill((191,25,25))

    titleFont = pygame.font.SysFont(None, 60)
    titleTxt1 = titleFont.render("Please enter the players' names", True, (255,230,0))
    titleTxt2 = titleFont.render("and colors in turn order", True, (255,230,0))
    screen.blit(titleTxt1, [width/2-325,height/2 - 300, 500, 100])
    screen.blit(titleTxt2, [width/2-250,height/2 - 250, 500, 100])

    textBoxes = []
    for i in range(1,5):
        rect1 = pygame.Rect(250,225+ 75*i,140,40)
        rect2 = pygame.Rect(450,225+ 75*i,140,40)
        textBoxes.append(rect1)
        textBoxes.append(rect2)

        str = f"Player {i}"
        makeRectFromRect(rect1,0,str,(255,255,255),(0,0,0))
        makeRectFromRect(rect2,0,"Color",(255,255,255),(0,0,0))

    playerMenuRunning = True
    while playerMenuRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            #if event.type == pygame.MOUSEBUTTONDOWN

        pygame.display.update()

def makeRect(x,y,w,h,outlineWidth,txt="",bkgcolor=(128,128,128),txtcolor=(255,255,255)):
    pygame.draw.rect(screen,(0,0,0),[x-w/2-outlineWidth,y-h/2-outlineWidth,w+outlineWidth*2,h+outlineWidth*2])
    pygame.draw.rect(screen,bkgcolor,[x-w/2,y-h/2,w,h])

    font = pygame.font.SysFont(None, 40)
    text = font.render(txt, True, txtcolor)
    screen.blit(text, [x-text.get_rect().width/2,y-text.get_rect().height/2,w,h])

def makeRectFromRect(rectangle,outlineWidth,txt="",bkgcolor=(128,128,128),txtcolor=(255,255,255)):
    makeRect(rectangle.left,rectangle.top,rectangle.w,rectangle.h,outlineWidth,txt,bkgcolor,txtcolor)

def main():
    #mainMenu()
    playerMenu()

pygame.init()
size = width, height = 700,700
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Catan Stats")
main()
