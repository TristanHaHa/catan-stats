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

    screen.fill(RED)

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
    screen.fill(RED)

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
                        players.append(Player(name,textBoxes[i].txt,0,0))
                    else:
                        break
                elif hasPlayer:
                    if textBoxes[i].txt == "":
                        hasPlayer = False
                        errorMessage = "Error: must include a color for each player"

            if errorMessage == "" and numPlayers < 2:
                errorMessage = "Error: must have at least 2 players"
            if errorMessage == "":
                canContinue = True
                gameMenu(players)
            else:
                errorFont = pygame.font.SysFont(None, 30)
                errorTxt = errorFont.render(errorMessage, True, YELLOW)
                errorBkgd = pygame.Rect(0,height*(3/4), width, 75)
                makeButton(errorBkgd,0,"",RED)
                screen.blit(errorTxt, [width/2-errorTxt.get_width()/2,height*(3/4), 300, 7])
        else:
            canContinue = True
            mainMenu()

def gameMenu(players):
    screen.fill(RED)

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
    timesDict = {}
    for player in players:
        timesDict[player.name] = 0
    index = -1 #current roll index
    playerTurn = 0 # current player index
    gameMenuRunning = True
    timerRunning = False
    started = False # if user rolled yet
    barPopup = False # if bar is being displayed
    ms = 0
    startTick=0
    pauseTick = 0

    rollGraph = Graph(numsDict,width-1.37*width/2-5,height-50,1.37*width/2,0.8*height/2,13,11,100,"%")
    timerGraph = Graph(timesDict,width-1.37*width/2-5,height-50 - (height/2),1.37*width/2,0.8*height/2,len(timesDict)+2,11,10,"s")

    def rollDice():
        seed()
        die1 = randint(1,6)
        die2 = randint(1,6)
        return die1+die2
    def displayRoll(roll=0):
        rollTxt = font.render(f"{roll}", True, YELLOW)
        rollTxtBkgd = pygame.Rect(rollButtonX,rollButtonY - rollTxt.get_height(),buttonWidth, rollTxt.get_height())
        makeButton(rollTxtBkgd,0,"",RED)
        makeButton(rollButton,outlineWidth,"Roll")
        screen.blit(rollTxt, [rollButtonX+(buttonWidth/2 - rollTxt.get_width()/2),rollButtonY - rollTxt.get_height(),rollTxt.get_width(), rollTxt.get_height()])
    def displayGraphs():
        rollGraph.display()
        timerGraph.display()
    def updateGraphs():
        rollGraph.update(numsDict)
        timerGraph.update(timesDict)
    def updateRolls(roll):
        nums.append(roll)
        numsDict[roll] += 1
        updateGraphs()
    def updateButtons():
        if 0 <= index < len(nums)-1:
            makeButton(nextButton,outlineWidth,"Next")
        else:
            makeButton(pygame.Rect(nextButton.left-outlineWidth,nextButton.top-outlineWidth,nextButton.width+outlineWidth*2,nextButton.height+outlineWidth*2),0,"",RED)
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
    def updateTimer(ms=0):
        seconds = int(ms/1000)
        minutes = int(seconds/60)
        tensPlace = int((seconds - minutes*60)/10)
        onesPlace = seconds%10
        timeFormatted = f"{minutes}:{tensPlace}{onesPlace}"
        timerTxt = font.render(timeFormatted, True, YELLOW)
        timerTxtBkgd = pygame.Rect(0,topGraphMargin,timerTxt.get_width()+50, timerTxt.get_height())
        makeButton(timerTxtBkgd,0,"",RED)
        screen.blit(timerTxt, [(rollButtonX+buttonWidth/2)-timerTxt.get_width()/2,timerTxtBkgd.top,timerTxt.get_width(), timerTxt.get_height()])
    updateTimer()
    updatePlayers()
    displayRoll()
    displayGraphs()
    while gameMenuRunning:
        if timerRunning:
            ms = int(pygame.time.get_ticks()-startTick)
            updateTimer(ms)
            displayGraphs()
        for bar in bars:
            if bar.rect.collidepoint(pygame.mouse.get_pos()):
                barPopup = True
                displayGraphs()
                barXLen = 50
                barYLen = 30
                barX =pygame.mouse.get_pos()[0]-barXLen
                barY =pygame.mouse.get_pos()[1]-barYLen
                tempRect = pygame.Rect(barX,barY,barXLen,barYLen)
                makeButton(tempRect,3,"",WHITE)
                screen.blit(bar.label, [barX+barXLen/2-bar.label.get_width()/2,barY+bar.label.get_height()/2,bar.label.get_width(),bar.label.get_height()])
                break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEMOTION:
                if barPopup:
                    if not bar.rect.collidepoint(pygame.mouse.get_pos()):
                        barPopup = False
                        displayGraphs()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rollButton.collidepoint(event.pos):
                    for i in range(15):
                        roll = rollDice()
                        displayRoll(roll)
                        pygame.display.update()
                        pygame.time.delay(20)
                    if started:
                        players[playerTurn] = players[playerTurn]._replace(turns=players[playerTurn].turns+1,averageTime=ms/(players[playerTurn].turns+1))
                        if timesDict[players[playerTurn].name] == 0:
                            timesDict[players[playerTurn].name] = timesDict[players[playerTurn].name]+(ms/1000)
                        else:
                            timesDict[players[playerTurn].name] = (timesDict[players[playerTurn].name]+(ms/1000))/2
                        playerTurn = (playerTurn+1)%len(players)
                        startTick = pygame.time.get_ticks()
                        timerRunning = True
                        makeButton(startButton,outlineWidth,"Pause")
                        updatePlayers()
                        updateRolls(roll)
                        updateGraphs()
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
                    if not started:
                        started = True
                    if timerRunning:
                        timerRunning = False
                        pauseTick=pygame.time.get_ticks()
                        makeButton(startButton,outlineWidth,"Start")
                    else:
                        if int(ms) == 0:
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
                            if started:
                                timerRunning = True
                                timesDict[players[playerTurn].name] = (timesDict[players[playerTurn].name]+seconds)/2
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

