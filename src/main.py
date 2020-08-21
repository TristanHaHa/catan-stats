import pygame, random, sys



def mainMenu():
    buttonX = width/2
    buttonY = height/2 + 50
    buttonWidth = 130
    buttonHeight = 50

    screen.fill((0,0,0))
    pygame.draw.rect(screen,(255,0,0),[buttonX-buttonWidth/2,buttonY-buttonHeight/2,buttonWidth,buttonHeight])

    buttonFont = pygame.font.SysFont(None, 40)
    startTxt = buttonFont.render('Start', True, (255,255,255))
    screen.blit(startTxt, [buttonX-startTxt.get_rect().width/2,buttonY-startTxt.get_rect().height/2,buttonWidth,buttonHeight])


    titleFont = pygame.font.SysFont(None, 125)
    titleTxt = titleFont.render('Catan Stats', True, (255,255,255))
    screen.blit(titleTxt, [width/2-250,height/2 - 150, 500, 100])

def main():
    mainMenu()

    while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        pygame.display.update()


pygame.init()
size = width, height = 700,700
screen = pygame.display.set_mode(size)
main()
