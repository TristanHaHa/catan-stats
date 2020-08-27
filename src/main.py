import pygame, sys, time, math
from collections import namedtuple
from random import seed
from random import randint


BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (128,128,128)
RED = (191,25,25)
YELLOW = (255,230,0)

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
    titleTxt = titleFont.render("Catan Stats", True, YELLOW)
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
    titleTxt1 = titleFont.render("Please enter the players' names", True, YELLOW)
    titleTxt2 = titleFont.render("and colors in turn order", True, YELLOW)
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
                        players.append(Player(name,textBoxes[i].txt,0,0))

            if errorMessage == "" and numPlayers < 2:
                errorMessage = "Error: must have at least 2 players"
            if errorMessage == "":
                canContinue = True
                gameMenu(players)
            else:
                errorFont = pygame.font.SysFont(None, 30)
                errorTxt = errorFont.render(errorMessage, True, YELLOW)
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
    margin = 175
    rollButtonX = 33
    rollButtonY = height - (margin + buttonHeight)

    rollButton = pygame.Rect(rollButtonX,rollButtonY,buttonWidth,buttonHeight)
    makeButton(rollButton,outlineWidth,"Roll")

    previousButton = pygame.Rect(rollButtonX,rollButtonY+buttonHeight+20,buttonWidth,buttonHeight)
    makeButton(previousButton,outlineWidth,"Prev.")

    nextButton = pygame.Rect(rollButtonX,previousButton.top+buttonHeight+20,buttonWidth,buttonHeight)

    startButton = pygame.Rect(rollButtonX,150,buttonWidth,buttonHeight)
    makeButton(startButton,outlineWidth,"Start")

    font = pygame.font.SysFont(None, 100)

    manualRollRect = pygame.Rect(rollButtonX-5,rollButtonY - 115,buttonWidth+10,buttonHeight)
    manualRollTextBox = TextBox(manualRollRect,"",False)
    makeTextBox(manualRollRect,"Input Roll")


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
    index = -1 #current roll index
    playerTurn = 0 # current player turn
    gameMenuRunning = True
    timerRunning = False
    nextPlayer = False
    barPopup = False
    seconds = 0
    startTick=0
    pauseTick = 0

    def rollDice():
        seed()
        die1 = randint(1,6)
        die2 = randint(1,6)
        return die1+die2
    def displayRoll(roll=0):
        rollTxt = font.render(f"{roll}", True, YELLOW)
        rollTxtBkgd = pygame.Rect(rollButtonX,rollButtonY - rollTxt.get_height(),buttonWidth, rollTxt.get_height())
        makeButton(rollTxtBkgd,0,"",(191,25,25))
        makeButton(rollButton,outlineWidth,"Roll")
        screen.blit(rollTxt, [rollButtonX+(buttonWidth/2 - rollTxt.get_width()/2),rollButtonY - rollTxt.get_height(),rollTxt.get_width(), rollTxt.get_height()])
    def updateGraph():
        drawGraph(numsDict,width*(2/7),height-50,1.37*width/2,0.8*height/2,nums)
    def updateRolls(roll):
        nums.append(roll)
        numsDict[roll] += 1
        updateGraph()
    def updateButtons():
        if 0 <= index < len(nums)-1:
            makeButton(nextButton,outlineWidth,"Next")
        else:
            makeButton(pygame.Rect(nextButton.left-outlineWidth,nextButton.top-outlineWidth,nextButton.width+outlineWidth*2,nextButton.height+outlineWidth*2),0,"",(191,25,25))
        rollsAgo = len(nums)-index-1
        if rollsAgo == 1:
            output = "1 roll ago"
        elif rollsAgo == 0:
            output = f"Current: {len(nums)}"
        else:
            output = f"{rollsAgo} rolls ago"
        makeTextBox(manualRollRect,output)
    topGraphMargin = 70
    def updatePlayers():
        playerFont = pygame.font.SysFont(None, 40)
        playerTxt = playerFont.render(f"{players[playerTurn].name}'s", True, BLACK)
        turnTxt = playerFont.render("turn", True, BLACK)
        playerTxtBkgd = pygame.Rect(0,4,180,playerTxt.get_height()+turnTxt.get_height())
        makeButton(playerTxtBkgd,0,"",RED)
        screen.blit(playerTxt,[(rollButtonX+buttonWidth/2)-playerTxt.get_width()/2,5,playerTxt.get_width(),playerTxt.get_height()])
        screen.blit(turnTxt,[(rollButtonX+buttonWidth/2)-turnTxt.get_width()/2,playerTxt.get_height(),turnTxt.get_width(),turnTxt.get_height()])
    def updateTimer(seconds=0):
        minutes = int(seconds/60)
        tensPlace = int((seconds - minutes*60)/10)
        onesPlace = seconds%10
        timeFormatted = f"{minutes}:{tensPlace}{onesPlace}"
        timerTxt = font.render(timeFormatted, True, YELLOW)
        timerTxtBkgd = pygame.Rect(0,topGraphMargin,timerTxt.get_width()+50, timerTxt.get_height())
        makeButton(timerTxtBkgd,0,"",(191,25,25))
        screen.blit(timerTxt, [(rollButtonX+buttonWidth/2)-timerTxt.get_width()/2,timerTxtBkgd.top,timerTxt.get_width(), timerTxt.get_height()])
    updateTimer()
    updatePlayers()
    displayRoll()
    updateGraph()
    while gameMenuRunning:
        if timerRunning:
            seconds = int( (pygame.time.get_ticks()-startTick) /1000)
            updateTimer(seconds)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            for bar in diceBars:
                if bar.rect.collidepoint(pygame.mouse.get_pos()):
                    barPopup = True
                    updateGraph()
                    barXLen = 50
                    barYLen = 30
                    barX =pygame.mouse.get_pos()[0]-barXLen
                    barY =pygame.mouse.get_pos()[1]-barYLen
                    tempRect = pygame.Rect(barX,barY,barXLen,barYLen)
                    makeButton(tempRect,3,"",WHITE)
                    screen.blit(bar.label, [barX+barXLen/2-bar.label.get_width()/2,barY+bar.label.get_height()/2,bar.label.get_width(),bar.label.get_height()])
                    break
            if event.type == pygame.MOUSEMOTION:
                if barPopup:
                    if not bar.rect.collidepoint(pygame.mouse.get_pos()):
                        barPopup = False
                        updateGraph()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rollButton.collidepoint(event.pos):
                    for i in range(15):
                        roll = rollDice()
                        displayRoll(roll)
                        pygame.display.update()
                        pygame.time.delay(20)
                    if nextPlayer:
                        playerTurn = (playerTurn+1)%len(players)
                        startTick = pygame.time.get_ticks()
                        timerRunning = True
                        makeButton(startButton,outlineWidth,"Pause")
                        updatePlayers()
                        updateRolls(roll)
                        index+=1
                        if len(nums) == 1:
                            makeTextBox(manualRollRect,"1 roll")
                        else:
                            makeTextBox(manualRollRect,f"{len(nums)} rolls")
                elif manualRollRect.collidepoint(event.pos):
                    manualRollTextBox = manualRollTextBox._replace(active=True)
                    makeTextBox(manualRollRect,manualRollTextBox.txt)
                elif previousButton.collidepoint(event.pos):
                    if index >= 1:
                        index-=1
                        displayRoll(nums[index])
                        updateButtons()
                elif nextButton.collidepoint(event.pos):
                    if 0 <= index <+ len(nums)-1:
                        index+=1
                        displayRoll(nums[index])
                        updateButtons()
                        updatePlayers()
                elif startButton.collidepoint(event.pos):
                    if timerRunning:
                        nextPlayer = True
                        timerRunning = False
                        pauseTick=pygame.time.get_ticks()
                        makeButton(startButton,outlineWidth,"Start")
                    else:
                        if seconds == 0:
                            startTick=pygame.time.get_ticks()
                        else:
                            startTick += pygame.time.get_ticks() - pauseTick
                        timerRunning = True
                        makeButton(startButton,outlineWidth,"Pause")
                else:
                    manualRollTextBox = manualRollTextBox._replace(active=False)
            if manualRollTextBox.active:
                if event.type == pygame.KEYDOWN:
                    newText = manualRollTextBox.txt
                    if event.key == pygame.K_RETURN:
                        roll = manualRollTextBox.txt
                        if roll in ["2","3","4","5","6","7","8","9","10","11","12"]:
                            displayRoll(roll)
                            updateButtons()
                            newText = ""
                            if nextPlayer:
                                timerRunning = True
                                playerTurn = (playerTurn+1)%len(players)
                                updatePlayers()
                                updateRolls(int(roll))
                            if len(nums) == 1:
                                makeTextBox(manualRollRect,"1 roll")
                            else:
                                makeTextBox(manualRollRect,f"{len(nums)} rolls")
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

