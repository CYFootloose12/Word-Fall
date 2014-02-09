#Connor Young
#Spring 2012 Term Project: Word Fall + ccyoung + section I

from Tkinter import *
import random
import string
import copy

def readFile(filename, mode="rt"): #Used to read the high score list
    # rt stands for "read text"   converts
    fin = contents = None
    try:
        fin = open(filename, mode)
        contents = fin.read()
    finally:
        if (fin != None): fin.close()
    return contents

def writeFile(filename, contents, mode="wt"):  #Used to rewrtie the high score
    # wt stands for "write text"         #list after the game is over.
    fout = None
    try:
        fout = open(filename, mode)
        fout.write(contents)
    finally:
        if (fout != None): fout.close()
    return True

def getHighScores(canvas):  #Is a function to retrieve the high score list
    canvas.data.contents = eval(readFile("highScoreList.txt"))
    addScoresToHighScoreList(canvas)  #adds the score to list after a game
    getScores(canvas)  #Retrieves the scores from the list 
    findIndex(canvas)  #Matches the names with their corresponding scores.
    update = repr(canvas.data.contents)  #The new high score list.
    writeFile("highScoreList.txt",update)  #Rewriting the high score list
    canvas.data.missedLetters = 0  #Reset missed letters so you are not adding
            #your name and score multiple times to the list for only one turn
                            

def getScores(canvas): #Extracts the scores from the list 
    canvas.data.scoresFromList = []  #and sorts them so that they can be matched
    scores = []  #up with their respective name
    for i in xrange(len(canvas.data.contents)):
        scores.append(canvas.data.contents[i][1])
    scores = sorted(scores)
    scores = scores[::-1]  #Reverses the order of the scores so that scores are
    canvas.data.scoresFromList = scores  #high to low

def addScoresToHighScoreList(canvas):  #Adds the score to high score list
    if canvas.data.missedLetters == 20:
        canvas.data.contents.append((canvas.data.currentPlayerName,
                                     canvas.data.score))

def findIndex(canvas):#Matches the names up with their corresponding scores.
    names = []
    for index in xrange(len(canvas.data.contents)):
        names.append(canvas.data.contents[index][0])
    canvas.data.orderNames = []  #List of the ordered names used to match up
    for i in xrange(len(canvas.data.scoresFromList)): #with their scores
        for j in xrange(len(names)):
            if canvas.data.scoresFromList[i] == canvas.data.contents[j][1]:
                canvas.data.orderNames.append(canvas.data.contents[j][0])

def mousePressed(canvas,event): #Used for mousepressing and buttons
    buttonWidth = canvas.data.buttonWidth
    buttonHeight = canvas.data.buttonHeight
    gameButtonWidth = canvas.data.gameButtonWidth
    gameButtonHeight = canvas.data.gameButtonHeight
    if canvas.data.state == "homePage":
        if ((event.x >= 200) and (event.x <= 200+buttonWidth) and
            (event.y >= 450) and (event.y <= 450+buttonHeight)):
            canvas.data.numberOfPlayers = 1  #One player mode
            canvas.data.state = "instructions"
        elif ((event.x >= 200) and (event.x <= 200+buttonWidth) and
              (event.y >= 600) and (event.y <= 600+buttonHeight)):
            canvas.data.state = "instructions"
            canvas.data.numberOfPlayers = 2  #Two player mode
    elif canvas.data.state == "instructions":
        if ((event.x >= 200) and (event.x <= 200+buttonWidth) and
            (event.y >= 450) and (event.y <= 450+buttonHeight)):
            init(canvas)  #restart the game
        if ((event.x >= 200) and (event.x <= 200+buttonWidth) and
            (event.y >= 600) and (event.y <= 600+buttonHeight)):
            canvas.data.state = "enterName" #This is so the user to update name
    elif ((canvas.data.state == "gamePlay") and (canvas.data.isPaused == False)
          and (canvas.data.isGameOver == False)):
        if ((event.x >= 10) and (event.x <= 10+gameButtonWidth) and
            (event.y >= 50) and (event.y <= 50+gameButtonHeight)):
            canvas.data.isPaused = True  #Pause feature
        elif ((event.x >= 10) and (event.x <= 10+gameButtonWidth) and
              (event.y >= 150) and (event.y <= 150+gameButtonHeight)):
            init(canvas) #Goes back to the main screen
    elif ((canvas.data.state == "gamePlay") and (canvas.data.isPaused == False)
          and (canvas.data.isGameOver == True)):
            if ((event.x >= 10) and (event.x <= 10+gameButtonWidth) and
                (event.y >= 50) and (event.y <= 50+gameButtonHeight)):
                initNewGame(canvas)  #Restarts the game for 
                canvas.data.currentPlayer = 1
                canvas.data.currentPlayerName = canvas.data.player1Name
            elif ((event.x >= 10) and (event.x <= 10+gameButtonWidth) and
              (event.y >= 150) and (event.y <= 150+gameButtonHeight)):
                init(canvas)
    elif canvas.data.state == "gamePlay" and canvas.data.isPaused == True:
        if ((event.x >= 10) and (event.x <= 10+gameButtonWidth) and
            (event.y >= 50) and (event.y <= 50+gameButtonHeight)):
            canvas.data.isPaused = False
        elif ((event.x >= 10) and (event.x <= 10+gameButtonWidth) and
              (event.y >= 150) and (event.y <= 150+gameButtonHeight)):
            init(canvas)  #Quits game
    redrawAll(canvas)

