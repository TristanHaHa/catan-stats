import pygame, sys, time
from collections import namedtuple
from random import seed
from random import randint

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

    textBoxes = []
    for i in range(1,5):
        rect1 = pygame.Rect(width/2 - (140+50),150+ 75*i,140,30)
        rect2 = pygame.Rect(width/2 + 50,150+ 75*i,140,30)

        makeTextBox(rect1,f"Player {i}")
        makeTextBox(rect2,"Color")

        textBoxes.append(TextBox(rect1,"",False))
        textBoxes.append(TextBox(rect2,"",False))
    canContinue = False
    while canContinue == False:
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
                    if event.key == pygame.K_TAB or  event.key == pygame.K_RETURN:
                        if activeTextBoxIndex+1 > len(textBoxes)-1 or activeTextBoxIndex < 0:
                            activeTextBoxIndex = 0
                        else:
                            activeTextBoxIndex += 1
                        makeTextBox(textBoxes[activeTextBoxIndex].rect,textBoxes[activeTextBoxIndex].txt)
                        continue
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
            Player = namedtuple("Player", "name color")
            players = []
            errorMessage = ""
            numPlayers = 0
            hasPlayer = False
            for i in range(len(textBoxes)):
                name = ""
                if i%2 == 0:
                    if textBoxes[i].txt != "":
                        hasPlayer = True
                        numPlayers+=1
                        name = textBoxes[i].txt
                    else:
                        break
                elif hasPlayer:
                    if textBoxes[i].txt == "":
                        hasPlayer = False
                        errorMessage = "Error: must include a color for each player"
                    else:
                        players.append(Player(name,textBoxes[i].txt))

            if errorMessage == "" and numPlayers < 2:
                errorMessage = "Error: must have at least 2 players"
            if errorMessage == "":
                canContinue = True
                gameMenu(players)
            else:
                errorFont = pygame.font.SysFont(None, 30)
                errorTxt = errorFont.render(errorMessage, True, (255,230,0))
                errorBkgd = pygame.Rect(0,height*(3/4), width, 75)
                makeButton(errorBkgd,0,"",(191,25,25))
                screen.blit(errorTxt, [width/2-errorTxt.get_width()/2,height*(3/4), 300, 7])
        else:
            canContinue = True
            mainMenu()

def gameMenu(players):
    screen.fill((191,25,25))

    buttonWidth = 100
    buttonHeight = 40
    outlineWidth = 4
    margin = 35
    rollButtonX = margin
    rollButtonY = height - (margin + buttonHeight)

    rollButton = pygame.Rect(rollButtonX,rollButtonY,buttonWidth,buttonHeight)
    makeButton(rollButton,outlineWidth,"Roll")

    def displayRoll(roll=0):
        rollTxt = font.render(f"{roll}", True, (255,230,0))
        rollTxtBkgd = pygame.Rect(margin,rollButtonY - rollTxt.get_height(),rollTxt.get_width()*3, rollTxt.get_height())
        makeButton(rollTxtBkgd,0,"",(191,25,25))
        makeButton(rollButton,outlineWidth,"Roll")
        screen.blit(rollTxt, [margin+(buttonWidth/2 - rollTxt.get_width()/2),rollButtonY - rollTxt.get_height(),rollTxt.get_width(), rollTxt.get_height()])

    font = pygame.font.SysFont(None, 100)
    displayRoll()

    manualRollRect = pygame.Rect(rollButtonX,rollButtonY - 110,buttonWidth,buttonHeight)
    manualRollTextBox = TextBox(manualRollRect,"",False)
    makeTextBox(manualRollRect,"Input")

    nums = []
    numsDict = {
        2:0,
        3:0,
        4:0,
        5:0,
        6:0,
        7:0,
        8:0,
        9:0,
        10:0,
        11:0,
        12:0
    }
    def showProb():
        print(f"Out of {len(nums)} rolls:")
        for i in range(2,len(numsDict)+1):
            prob = 100*(numsDict[i]/len(nums))
            print(f"{i}: {prob:.2f}%", flush=True  )
    def updateRolls(roll):
        nums.append(roll)
        numsDict[roll] += 1
        showProb()
    gameMenuRunning = True
    while gameMenuRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rollButton.collidepoint(event.pos):
                    for i in range(15):
                        roll = rollDice()
                        displayRoll(roll)
                        pygame.display.update()
                        pygame.time.delay(20)
                    updateRolls(roll)
                elif manualRollRect.collidepoint(event.pos):
                    manualRollTextBox = manualRollTextBox._replace(active=True)
                    makeTextBox(manualRollRect,manualRollTextBox.txt)
                else:
                    manualRollTextBox = manualRollTextBox._replace(active=False)
            if manualRollTextBox.active:
                if event.type == pygame.KEYDOWN:
                    newText = manualRollTextBox.txt
                    if event.key == pygame.K_RETURN:
                        roll = manualRollTextBox.txt
                        if 2 <= int(roll) <= 12:
                            displayRoll(roll)
                            updateRolls(int(roll))
                            newText = ""
                        else:
                            manualRollTextBox = manualRollTextBox._replace(txt="")
                            makeTextBox(manualRollRect,"ERROR")
                            continue
                    elif event.key == pygame.K_BACKSPACE:
                        newText = newText[:-1]
                    else:
                        newText += event.unicode
                    manualRollTextBox = manualRollTextBox._replace(txt=newText)
                    makeTextBox(manualRollRect,newText)

        pygame.display.update()

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

def rollDice():
    seed()
    die1 = randint(1,6)
    die2 = randint(1,6)
    return die1+die2

def main():
    #mainMenu()
    #playerMenu()
    Player = namedtuple("Player", "name color")
    gameMenu([Player("Tristan","Red"),Player("Tristanity","Blue")])

pygame.init()
size = width, height = 700,700
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Catan Stats")
TextBox = namedtuple("TextBox", "rect txt active")
main()
