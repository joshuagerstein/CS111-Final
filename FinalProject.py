import graphics
import math
import random
'''
This program defines the classes and functions necessary to create a game of
mastermind. This game can have the user either set the code for the computer
to solve, or try to solve a code set by the computer. There is also an option
to have either 8, 10, or 12 turns. The AI for this program follows the 5 guess
algorithm created by Donald Knuth, as explained here:
https://en.wikipedia.org/wiki/Mastermind_(board_game)#Five-guess_algorithm
Created by: Anna Stengle Johnson, Josh Gerstein, and Julia Miller.
CS111, Fall 2015
'''


def circleContains(self, p):
    ''' This function checks to see if a point is in a circle. It is used as
    a __contains__ method for graphics.Circle objects.
    '''
    # If p is not a point, return false
    if type(p) != graphics.Point:
        return False
    # If the point is in the circle, return true
    if ((p.getX() - self.getCenter().getX()) ** 2 +
            (p.getY() - self.getCenter().getY()) ** 2) <= self.getRadius()**2:
        return True
    return False


graphics.Circle.__contains__ = circleContains


class ColorOptions:
    ''' An object that allows users to input their color selections. '''
    def __init__(self, bottomLeft, colorList):
        '''Constructor that creates all the elements of the color selecting
        box based on the given bottom left corner point and the list of colors
        to be used.
        '''
        topRight = graphics.Point(bottomLeft.getX() + 150,
                                  bottomLeft.getY() + 200)
        self.container = graphics.Rectangle(bottomLeft, topRight)
        self.container.setFill('saddle brown')
        self.colorDots = []
        self.colorList = colorList
        # Create colored dot/buttons
        for i in range(len(self.colorList)):
            xAdjust = (i % 3) * 50 + 25
            yAdjust = (i // 3) * 35 + 145
            center = graphics.Point(bottomLeft.getX() + xAdjust,
                                    bottomLeft.getY() + yAdjust)
            self.colorDots.append(graphics.Circle(center, 10))
            self.colorDots[-1].setFill(self.colorList[i])
        self.entryPegList = []
        # Create the dots used to represent the code user enters
        for i in range(4):
            xAdjust = (i * 33) + 25
            center = graphics.Point(bottomLeft.getX() + xAdjust,
                                    bottomLeft.getY() + 35)
            self.entryPegList.append(graphics.Circle(center, 10))
            self.entryPegList[-1].setFill('sienna4')
        # Create delete and enter buttons
        enterPoint1 = graphics.Point(bottomLeft.getX() + 10,
                                     bottomLeft.getY() + 70)
        enterPoint2 = graphics.Point(bottomLeft.getX() + 70,
                                     bottomLeft.getY() + 120)
        delPoint1 = graphics.Point(bottomLeft.getX() + 80,
                                   bottomLeft.getY() + 70)
        delPoint2 = graphics.Point(bottomLeft.getX() + 140,
                                   bottomLeft.getY() + 120)
        self.enterButton = TextButton(enterPoint1, enterPoint2, 'Enter',
                                      'medium sea green')
        self.delButton = TextButton(delPoint1, delPoint2, 'Delete',
                                    'medium sea green')

    def draw(self, window):
        ''' Draws the color option box in the given window. '''
        self.window = window
        self.container.draw(window)
        # Draw all the colored dots and entry pegs
        for circle in self.colorDots + self.entryPegList:
            circle.draw(window)
        # Draw the delete button and enter button
        self.delButton.draw(window)
        self.enterButton.draw(window)

    def getInput(self):
        ''' Waits for a click, then checks if the click was made in any of the
        buttons in the object. Returns either an integer or string
        corresponding to the button that was clicked on. Loops until one of the
        buttons is clicked.
        '''
        while True:
            click = self.window.getMouse()
            # If enter is clicked return enter
            if click in self.enterButton:
                return 'enter'
            # If delete is clicked return delete
            elif click in self.delButton:
                return 'delete'
            for i in range(len(self.colorDots)):
                # We defined __contains__ for graphics.Circle objects above,
                # which is why this line works:
                if click in self.colorDots[i]:
                    return i

    def getColors(self):
        ''' Gets user input for a 4 color code using getInput. '''
        entryColorList = [None] * 4
        curSpot = 0
        while True:
            action = self.getInput()
            # If a color dot is clicked, change the current dot/peg to be that
            # color.
            if type(action) == int and curSpot <= 3:
                entryColorList[curSpot] = action
                self.entryPegList[curSpot].setFill(self.colorList[action])
                curSpot += 1
            # If the user clicks the delete button, change the color of the
            # previous spot back to sienna4 and change that to the current spot
            elif action == 'delete' and curSpot > 0:
                curSpot -= 1
                entryColorList[curSpot] = None
                self.entryPegList[curSpot].setFill('sienna4')
            # If the user clicks enter, change all the dots back to sienna4
            # and return the color list.
            elif action == 'enter' and curSpot == 4:
                for i in range(4):
                    self.entryPegList[i].setFill('sienna4')
                return entryColorList


class TextButton:
    ''' Button class that contains a rectangle object and text object. '''
    def __init__(self, p1, p2, text, color):
        ''' Constructor that creates rectangle and text based on given points
        and given text.
        '''
        self.color = color
        self.rectangle = graphics.Rectangle(p1, p2)
        self.rectangle.setFill(color)
        self.text = graphics.Text(self.rectangle.getCenter(), text)

    def __contains__(self, p):
        ''' Boolean function, returns true if given point is in the button's
        rectangle, otherwise false.
        '''
        if type(p) != graphics.Point:
            return False
        xMax = max(self.rectangle.getP1().getX(),
                   self.rectangle.getP2().getX())
        xMin = min(self.rectangle.getP1().getX(),
                   self.rectangle.getP2().getX())
        yMax = max(self.rectangle.getP1().getY(),
                   self.rectangle.getP2().getY())
        yMin = min(self.rectangle.getP1().getY(),
                   self.rectangle.getP2().getY())
        if (p.getX() >= xMin and p.getX() <= xMax and
                p.getY() >= yMin and p.getY() <= yMax):
            return True
        return False

    def draw(self, graphwin):
        ''' Draws the rectangle and text on the given window. '''
        self.rectangle.draw(graphwin)
        self.text.draw(graphwin)

    def undraw(self):
        ''' Undraws both the rectangle and text. '''
        self.text.undraw()
        self.rectangle.undraw()

    def getText(self):
        ''' Returns the string that is being displayed on the button. '''
        return self.text.getText()

    def setText(self, text):
        ''' Sets the string that is being displayed on the button. '''
        self.text.setText(text)

    def setTextSize(self, textSize):
        ''' Sets the text's size. '''
        self.text.setSize(textSize)

    def setTextColor(self, textColor):
        ''' Sets the text's color. '''
        self.text.setTextColor(textColor)


class Row:
    ''' This class deals with all the functions required to create a row of
    pegs and to manipulate it, including changing the colors of the pegs and
    setting feedback.
    '''
    def __init__(self, bottomLeft, pegColorList, colorList, covered=False):
        '''initializes variables that will be used throughout this class,
        including whether or not the solution row is covered and if there will
        be a feedback container.
        '''
        self.pegColorList = pegColorList
        self.bottomLeft = bottomLeft
        self.colorList = colorList
        self.covered = covered
        topRight = graphics.Point(self.bottomLeft.getX() + 300,
                                  self.bottomLeft.getY() + 80)
        self.container = graphics.Rectangle(bottomLeft, topRight)
        self.container.setFill('DarkOrange4')
        self.createPegContainer()
        if not self.covered:
            self.cover = None
            self.createFeedbackContainer()
        else:
            self.feedbackContainer = None

    def setPegColorList(self, pegColorList):
        '''This function changes the color of a row of pegs to display the
        colors in pegColorList.
        '''
        self.pegColorList = pegColorList
        # Iterates through pegColorList, setting each peg in pegList to its
        # corresponding color in pegColorList.
        for i in range(len(self.pegList)):
            self.pegList[i].setFill(self.colorList[self.pegColorList[i]])

    def createPegContainer(self):
        '''This function creates a rectangle with a row of circles (also
        referred to as "pegs") and, if the player option is human, it covers
        the top code row. The spacing of the pegs can change depending on the
        number of pegs that there are, though that never changes in the
        current code.
        '''
        # Set the points for the rectangle
        pegBottomLeft = graphics.Point(self.bottomLeft.getX() + 10,
                                       self.bottomLeft.getY() + 10)
        pegTopRight = graphics.Point(self.bottomLeft.getX() + 230,
                                     self.bottomLeft.getY() + 70)
        # Draw and color the rectangle
        self.pegContainer = graphics.Rectangle(pegBottomLeft, pegTopRight)
        self.pegContainer.setFill('sienna4')
        self.pegList = []
        # Draws each "peg" for however many pegs there are, in this game it
        # remains 4, and either colors them the appropriate color or sets the
        # color to be the same as the box it is in.
        for i in range(len(self.pegColorList)):
            centerX = self.bottomLeft.getX() + 50 * (i + 1)
            centerY = self.bottomLeft.getY() + 40
            circle = graphics.Circle(graphics.Point(centerX, centerY), 10)
            self.pegList.append(circle)
            if type(self.pegColorList[i]) == int:
                self.pegList[-1].setFill(self.colorList[self.pegColorList[i]])
            else:
                self.pegList[-1].setFill('sienna4')
        # If the row is covered, cover it with a rectangle of the same color as
        # the rectangle containing the pegs.
        if self.covered:
            self.cover = graphics.Rectangle(pegBottomLeft, pegTopRight)
            self.cover.setFill('sienna4')

    def createFeedbackContainer(self):
        '''This function creates a rectangle that contains pegs to display
        feedback. The spacing of the pegs can change depending on the number
        of pegs that there are, though that never changes in the current code.
        '''
        # Set points for the container
        feedbackBottomLeft = graphics.Point(self.bottomLeft.getX() + 240,
                                            self.bottomLeft.getY() + 10)
        feedbackTopRight = graphics.Point(self.bottomLeft.getX() + 290,
                                          self.bottomLeft.getY() + 70)
        # Create the rectangular container
        self.feedbackContainer = graphics.Rectangle(feedbackBottomLeft,
                                                    feedbackTopRight)
        self.feedbackContainer.setFill('sienna4')
        self.feedbackList = []
        numPegs = len(self.pegList)
        # Set the spacing of the pegs-- currently not that important since the
        # number of pegs never changes, but this makes it so that there is even
        # spacing if the number of pegs ever changed.
        feedbackPerRow = math.ceil(math.sqrt(numPegs))
        width = abs(self.feedbackContainer.getP1().getX() -
                    self.feedbackContainer.getP2().getX())
        height = abs(self.feedbackContainer.getP1().getY() -
                     self.feedbackContainer.getP2().getY())
        xSpacing = (width - 20) / (feedbackPerRow - 1)
        ySpacing = (height - 20) / math.ceil(numPegs / feedbackPerRow - 1)
        i = 0
        # Loop to draw the pegs
        while i < numPegs:
            for j in range(feedbackPerRow):
                x = (min(self.feedbackContainer.getP1().getX(),
                         self.feedbackContainer.getP2().getX()) +
                     10 + j * xSpacing)
                y = (max(self.feedbackContainer.getP1().getY(),
                         self.feedbackContainer.getP2().getY()) -
                     10 - (i // feedbackPerRow) * ySpacing)
                feedbackPeg = graphics.Circle(graphics.Point(x, y), 5)
                # Fill each peg with the same color as the container
                feedbackPeg.setFill('sienna4')
                self.feedbackList.append(feedbackPeg)
                i += 1
                if i >= numPegs:
                    break

    def draw(self, graphwin):
        '''This function draws the container, peg container, pegs, and feedback
        container if a feedback container is being used.
        '''
        # Draw the container and peg container
        self.container.draw(graphwin)
        self.pegContainer.draw(graphwin)
        # If the code is not covered, draw the feedback container with feedback
        # and the pegs.
        if not self.covered:
            self.feedbackContainer.draw(graphwin)
            for feedback in self.feedbackList:
                feedback.draw(graphwin)
            # Draw all the pegs
            for peg in self.pegList:
                peg.draw(graphwin)
        # If there is a cover draw the cover
        else:
            self.cover.draw(graphwin)

    def undraw(self):
        '''This function undraws what was drawn in the draw function-- the
        rectangle container and peg container.
        '''
        self.container.undraw()
        self.pegContainer.undraw()
        # If the code is not covered, undraw the feedback container
        if not self.covered:
            self.feedbackContainer.undraw()
            for feedback in self.feedbackList:
                feedback.undraw()
        # If the code is covered, undraw the cover
        else:
            self.cover.undraw()
        # Undraw all the pegs
        for peg in self.pegList:
            peg.undraw()

    def setFeedback(self, red, white):
        '''This function displays red and white pegs according to the given
        feedback (as red, white).
        '''
        # Color pegs red
        for i in range(red):
            self.feedbackList[i].setFill('red')
        # Color pegs white
        for i in range(white):
            self.feedbackList[i + red].setFill('white')

    def uncover(self, graphwin):
        '''This function uncovers any code that has been covered by a "cover",
        and it draws the pegs that were covered.
        '''
        if self.cover:
            self.cover.undraw()
        for peg in self.pegList:
            peg.draw(graphwin)
        self.covered = False


class Mastermind:
    ''' This class holds all the functions immediately necessary to play the
    Mastermind game. This class includes functions to create opening displays,
    gather information that will affect how the game will be played (player
    mode and the number of turns) This class also holds functions that give
    feedback on guesses and allow the user to take turns and make guesses.
    '''
    def __init__(self):
        '''This function initializes variables that will be used throughout
        the Mastermind class. It also calls the options function and opening
        picture and calls the code generator to create a list of all possible
        codes.
        '''
        self.colorList = ['SeaGreen3', 'firebrick2', 'dark orange', 'yellow',
                          'snow', 'DodgerBlue2']
        self.rows = []
        self.lastGuess = None
        self.possibleCodes = []
        # Calls the code generator to create a list of all possible codes
        gen = self.codeGenerator()
        for i in range(6 ** 4):
            self.possibleCodes.append(next(gen))
        self.remainingCodes = self.possibleCodes.copy()
        self.possibleFeedback = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                                 (1, 0), (1, 1), (1, 2), (1, 3), (2, 0),
                                 (2, 1), (2, 2), (3, 0), (3, 1), (4, 0)]
        # Displays opening picture
        self.opening = self.openingPicture()
        # Displays the options and saves what that function returns in
        # self.options.
        self.optionWin = graphics.GraphWin(title='Mastermind Options',
                                           width=300, height=300)
        self.optionWin.setCoords(0, 0, 300, 300)
        self.optionWin.setBackground('saddle brown')
        self.options = self.getOptions()
        self.optionWin.close()

    def openingPicture(self):
        '''This function displays the mastermind logo before the game starts
        '''
        # Set the opening pictures
        openingPicture = graphics.Image(graphics.Point(200, 55),
                                        'mastermind.gif')
        # Create a window for this picture
        openingWin = graphics.GraphWin('Mastermind', 400, 110)
        openingWin.setCoords(0, 0, 400, 110)
        # Display this picture
        openingPicture.draw(openingWin)
        # Close window when the user clicks
        openingWin.getMouse()
        openingWin.close()

    def getOptions(self):
        '''This function creates buttons to get user input for which mode to
        play the game in, the user guessing the code created by the computer or
        the computer guessing the code created by the user, and how many turns
        will be played, 8, 10, or 12.
        '''
        options = {}
        # Create the first question, which mode will be played
        questionAnchor = graphics.Point(150, 225)
        questionText = graphics.Text(questionAnchor,
                                     'What mode would you like to play?')
        # Create two buttons, a guess code and a create code option, side by
        # side.
        humanPoint1 = graphics.Point(40, 150)
        humanPoint2 = graphics.Point(140, 100)
        computerPoint1 = graphics.Point(160, 150)
        computerPoint2 = graphics.Point(260, 100)
        humanButton = TextButton(humanPoint1, humanPoint2, 'Guess Code',
                                 'medium sea green')
        computerButton = TextButton(computerPoint1, computerPoint2,
                                    'Create Code', 'medium sea green')
        # Draw question and buttons
        questionText.draw(self.optionWin)
        humanButton.draw(self.optionWin)
        computerButton.draw(self.optionWin)
        # Wait until one of the buttons is clicked, and set the player option
        # to either human or computer depending on who will be guessing the
        # code.
        while True:
            click = self.optionWin.getMouse()
            if click in humanButton:
                options['player'] = 'Human'
                break
            elif click in computerButton:
                options['player'] = 'Computer'
                break
        # Undraw the human and computer buttons
        humanButton.undraw()
        computerButton.undraw()
        # Create three side by side buttons for the three turn choices
        eightPoint1 = graphics.Point(50, 150)
        eightPoint2 = graphics.Point(100, 100)
        tenPoint1 = graphics.Point(125, 150)
        tenPoint2 = graphics.Point(175, 100)
        twelvePoint1 = graphics.Point(200, 150)
        twelvePoint2 = graphics.Point(250, 100)
        eightButton = TextButton(eightPoint1, eightPoint2, 'Eight',
                                 'medium sea green')
        tenButton = TextButton(tenPoint1, tenPoint2, 'Ten',
                               'medium sea green')
        twelveButton = TextButton(twelvePoint1, twelvePoint2, 'Twelve',
                                  'medium sea green')
        # Set the text of the question to ask how many turns there should be
        questionText.setText('How many turns would you like to have?')
        # Draw the buttons
        eightButton.draw(self.optionWin)
        tenButton.draw(self.optionWin)
        twelveButton.draw(self.optionWin)
        # Wait until one of the buttons is clicked, and set the turns option to
        # either 8, 10, or 12 depending on which button is clicked.
        while True:
            click = self.optionWin.getMouse()
            if click in eightButton:
                options['level'] = '8'
                break
            elif click in tenButton:
                options['level'] = '10'
                break
            elif click in twelveButton:
                options['level'] = '12'
                break
        # Return the options selected.
        return options

    def chooseComputerCode(self):
        ''' This function allows the user to choose the code the computer
        will try to solve. It returns a list of colors that respond to indexes
        like getColors() in codeColorOptions.
        '''
        # Create a new window
        codeChoiceWin = graphics.GraphWin('Code Choice', 150, 200)
        codeChoiceWin.setCoords(0, 0, 150, 200)
        codeChoiceWin.setBackground('saddle brown')
        # Create a message asking for the code
        text = ('Click to choose the\ncolor code you\nwould like the\n' +
                'computer to attempt.')
        message = graphics.Text(graphics.Point(75, 100), text)
        message.draw(codeChoiceWin)
        # Get the colors selected by the user and display them
        codeChoiceWin.getMouse()
        bottomLeft = graphics.Point(0, 0)
        codeColorOptions = ColorOptions(bottomLeft, self.colorList)
        codeColorOptions.draw(codeChoiceWin)
        colorCode = codeColorOptions.getColors()
        # Close the window and return the code
        codeChoiceWin.close()
        return colorCode

    def initPlayWin(self, numRows):
        ''' This creates a window in which to play the game Mastermind based on
        how many turns the user has selected to have. This function only draws
        the window, the rows in it, and the covered, or uncovered code,
        depending on whether it is the human player mode or the computer player
        mode.
        '''
        # Add one to numRows so that there will be room for the set code
        # solution at the top.
        numRows += 1
        # Create a window, height based on the numRows, which is number of
        # turns + 1.
        self.playWin = graphics.GraphWin(title='Mastermind Game',
                                         width=400, height=64 * numRows)
        self.playWin.setCoords(0, 0, 500, 80 * numRows)
        self.playWin.setBackground('saddle brown')
        # Create empty rows for pegs
        for i in range(int(self.options['level'])):
            yPoint = i * 80
            row = Row(graphics.Point(0, yPoint), [None] * 4, self.colorList)
            row.draw(self.playWin)
            self.rows.append(row)
        # If the player is human, create the color options box where the human
        # player will choose which code to guess.
        # Also creates a box with the solution code at the top that is covered
        # (so the user can't see the solution).
        if self.options['player'] == 'Human':
            # Create color options box
            colorOptionsBottomLeft = graphics.Point(325, 0)
            self.colorOptionsBox = ColorOptions(colorOptionsBottomLeft,
                                                self.colorList)
            self.colorOptionsBox.draw(self.playWin)
            # Create covered code box
            self.coveredCode = Row(graphics.Point(0, yPoint + 80), self.code,
                                   self.colorList, covered=True)
            self.coveredCode.draw(self.playWin)
        # Else if the player option is the computer, the code at the top is
        # uncovered so the user can see it.
        else:
            self.coveredCode = Row(graphics.Point(0, yPoint + 80), self.code,
                                   self.colorList, covered=True)
            self.coveredCode.draw(self.playWin)
            self.coveredCode.uncover(self.playWin)

    def codeGenerator(self):
        ''' Generator function that can be used to generate a list of all
        possible codes.
        '''
        length = 4
        colors = len(self.colorList)
        code = [0] * length
        # Yield first code
        yield code.copy()
        while True:
            curSpot = 0
            # Find the first place that doesn't have maximum color value
            while code[curSpot] == colors - 1:
                curSpot += 1
                # If curSpot == length, then the last possible code was reached
                # so raise StopIteration().
                if curSpot == length:
                    raise StopIteration()
            # Increment by making everything that was maximum value 0, and
            # adding 1 to next color spot, then yield code.
            for j in range(curSpot):
                code[j] = 0
            code[curSpot] += 1
            yield code.copy()

    def getScore(self, guess):
        '''This function finds the minimum number of color combinations that
        the guess could eliminate if it were guessed. It also returns a
        boolean, Ture if it is in the list of remaining codes, otherwise False,
        and the guess itself.
        '''
        minEliminated = 1296
        # Loop through all possible feedback
        for feedback in self.possibleFeedback:
            eliminated = 0
            # Loop through the remaining codes to see how many the curren
            # guess would eliminate.
            for i in range(len(self.remainingCodes)):
                curFeedback = self.generateFeedback(guess,
                                                    self.remainingCodes[i])
                if curFeedback != feedback:
                    eliminated += 1
            if eliminated < minEliminated:
                minEliminated = eliminated
        # Return true if in remaining codes, or false if it isn't
        inRemainingCodes = guess in self.remainingCodes
        # Return the number eliminated, the boolean if it is or isn't in
        # remaining codes, and the guess that generated this.
        return minEliminated, inRemainingCodes, guess

    def getColorInput(self):
        '''This function gets the code guesses from either the Human user or
        the computer (depending on the player mode)
        '''
        # If the player is the human user, make the guess what the input in the
        # guess box
        if self.options['player'] == 'Human':
            return self.colorOptionsBox.getColors()
        # If the player is the computer, use the Donald Knuth algorithm to make
        # a guess
        elif self.options['player'] == 'Computer':
            # Create and draw the step button (which allows the computer to
            # make a new guess if clicked)
            step = TextButton(graphics.Point(350, 25),
                              graphics.Point(450, 75), 'Step',
                              'medium sea green')
            step.draw(self.playWin)
            # Loop waiting to see if step is clicked, if it is, break out of
            # the loop to take a turn.
            while True:
                click = self.playWin.getMouse()
                if click in step:
                    break
            # If this is the first guess, guess [0, 0, 1, 1,]
            if not self.lastGuess:
                guess = [0, 0, 1, 1]
                self.lastGuess = guess
            # If this is not the first guess:
            else:
                guess = self.lastGuess
                remainingCodes = self.remainingCodes.copy()
                for i in range(len(remainingCodes)):
                    # Find the feedback from comparing a remaining code to the
                    # last guess.
                    curFeedback = self.generateFeedback(guess,
                                                        remainingCodes[i])
                    # If the feedback isn't the same as when you compared the
                    # guess to the correct code in the last turn, remove that
                    # remaining code from the remaining codes list.
                    if curFeedback != self.lastFeedback:
                        self.remainingCodes.remove(remainingCodes[i])
                # Create a maxScoreGuess
                maxScoreGuess = (0, False, [0, 0, 0, 0])
                # This loop iterates through all the possible codes
                for guess in self.possibleCodes:
                    # Find the score of the guess (how many codes it would be
                    # able to eliminate in the worst case scenario)
                    curScoreGuess = self.getScore(guess)
                    # If the current score is greater than the maxScoreGuess,
                    # set maxScoreGuess to the curScoreGuess.
                    if curScoreGuess[0] > maxScoreGuess[0]:
                        maxScoreGuess = curScoreGuess
                    # If the two scores are equal but the curScoreGuess is in
                    # the list of remaining possible codes,set maxScoreGuess to
                    # the curScoreGuess
                    elif (curScoreGuess[0] == maxScoreGuess[0] and
                          curScoreGuess[1]):
                        maxScoreGuess = curScoreGuess
                # Set the gess to the best guess--the one stored in
                # maxScoreGuess
                guess = maxScoreGuess[2]
            # If that guess is in remaining codes, remove it
            if guess in self.remainingCodes:
                self.remainingCodes.remove(guess)
            # Set self.lastGuess to the new guess
            self.lastGuess = guess
            # Generate new feedback
            self.lastFeedback = self.generateFeedback(guess)
            # Return the best possible guess
            return guess

    def generateFeedback(self, guess, code=None):
        '''This function creates the feedback for the guess-- it compares the
        guess to the correct code and gives it red and white pegs accordingly
        (red == right color right place, white == right color, wrong place).
        '''
        # Create a copy of the guess and the code
        guess = guess.copy()
        if not code:
            code = self.code.copy()
        else:
            code = code.copy()
        # Initialize the feedback as 0 white 0 red pegs
        red = 0
        white = 0
        i = 0
        # Loop through the guess and see how many pegs/dots match the exact
        # color and place as the actual code. Each time there is one exact
        # match, increase the red count and delete both entries.
        while i < len(guess):
            if guess[i] == code[i]:
                red += 1
                del guess[i]
                del code[i]
            else:
                i += 1
        i = 0
        # Loop through the guess and see how many pegs/dots match the color,
        # but not thesame place as  that color in the actual code. Each time
        # there is one of these matches, increase the white count and delete
        # the entry from the guess.
        while i < len(guess):
            if guess[i] in code:
                white += 1
                code.remove(guess[i])
                del guess[i]
                i = 0
            else:
                i += 1
        # Return the red and white counts
        return (red, white)

    def displayOutcome(self, outcome):
        '''This function displays an outcome message on the screen of either a
        win on first try, win, or lose case.
        '''
        # Gets the correct subject of the sentence, you if the user is guessing
        # the code or the AI if the computer is guessing the code.
        if self.options['player'] == 'Human':
            player = 'You'
        else:
            player = 'The AI'
        # If there was a win, have the text be gold
        if outcome[0] == 'win':
            messageColor = 'Gold'
            # If it was won on the first guess make a special message saying
            # they are lucky.
            if outcome[1] == 0:
                message = '%s won on the\nfirst guess! Lucky!' % player
            # Else, make a message that says the player won in the amount of
            # turns it took.
            else:
                message = '%s won!!\nin %d turns!!!' % (player, outcome[1] + 1)
        # If the player loses, have the text be red
        elif outcome == 'loss':
            messageColor = 'red'
            codeNames = []
            # Make a list of all the different color names
            colorNames = ['Green', 'Red', 'Orange', 'Yellow', 'White',
                          'Blue']
            # Create a list with the list of names of all the colors in the
            # correct code
            for i in range(len(self.code)):
                codeNames.append(colorNames[self.code[i]])
            # Make a message saying the user lost and what the actual code was
            message = ('%s lost :/\nThe right code was:\n%s\n%s' %
                       (player, codeNames[0] + ', ' + codeNames[1],
                        codeNames[2] + ', ' + codeNames[3]))
        # Draw the message
        Y = (len(self.rows) + 1) * 80
        outcomeP1 = graphics.Point(325, Y - 100)
        outcomeP2 = graphics.Point(475, Y)
        self.outcomeButton = TextButton(outcomeP1, outcomeP2, message,
                                        'saddle brown')
        self.outcomeButton.setTextSize(14)
        self.outcomeButton.setTextColor(messageColor)
        self.outcomeButton.draw(self.playWin)

    def waitForNewGame(self):
        '''This function creates a new game button and waits for the user to
        click it.  When this happens, the function calls main, and starts a new
        game!
        '''
        # Create the button and the points for its location
        Y = (len(self.rows) + 1) * 80
        replayP1 = graphics.Point(350, Y - 200)
        replayP2 = graphics.Point(450, Y - 150)
        replayButton = TextButton(replayP1, replayP2, 'New Game',
                                  'medium sea green')
        # Draw the button
        replayButton.draw(self.playWin)
        # Wait until the button is clicked, when it is clicked, close the game
        # window and start a new game by calling main.
        while True:
            click = self.playWin.getMouse()
            if click in replayButton:
                self.playWin.close()
                main()

    def play(self):
        '''This functions calls all the other functions necessary to play the
        game after the opening screen and the options are chosen.
        '''
        # If the player is human (the human user is guessing the code), set a
        # random code.
        if self.options['player'] == 'Human':
            self.code = [random.randint(0, 5) for x in range(4)]
        # Else if the player is the computer (the human user is setting the
        # code), let the user create the code
        elif self.options['player'] == 'Computer':
            self.code = self.chooseComputerCode()
        # Create the Game window based on the amount of turnss
        self.initPlayWin(int(self.options['level']))
        # Set the outcome to loss at the beginning
        outcome = 'loss'
        # Play the game for how many rows (turns) there are
        for i in range(len(self.rows)):
            # Get input
            playerInput = self.getColorInput()
            self.rows[i].setPegColorList(playerInput)
            # Get feedback on the input
            feedback = self.generateFeedback(playerInput)
            self.rows[i].setFeedback(*feedback)
            # If the feedback is 4 red pegs (all right colors in all the right
            # places), the game has been won, set the outcome to win and how
            # many turns have passed, and break out of the loop (end the game).
            if feedback == (4, 0):
                outcome = ('win', i)
                break
        # Display either the win or lose messages, depending on the outcome
        self.displayOutcome(outcome)
        # If the player option was Human (the human user is guessing the code),
        # display the code that they were trying to guess.
        if self.options['player'] == 'Human':
            self.coveredCode.uncover(self.playWin)
        # Wait for the New Game button to be pressed
        self.waitForNewGame()


def main():
    '''This main function plays the game mastermind.'''
    game = Mastermind()
    game.play()


if __name__ == '__main__':
    main()