def delete(canvas,event):  #Used if the user wants to backspace
    if canvas.data.state == "enterName":
        if canvas.data.currentPlayer == 1 or canvas.data.currentPlayer == 2:        
            canvas.data.enteredName = canvas.data.enteredName[:-1]
    elif canvas.data.state == "gamePlay":
        canvas.data.currentWord = canvas.data.currentWord[:-1]
    
def submitEnter(canvas,event):  #Used if the player submits a word or name, or
    if ((canvas.data.state == "enterName") and  #the the player 2 needs to play
        (len(canvas.data.enteredName) != 0)): #during the intermission of the
        if canvas.data.numberOfPlayers == 1:  #two-player mode
            canvas.data.player1Name = canvas.data.enteredName
            canvas.data.currentPlayerName = canvas.data.player1Name
            canvas.data.enteredName = ""  #Entering player's name
            canvas.data.state = "gamePlay"            
        elif canvas.data.numberOfPlayers == 2:
            if canvas.data.currentPlayer == 1:
                canvas.data.player1Name = canvas.data.enteredName
                canvas.data.currentPlayerName = canvas.data.player1Name
                canvas.data.enteredName = ""   #first player entering name
                canvas.data.currentPlayer = 2
            elif canvas.data.currentPlayer == 2:
                canvas.data.player2Name = canvas.data.enteredName
                canvas.data.currentPlayer = 1
                canvas.data.currentPlayerName = canvas.data.player1Name
                canvas.data.enteredName = ""  #second player entering name
                canvas.data.state = "gamePlay"
    elif canvas.data.state == "gamePlay":
        if canvas.data.isGameOver == False:
            lettersOnScreen(canvas) #Going through the word verification process
            isWord(canvas)
            canvas.data.currentWord = ""  #Resets the word back to nothing.
        elif ((canvas.data.numberOfPlayers == 2) and
              (canvas.data.isGameOver == True) and
              (canvas.data.currentPlayer == 1)):
            canvas.data.currentPlayer = 2
            canvas.data.currentPlayerName = canvas.data.player2Name
            initNewGame(canvas)
            
def keyPressed(canvas,event): #Used if you need to type in a word.
    if (canvas.data.isGameOver == False) and (canvas.data.state == "gamePlay"):
        if ((event.keysym >= "a") and (event.keysym <= "z") and
            (len(canvas.data.currentWord) <= 10) and (len(event.keysym) == 1)):
            canvas.data.currentWord += event.keysym #adds the letter to the word
    elif (canvas.data.state == "enterName"):
        if ((event.keysym >= "A") and (event.keysym <= "z") and
            (len(canvas.data.enteredName) <= 10) and
            (len(event.keysym) == 1)):
            canvas.data.enteredName += event.keysym #adds the letter to the word

def lettersOnScreen(canvas):  #Checks if the letter is on the screen
    letterCircles = canvas.data.letterCircles
    copyOfLetters = copy.copy(letterCircles)
    count = 0  #This variable is to check if the each letter of the word
    for i in xrange(len(canvas.data.currentWord)):  #is on the screen
        current = canvas.data.currentWord[i]
        if copyOfLetters.count(current) > 0:
            count += 1
            copyOfLetters.remove(current)
    if count != len(canvas.data.currentWord): #If all the letters are on the
        canvas.data.currentWord = ""
    isWord(canvas)  #screen, then go on to check if its an actual word.
    