class Graph:
    def __init__(self, data, x, y, w, h, numXLines, numYLines, maxYAxis, yAxisLabel):
        self.data = data
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.numYLines = numYLines
        self.numXLines = numXLines
        self.maxXAxis = len(data)
        self.maxYAxis = maxYAxis
        self.yAxisLabel = yAxisLabel
        self.total = 0
        for value in self.data.values():
            self.total += value
        self.display()

    def update(self, newData):
        self.data = newData
        self.total = 0
        for value in self.data.values():
            self.total += value
        #readjust the y axis
        if self.total > 0:
            self.maxYAxis = 1
            for value in self.data.values():
                if self.yAxisLabel == "%":
                    self.maxYAxis = max(self.maxYAxis,int(100*(value/self.total)))
                else:
                    self.maxYAxis = max(self.maxYAxis,int(value+1))
            yAxisInterval = self.maxYAxis/(self.numYLines-1)
        self.display()

    def display(self):
        global bars
        yLines = []
        temp = []
        for bar in bars:
            if self.yAxisLabel == "%":
                if bar.rect.top < self.h/2:
                    temp.append(bar)
            else:
                if bar.rect.top > self.h/2:
                    temp.append(bar)
        bar = temp
        data = self.data
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        total = self.total

        numXLines = self.numXLines
        numYLines = self.numYLines
        maxXAxis = self.maxXAxis
        maxYAxis = self.maxYAxis
        xAxisInterval = maxXAxis/(numXLines-1)
        yAxisInterval = maxYAxis/(numYLines-1)

        thickness = 2

        makeButton(pygame.Rect(x-60,y-h-50,w+120,h+100),0,"",RED)
        font = pygame.font.SysFont(None, 25)
        #draw reference ylines
        if self.yAxisLabel == "%":
            for i in range(maxYAxis+1):
                rect = pygame.Rect(x,y-i*h/maxYAxis,w,thickness)
                yLines.append(rect)
        else:
            for i in range((maxYAxis+1)*10):
                rect = pygame.Rect(x,y-i*h/(maxYAxis*10),w,thickness)
                yLines.append(rect)
        #draw ylines
        for i in range(numYLines):
            yLine = pygame.Rect(x,y-i*(h/(numYLines-1)),w,thickness)
            makeButton(yLine,0,"",BLACK)
            #draw y axis labels
            sideLabel = font.render(f"{i*yAxisInterval:.1f}{self.yAxisLabel}", True, BLACK)
            screen.blit(sideLabel, [x-(5+sideLabel.get_width()),y-i*(h/(numYLines-1))-5,sideLabel.get_width(),sideLabel.get_height()])

        midLine = pygame.Rect(0,height/2,width,thickness)
        makeButton(midLine,0,"",BLACK)

        for i in range(numXLines):
            if i == 0 or i == numXLines-1:
                xLine = pygame.Rect(x+i*(w/(numXLines-1)),y-h,thickness,h)
                makeButton(xLine,0,"",BLACK)

        i = 0
        for key,value in data.items():
            barWidth = 25
            if total == 0:
                percent = 0
                yValue = y
            else:
                percent = value/total
                if self.yAxisLabel == "%":
                    yValue = yLines[math.floor(percent*100)].top
                else:
                    yValue = yLines[math.floor(value*10)].top
            bar = pygame.Rect(x+(i+1)*(w/(numXLines-1))-barWidth/2,yValue,barWidth,yLines[0].bottom-yValue-thickness)
            makeButton(bar,0,"",YELLOW)


            if self.yAxisLabel == "%":
                str = f"{percent*100:.2f}%"
            else:
                str = f"{value:.2f}s"
            hoverFont = pygame.font.SysFont(None, 20)
            bars.append(Bar(bar,hoverFont.render(str,True,BLACK),i+1))

            if value > 0:
                if self.yAxisLabel == "%":
                    bottomLabel = font.render(f"{value}", True, BLACK)
                    screen.blit(bottomLabel, [x+(i+1)*(w/(numXLines-1))-5,yValue,bottomLabel.get_width(),bottomLabel.get_height()])
                else:
                    bottomLabel = font.render(f"{(value):.1f}", True, BLACK)
                    screen.blit(bottomLabel, [x+(i+1)*(w/(numXLines-1))-12,yValue,bottomLabel.get_width(),bottomLabel.get_height()])


            #draw x axis labels
            numLabel = font.render(f"{key}",True,BLACK)
            screen.blit(numLabel, [x+(i+1)*(w/(numXLines-1))-numLabel.get_width()/2,y+5,numLabel.get_width(),numLabel.get_height()])
            i+=1

def main():
    mainMenu()

pygame.init()
size = width, height = 700,700
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Catan Stats")

Player = namedtuple("Player", "name color turns averageTime")

TextBox = namedtuple("TextBox", "rect txt active")
Bar = namedtuple("Bar", "rect label num")
bars=[]
#TODO revamp labeling and data from dict to namedtuple
#GraphData = namedtuple("GraphData", "xAxisLabel yAxisLabel yData")


main()