def makeButton(rectangle,outlineWidth,txt="",bkgcolor=GRAY,txtcolor=WHITE):
    x = rectangle.left
    y = rectangle.top
    w = rectangle.w
    h = rectangle.h

    pygame.draw.rect(screen,BLACK,[x-outlineWidth,y-outlineWidth,w+2*outlineWidth,h+2*outlineWidth])
    pygame.draw.rect(screen,bkgcolor,[x,y,w,h])

    font = pygame.font.SysFont(None, 40)
    text = font.render(txt, True, txtcolor)
    screen.blit(text, [x+(w/2 - text.get_width()/2),y+(h/2-text.get_height()/2),text.get_width(),text.get_height()])

def makeTextBox(rectangle,txt="",color=WHITE,txtcolor=BLACK):
    x = rectangle.left
    y = rectangle.top
    w = rectangle.w
    h = rectangle.h

    pygame.draw.rect(screen,color,[x,y,w,h])
    font = pygame.font.SysFont(None, 30)
    text = font.render(txt, True, txtcolor)
    screen.blit(text, [x+5,y+(h/2-text.get_height()/2+2),text.get_width(),text.get_height()])

def drawGraph(dict,x,y,w,h,total):
    global diceBars
    yLines = []
    xLines = []
    diceBars.clear()
    thickness = 2
    numLines = 13
    makeButton(pygame.Rect(x-50,y-h-50,w+100,h+100),0,"",(191,25,25))
    font = pygame.font.SysFont(None, 25)
    for i in range(101):
        rect = pygame.Rect(x,y-i*(h/100),w,thickness)
        yLines.append(rect)
    for i in range(11):
        yLine = pygame.Rect(x,y-i*(h/10),w,thickness)
        makeButton(yLine,0,"",BLACK)
        sideLabel = font.render(f"{i*10}%", True, BLACK)
        screen.blit(sideLabel, [x-(5+sideLabel.get_width()),y-i*(h/10)-5,sideLabel.get_width(),sideLabel.get_height()])
    for i in range(numLines):
        midLine = pygame.Rect(0,height/2,width,thickness)
        makeButton(midLine,0,"",BLACK)
        if i == 0 or i == numLines-1:
            xLine = pygame.Rect(x+i*(w/(numLines-1)),y-h,thickness,h)
            xLines.append(xLine)
            makeButton(xLine,0,"",BLACK)
        else:#27p = 10 percent, 37p = 1 die
            barWidth = 25
            if len(total) == 0:
                percent = 0
                yValue = y
            else:
                percent = dict[i+1]/len(total)
                yValue = yLines[math.floor(percent*100)].top
            bar = pygame.Rect(x+i*(w/(numLines-1))-barWidth/2,yValue,barWidth,yLines[0].bottom-yValue)
            makeButton(bar,0,"",YELLOW)

            bottomBarHeight = 2
            bottomBar = pygame.Rect(x+i*(w/(numLines-1))-barWidth/2,y-bottomBarHeight,barWidth,bottomBarHeight)
            makeButton(bottomBar,0,"",YELLOW)


            if dict[i+1] > 0:
                numLabel = font.render(f"{dict[i+1]}",True,BLACK)
                screen.blit(numLabel, [x+i*(w/(numLines-1))-numLabel.get_width()/2,yValue,numLabel.get_width(),numLabel.get_height()])

            hoverFont = pygame.font.SysFont(None, 20)
            diceBars.append(Bar(bar,hoverFont.render(f"{percent*100:.2f}%",True,BLACK),i+1))

        if not i >= numLines-2:
            bottomLabel = font.render(f"{i+2}", True, BLACK)
            screen.blit(bottomLabel, [x+(i+1)*(w/(numLines-1))-5,y+(5),bottomLabel.get_width(),bottomLabel.get_height()])

def main():
    #mainMenu()
    #playerMenu()
    Player = namedtuple("Player", "name color turnTime average")
    gameMenu([Player("Player","Red",0,0),Player("Tristan","Blue",0,0)])

pygame.init()
size = width, height = 700,700
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Catan Stats")

TextBox = namedtuple("TextBox", "rect txt active")
Bar = namedtuple("Bar", "rect label diceNum")
diceBars=[]


main()