def isWord(canvas):  #checks if the word is in the dictionary
    dictionary = canvas.data.dictionary
    canvas.data.currentWord = canvas.data.currentWord + ("\n")
    if canvas.data.currentWord in dictionary:
        canvas.data.currentWord = canvas.data.currentWord[:-1]
        addToScore(canvas) #adds the score of the letters
        deleteWords(canvas)

def addToScore(canvas): #Similar to scrabble in the sense that the corresponding
    alphabet = canvas.data.alphabet #addition to your score in the game.
    currentWord = canvas.data.currentWord
    letterScores = canvas.data.letterScores
    for i in xrange(len(currentWord)):
        index = alphabet.index(currentWord[i])
        canvas.data.score += letterScores[index]
        if (((canvas.data.score/20) > canvas.data.scoreCounter) and
            (canvas.data.scoreCounter < 6)): #For each increase in 20 points,
            canvas.data.scoreCounter += 1 #the more frequent a letter fall 
            canvas.data.circleDrop -= 5  #becomes
    if len(canvas.data.currentWord) >= 5:#If the word that you have just
        canvas.data.longWords += 1 #submitted
        if canvas.data.longWords == 5:  #used to get back missing letters
            if canvas.data.missedLetters > 5:
                canvas.data.missedLetters -= 5
            else:
                canvas.data.missedLetters = 0
    elif len(canvas.data.currentWord) > 5:#If you lose the streak of 5 letters 
        canvas.data.longWords = 0  #or longer, reset the count to 0.

                    
def deleteWords(canvas):  #deletes the letters of the word that you typed in
    for i in xrange(len(canvas.data.currentWord)):#from the screen
        try:
            index = canvas.data.letterCircles.index(canvas.data.currentWord[i])
            canvas.data.fallingCircles.pop(index)
            canvas.data.letterCircles.remove(canvas.data.letterCircles[index])
        except:
            continue
    canvas.data.currentWord = ""

def circleFall(canvas): #This is the function that is making the cirlces fall
    fallingCircles = canvas.data.fallingCircles
    letterCircles = canvas.data.letterCircles
    for circle in fallingCircles: #For each circle on the board, 
        circle[1] += canvas.data.fallDistance   #make it fall by 10 pixels each time
        index = fallingCircles.index(circle) #Gets the letter of the circle 
        if circle[1] > canvas.data.canvasHeight - canvas.data.margin - 20:
            fallingCircles.remove(circle)  # Removes the circle once it has 
            letterCircles.remove(letterCircles[index]) #reached the bottom.
            canvas.data.missedLetters += 1
                                                   
def timerFired(canvas):
    if canvas.data.state == "gamePlay":
        canvas.data.counter += 1  #The counter is used for the falling letters
        if canvas.data.isPaused == True:
            canvas.data.pauseCounter += 1  #used to create a flashing pause
            canvas.data.pauseColor=\
                                     canvas.data.pauseColors\
                                     [(canvas.data.pauseCounter/5)%4]
    isGameOver(canvas)
    if ((canvas.data.state == "gamePlay") and
        (canvas.data.isGameOver == False) and
        (canvas.data.isPaused == False)):
        if canvas.data.counter % canvas.data.circleDrop == 0: #actual occurence 
            newFallingLetter(canvas)  #of the circle drop
        circleFall(canvas)  #Makes the circles fall
    redrawAll(canvas)
    delay = 50
    f = lambda: timerFired(canvas)
    canvas.after(delay,f)


def redrawAll(canvas):  #redraws the game and the screen
    canvas.delete(ALL)
    width = canvas.data.canvasWidth
    height = canvas.data.canvasHeight
    margin = canvas.data.margin
    if canvas.data.state == "gamePlay":
        drawScreen(canvas) #This is where the gameplay actually happens
        if canvas.data.isPaused == True:
            drawPauseScreen(canvas)
    elif canvas.data.state == "homePage":
        drawHomePage(canvas)
    elif canvas.data.state == "enterName":
        drawEnterNamePage(canvas)
    elif canvas.data.state == "instructions":
        drawInstructions(canvas)

def drawScreen(canvas): #Draws the gameplay part of my game.
    width = canvas.data.canvasWidth
    height = canvas.data.canvasHeight
    margin = canvas.data.margin
    cx = canvas.data.canvasWidth/2
    cy = canvas.data.canvasHeight/2
    buttonWidth = canvas.data.buttonWidth
    buttonHeight = canvas.data.buttonHeight
    buttonMargin = canvas.data.buttonMargin
    gameButtonWidth = canvas.data.gameButtonWidth
    gameButtonHeight = canvas.data.gameButtonHeight
    gameButtonMargin = canvas.data.gameButtonMargin
    fallingCircles = canvas.data.fallingCircles
    pauseColor = canvas.data.pauseColor
    canvas.create_rectangle(0,0,width,height,fill="green")
    canvas.create_text(width/2,50,text="Word Fall",
                       font=("Times New Romans",20))
    canvas.create_rectangle(margin+50,margin,width-50,
                            height-margin,fill="white")
    canvas.create_text(75,height-(3/2.0)*margin,text="Current player is:",
                       font=("Times New Romans",16))
    canvas.create_text(75,height-margin,
                       text=str(canvas.data.currentPlayerName),
                       font=("Times New Romans",16))
    canvas.create_text(75,height-2*margin, #Displays the score of the game.
                       text="Total Score: " + str(canvas.data.score),
                       font=("Times New Romans",16))  
    canvas.create_text(width/2-60,height-(margin/2),text="Enter a word:",font=
                           ("Helvetica", 20, "bold"))
    canvas.create_rectangle(width/2+10,height-(margin/2)-15,
                            width/2+150,height-(margin/2)+15,fill="orange")
    canvas.create_rectangle(10,150,10+gameButtonWidth,
                            150+gameButtonHeight,fill="black")
    canvas.create_rectangle(10+gameButtonMargin,150+gameButtonMargin,
                            10+gameButtonWidth-gameButtonMargin,
                            150+gameButtonHeight-gameButtonMargin,fill="red")
    canvas.create_text(10+(gameButtonWidth/2),150+(gameButtonHeight/2),
                       text="Quit",font=("Helvetica", 30, "bold"))
    canvas.create_rectangle(10,50,10+gameButtonWidth,50+gameButtonHeight,
                            fill="black")
    canvas.create_rectangle(10+gameButtonMargin,50+gameButtonMargin,
                            10+gameButtonWidth-gameButtonMargin,
                            50+gameButtonHeight-gameButtonMargin,fill="red")
    canvas.create_text(10+(gameButtonWidth/2),50+(gameButtonHeight/2),
                       text="Pause",font=("Helvetica", 30, "bold"))
    canvas.create_text(width/2+40,height-(margin/2),
                       text = str(canvas.data.currentWord),anchor=W)
    canvas.create_text(75,cy+margin/2,
                       text="Number of",
                       font=("Times New Romans",16))
    canvas.create_text(75,cy+margin,
                       text="Missed Letters:",
                       font=("Times New Romans",16))
    canvas.create_text(75,cy+(3/2.0)*margin,
                       text=str(canvas.data.missedLetters))
    drawCirclesFalling(canvas)
    drawGameOver(canvas)

def drawCirclesFalling(canvas):  #This is the function that draws the circles
    fallingCircles,radius = canvas.data.fallingCircles,canvas.data.radius
    letterCircles = canvas.data.letterCircles  #with their corresponding letter
    for circleCenter in fallingCircles:  #inside of them.
        (cx,cy) = circleCenter
        index = fallingCircles.index(circleCenter)
        canvas.create_oval(cx-radius,cy-radius,cx+radius,cy+radius,fill="cyan")
        canvas.create_text(cx,cy,text=str(canvas.data.letterCircles[index]))

def drawHighScoreList(canvas):
    gameButtonWidth = canvas.data.gameButtonWidth
    gameButtonHeight = canvas.data.gameButtonHeight
    gameButtonMargin = canvas.data.gameButtonMargin
    margin = canvas.data.margin
    canvas.create_rectangle(10,50,10+gameButtonWidth,50+gameButtonHeight,
                            fill="black")
    canvas.create_rectangle(10+gameButtonMargin,50+gameButtonMargin,
                            10+gameButtonWidth-gameButtonMargin,
                            50+gameButtonHeight-gameButtonMargin,fill="red")
    canvas.create_text(10+(gameButtonWidth/2),
                       50+(gameButtonHeight/2),text="Restart",
                       font=("Helvetica", 30, "bold"))
    cx = canvas.data.canvasWidth/2
    cy = canvas.data.canvasHeight/2
    canvas.create_text(cx,margin*(3/2.0),text="Game Over!",
                       font=("Helvetica", 40, "bold"))
    canvas.create_text(cx,margin*2,text="High Scores",
                       font=("Helvetica", 40, "bold"))
    for i in xrange(5):
        canvas.create_text(cx-margin,margin*(2+(1/2.0)*(1+i)),
                           text=str(i+1)+" "+str(canvas.data.orderNames[i]),
                           font=("Helvetica", 20, "bold"))
        canvas.create_text(cx+(margin/2),margin*(2+(1/2.0)*(1+i)),
                           text=str(canvas.data.scoresFromList[i]),
                           font=("Helvetica", 20, "bold"))

def drawGameOver(canvas):  #draws the game when it is over
    gameButtonWidth = canvas.data.gameButtonWidth
    gameButtonHeight = canvas.data.gameButtonHeight
    gameButtonMargin = canvas.data.gameButtonMargin
    margin = canvas.data.margin
    cx = canvas.data.canvasWidth/2  #placed in the middle of the window
    cy = canvas.data.canvasHeight/2 #placed in the middle of the window
    if canvas.data.isGameOver == True:
        if canvas.data.numberOfPlayers == 1:
            drawHighScoreList(canvas)
            canvas.create_text(cx,cy+(3/2.0)*(margin),
                               text="Congrats " + \
                               str(canvas.data.player1Name) + \
                               "!" + " You scored " + \
                               str(canvas.data.player1Score)+" points!",
                               font=("Helvetica", 30, "bold"))
        elif canvas.data.numberOfPlayers == 2:
            if canvas.data.currentPlayer == 1:
                canvas.create_text(cx,cy,text="Player 2, Press Enter to Play",
                                   font=("Helvetica", 30, "bold"))
            elif canvas.data.currentPlayer == 2:
                drawHighScoreList(canvas)
                if canvas.data.player1Score > canvas.data.player2Score:
                    canvas.create_text(cx,cy+(3/2.0)*(margin),
                                       text="Congrats " + \
                                       str(canvas.data.player1Name) + \
                                       "!" + " You're the winner!",
                                       font=("Helvetica", 30, "bold"))
                elif canvas.data.player1Score < canvas.data.player2Score:
                    canvas.create_text(cx,cy+(3/2.0)*(margin),
                                       text="Congrats " + \
                                       str(canvas.data.player2Name) + "! " + \
                                       " You're the winner!",
                                       font=("Helvetica", 30, "bold"))
                elif canvas.data.player1Score == canvas.data.player2Score:
                    canvas.create_text(cx,cy+(3/2.0)*(margin),text="Wow! " + \
                                       str(canvas.data.player1Name) + " and " +\
                                       str(canvas.data.player2Name) + " tied!",
                                       font=("Helvetica", 30, "bold"))
                    
def drawPauseScreen(canvas):  #draws the paused screen of the game
    gameButtonWidth = canvas.data.gameButtonWidth
    gameButtonHeight = canvas.data.gameButtonHeight
    gameButtonMargin = canvas.data.gameButtonMargin
    if canvas.data.isPaused == True:  #If the game is paused, draw these things
        cx = canvas.data.canvasWidth/2
        cy = canvas.data.canvasHeight/2
        canvas.create_text(cx, cy, text="Game Paused",
                           font=("Helvetica", 32,"bold"),
                           fill=canvas.data.pauseColor)
        canvas.create_rectangle(10,50,10+gameButtonWidth,50+gameButtonHeight,
                                fill="black")
        canvas.create_rectangle(10+gameButtonMargin,50+gameButtonMargin,
                                10+gameButtonWidth-gameButtonMargin,
                                50+gameButtonHeight-gameButtonMargin,
                                fill="red")
        canvas.create_text(10+(gameButtonWidth/2),50+(gameButtonHeight/2),
                           text="Resume",font=("Helvetica", 26, "bold"))

def drawInstructions(canvas):  #draws the intructions of the game
    width = canvas.data.canvasWidth
    height = canvas.data.canvasHeight
    buttonWidth = canvas.data.buttonWidth
    buttonHeight = canvas.data.buttonHeight
    buttonMargin = canvas.data.buttonMargin
    canvas.create_rectangle(0,0,width,height,fill="green")
    canvas.create_text(350,20,text="INSTRUCTIONS TO WORD FALL",
                       font=("Helvetica", 20, "bold"))
    canvas.create_text(100,50,
                       text="-Construct a word using the letters on the screen"+
                        " and press enter to submit the word.", anchor=W)
    canvas.create_text(100,75,text="-Your words will range from one letter " +
                        " to ten letters in length.",anchor=W)
    canvas.create_text(100,100,text="-The number of points you receive " +
                        "depends on the letters of the word. The",anchor=W)
    canvas.create_text(100,125,text=" scoring system is based on the "+
                        "Scrabble scoring system.", anchor=W)
    canvas.create_text(100,150,text="-As the game progresses, letters " +
                       "will appear more quickly on the screen.",anchor=W)
    canvas.create_text(100,175,text="-If you are allowed to miss twenty "+
                        "letters during your gameplay with Word Fall.",anchor=W)
    canvas.create_text(100,200,text="-If you score on five words that "+
                        "are longer than five letters in a row, then",anchor=W)
    canvas.create_text(100,225,text=" you will get back, five of the "+
                        "missed Letters. If you have missed five or less",
                       anchor=W)
    canvas.create_text(100,250,text=" letters, then your number of " +
                        "missed letters will reset to zero for you.",anchor=W)
    image = PhotoImage(file="fallingLetters.gif")  #image of a bunch of letters
    canvas.data.image = image
    canvas.create_image(350,350, image=canvas.data.image)
    canvas.create_rectangle(200,450,200+buttonWidth,450+buttonHeight,
                            fill="black")
    canvas.create_rectangle(200+buttonMargin,450+buttonMargin,
                            200+buttonWidth-buttonMargin,
                            450+buttonHeight-buttonMargin,fill="red")
    canvas.create_text(200+(buttonWidth/2),450+(buttonHeight/2),
                       text="Main Menu",font=("Helvetica", 40, "bold"))
    canvas.create_rectangle(200,600,200+buttonWidth,600+buttonHeight,
                            fill="black")
    canvas.create_rectangle(200+buttonMargin,600+buttonMargin,
                            200+buttonWidth-buttonMargin,
                            600+buttonHeight-buttonMargin,fill="red")
    canvas.create_text(200+(buttonWidth/2),600+(buttonHeight/2),
                       text="Let's Play",font=("Helvetica", 40, "bold"))

def drawEnterNamePage(canvas):  #Creates the page needed to enter your name 
    width = canvas.data.canvasWidth   #into the computer
    height = canvas.data.canvasHeight
    margin = canvas.data.margin
    buttonWidth = canvas.data.buttonWidth
    buttonHeight = canvas.data.buttonHeight
    buttonMargin = canvas.data.buttonMargin
    margin = canvas.data.margin
    textBoxWidth = canvas.data.textBoxWidth
    textBoxHeight = canvas.data.textBoxHeight
    canvas.create_rectangle(0,0,width,height,fill="green")
    canvas.create_text(width/2,height-(5*margin),
                       text="Enter name here player "+\
                       str(canvas.data.currentPlayer),
                       font=("Helvetica", 40, "bold"))
    canvas.create_text(width/2,height-(4*margin),text="and press Enter:",
                       font=("Helvetica", 40, "bold"))
    canvas.create_rectangle(width/2-(textBoxWidth/2),
                            height-(3*margin)-(textBoxHeight/2),
                            width/2+(textBoxWidth/2),
                            height-(3*margin)+(textBoxHeight/2),fill="orange")
    canvas.create_text(width/2,height-(3*margin),
                       text=str(canvas.data.enteredName),
                       font=("Helvetica", 40, "bold"))
                                              
    
def drawHomePage(canvas):  #draws the homepage
    width = canvas.data.canvasWidth
    height = canvas.data.canvasHeight
    buttonWidth = canvas.data.buttonWidth
    buttonHeight = canvas.data.buttonHeight
    buttonMargin = canvas.data.buttonMargin
    canvas.create_rectangle(0,0,width,height,fill="green")
    canvas.create_text(350,100,text="W    R ",  
                       font=("Helvetica", 60, "bold")) #title on homepage
    canvas.create_text(350,140,text="      O    D",
                       font=("Helvetica", 60, "bold")) #title on homepage
    canvas.create_text(350,220,text="F    L ",
                       font=("Helvetica", 60, "bold")) #title on homepage
    canvas.create_text(350,260,text="      A    L",
                       font=("Helvetica", 60, "bold")) #title on homepage
    canvas.create_rectangle(200,450,200+buttonWidth,
                            450+buttonHeight,fill="black")
    canvas.create_rectangle(200+buttonMargin,450+buttonMargin,
                            200+buttonWidth-buttonMargin,
                            450+buttonHeight-buttonMargin,fill="red")
    canvas.create_text(200+(buttonWidth/2),450+(buttonHeight/2),
                       text="Single Player",font=("Helvetica", 40, "bold"))
    canvas.create_rectangle(200,600,200+buttonWidth,
                            600+buttonHeight,fill="black")
    canvas.create_rectangle(200+buttonMargin,600+buttonMargin,
                            200+buttonWidth-buttonMargin,
                            600+buttonHeight-buttonMargin,fill="red")
    canvas.create_text(200+(buttonWidth/2),600+(buttonHeight/2),
                       text="Two Player",font=("Helvetica", 40, "bold"))

def chooseWord(canvas):  #This function chooses a random word from a list of 
    listOfWords = canvas.data.listOfWords  #words from the dictionary
    index1 = random.randint(0,len(listOfWords)-1)
    canvas.data.word1 = listOfWords[index1]
    while (len(canvas.data.word1[:-2]) <= 2): 
        index1 = random.randint(0,len(listOfWords))
        canvas.data.word1 = listOfWords[index1]
    canvas.data.word1 = canvas.data.word1[:-2] #Because of the way the
                    #dictionary was implemented, there is a /n at the end of
                    #string. Thus, we simply need to cut of the newline part
                    #off of the word.
        
def splitUpWord(canvas): #Splits up the word choosen by the chooseWord function
    splitUpLetters = canvas.data.splitUpLetters
    for i in xrange(len(canvas.data.word1)):  #word1 is now a list of letters as
        splitUpLetters.append(canvas.data.word1[i]) # the list splitUpLetters
    

def chooseFallingLetter(canvas):#Chooses the function for its respective circle
    letterCircles = canvas.data.letterCircles
    splitUpLetters = canvas.data.splitUpLetters
    if len(splitUpLetters) == 0:
        chooseWord(canvas)
        splitUpWord(canvas)
    index = random.randint(0,len(splitUpLetters)-1)
    letterCircles.append(splitUpLetters[index])
    splitUpLetters.pop(index)

def createFallingPlace(canvas):  #Creates the coordinates for the circle to fall
    margin = canvas.data.margin  #for each letter
    width = canvas.data.canvasWidth
    radius = canvas.data.radius
    fallingCircles = canvas.data.fallingCircles
    if canvas.data.side == "left":  #Makes sure that the letters alterante sides
        xCoord = (random.randint(margin+100,width/2-(canvas.data.radius/2)))
        canvas.data.side = "right"
    else:#No overlapping of letters should exist because they are alternating
        xCoord = (random.randint(width/2+(canvas.data.radius/2)+20,width-100))
        canvas.data.side = "left"            #sides
    yCoord = margin + canvas.data.radius
    newCircleCenter = [xCoord,yCoord]
    fallingCircles.append(newCircleCenter)    

def newFallingLetter(canvas):  #Creates the new falling letter with the help of 
    chooseFallingLetter(canvas)  #a few helper functions
    createFallingPlace(canvas)

def isGameOver(canvas):  #If the person has missed more than 20 letters 
    if canvas.data.missedLetters == 20: #the game is over
        canvas.data.isGameOver = True
        getHighScores(canvas)
        if canvas.data.numberOfPlayers == 1:
            canvas.data.player1Score = canvas.data.score
        elif ((canvas.data.numberOfPlayers == 2) and
              (canvas.data.currentPlayer == 1)):
            canvas.data.player1Score = canvas.data.score
        elif ((canvas.data.numberOfPlayers == 2) and
              (canvas.data.currentPlayer == 2)):
            canvas.data.player2Score = canvas.data.score

def initNewGame(canvas):  #Used to restart game for one or two player mode
    if ((canvas.data.numberOfPlayers == 2) and (canvas.data.currentPlayer ==1)):
         if canvas.data.isGameOver == True:
            canvas.data.currentPlayer = 2
            canvas.data.currentPlayerName = canvas.data.player2Name
         elif canvas.data.isGameOver == False:
            canvas.data.currentPlayer = 1
            canvas.data.currentPlayerName = canvas.data.player1Name
    canvas.data.score = 0
    canvas.data.scoreCounter = 0
    canvas.data.missedLetters = 0 #
    canvas.data.isGameOver = False  #Turns on when game is over
    canvas.data.isPaused = False
    canvas.data.side = "right"  #The first circle will fall on the right side.
    canvas.data.counter = 0
    canvas.data.radius = 20
    canvas.data.pauseCounter = 0
    canvas.data.pauseColor = "black"
    canvas.data.pauseColors = ["black","purple","orange","red"]
    canvas.data.splitUpLetters = []
    canvas.data.word1 = ""
    canvas.data.circleDrop = 40  # Every 25 timerfired cycles, a circle is made
    canvas.data.fallDistance = 2
    canvas.data.fallingCircles = []  #list of the circles that are falling
    canvas.data.letterCircles = [] #list of the letters of those circles
    canvas.data.currentWord = ""
    canvas.data.enteredName = ""
    redrawAll(canvas)

def init(canvas):
    canvas.data.score = 0  #The current score of who is playing
    canvas.data.player1Score = 0  
    canvas.data.player2Score = 0
    canvas.data.scoreCounter = 0  #As it increases, words fall more frequently
    canvas.data.longWords = 0  #This is the counter for the bonus points
    canvas.data.state = "homePage"  #This is the state of the game at the start
    canvas.data.currentPlayer = 1
    canvas.data.currentPlayerName = ""
    canvas.data.longWord = 0  #if his reaches five, then you get back five
    canvas.data.player1Name = ""              #missed letters
    canvas.data.player2Name = ""
    canvas.data.numberOfPlayers = 0  #user chooses which game mode he/she wants
    canvas.data.missedLetters = 0
    canvas.data.isGameOver = False  #Turns on when 
    canvas.data.isPaused = False
    canvas.data.buttonWidth = 300  #dimensions for button that is used during
    canvas.data.buttonHeight = 100 #a non-game play state
    canvas.data.buttonMargin = 20
    canvas.data.gameButtonWidth = 125 #dimensions for button that is used during
    canvas.data.gameButtonHeight = 80  #gameplay
    canvas.data.gameButtonMargin = 10
    canvas.data.textBoxWidth = 250
    canvas.data.textBoxHeight = 80
    canvas.data.side = "right"  #The first circle will fall on the right side.
    canvas.data.counter = 0  #used to calculate when a circle should be dropped
    canvas.data.radius = 20  #radius of the circle
    canvas.data.pauseCounter = 0  #Used to have the changing colors for pause
    canvas.data.pauseColor = "black"
    canvas.data.pauseColors = ["black","purple","orange","red"]
    canvas.data.splitUpLetters = []  #used for splitUpWord
    canvas.data.word1 = "" #used
    canvas.data.circleDrop = 40  # Every 25 timerfired cycles, a circle is made
    canvas.data.fallDistance = 2  #How far the circle falls every timerFired
    canvas.data.contents = []  #high score list retrieved from the file
    canvas.data.orderNames = [] #ordered names of the high scored list
    canvas.data.currentPlayer = 1
    canvas.data.scoresFromList = []
    canvas.data.fallingCircles = []  #list of the circles that are falling
    canvas.data.letterCircles = [] #list of the letters of those circles
    canvas.data.letterScores = [
   #  a, b, c, d, e, f, g, h, i, j, k, l, m
      1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3,
   #  n, o, p, q, r, s, t, u, v, w, x, y, z
      1, 1, 3,10, 1, 1, 1, 1, 4, 4, 8, 4,10
   ]  #scrabble letter scores that are then added to the score of the game.
    canvas.data.listOfWords = (open('allWords.txt')).readlines()
    canvas.data.dictionary = set((open('allWords.txt')).readlines())
    canvas.data.alphabet = list(string.ascii_lowercase)
    canvas.data.currentWord = ""
    canvas.data.enteredName = ""
    redrawAll(canvas)

def run():  #Runs the game 
    root = Tk()
    margin = 100
    canvasWidth = 700
    canvasHeight = 800
    canvas = Canvas(root,width=canvasWidth,height=canvasHeight)
    canvas.pack()
    class Struct: pass
    canvas.data = Struct()
    canvas.data.margin = margin
    canvas.data.canvasWidth = canvasWidth
    canvas.data.canvasHeight = canvasHeight
    root.bind("<Button-1>",lambda event: mousePressed(canvas,event))
    root.bind("<Key>", lambda event: keyPressed(canvas,event))
    root.bind("<Return>", lambda event: submitEnter(canvas,event))
    root.bind("<BackSpace>", lambda event: delete(canvas,event))
    init(canvas)
    timerFired(canvas)
    root.mainloop()

run()
